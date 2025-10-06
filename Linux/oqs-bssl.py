import requests, yaml, re

def get_source(URL):
    response = requests.get(URL)
    return response.text

def convert_if_numeric(s):
    if s.isdigit():
        return f"0x{int(s):04x}"
    return s

def merge_sublists_by_first_element(big_list):
    merged = {}
    for sublist in big_list:
        if not sublist:
            continue
        key = sublist[0]
        if key in merged:
            merged[key].extend(sublist[1:])
        else:
            merged[key] = sublist[:]
    return list(merged.values())


html_source = get_source("https://raw.githubusercontent.com/open-quantum-safe/oqs-provider/refs/heads/main/oqs-template/generate.yml")

data = yaml.safe_load(html_source)

oqs_mapping = {}

for kem in data.get('kems', []):
    name = kem.get('name_group')
    oqs_meth = kem.get('oqs_alg')
    family = kem.get('family')
    if name and oqs_meth and family:
        oqs_mapping[name] = [oqs_meth, family]

for sig_family in data.get('sigs', []):
    family = sig_family.get('family')
    for variant in sig_family.get('variants', []):
        name = variant.get('name')
        oqs_meth = variant.get('oqs_meth')
        if name and oqs_meth and family:
            oqs_mapping[name] = [oqs_meth, family]

V = get_source("https://raw.githubusercontent.com/open-quantum-safe/oqs-provider/refs/heads/main/oqs-template/oqs-sig-info.md").split("\n")
T = []
for v in V:
    if "| " in v:
        t = v.split("| ")
        T.append([t[1].strip(),t[4].strip()])
V = get_source("https://raw.githubusercontent.com/open-quantum-safe/oqs-provider/refs/heads/main/oqs-template/oqs-kem-info.md").split("\n")
for v in V:
    if "| " in v:
        t = v.split("| ")
        T.append([t[3].strip(),t[5].strip()])
T1 = dict(T)

V = get_source("https://raw.githubusercontent.com/open-quantum-safe/oqs-provider/refs/heads/main/ALGORITHMS.md").split("\n")
T = []
for v in V:
    if "| OQS_" in v:
        t = v.split(" |")
        html_source = t[0][2:].strip()
        if html_source == "X25519MLKEM768":
            html_source = "x25519_mlkem768"
        elif html_source == "SecP256r1MLKEM768":
            html_source = "p256_mlkem768"
        elif html_source == "SecP384r1MLKEM1024":
            html_source = "p384_mlkem1024"
        T.append([html_source, convert_if_numeric(t[1].strip()).lower()])
algsList = merge_sublists_by_first_element(T)

T = []
for v in algsList:
    html_source = v[0]
    if (html_source.startswith("p") or html_source.startswith("x") or html_source.startswith("bp") or html_source.startswith("rsa")) and "_" in html_source:
        v2 = html_source.split("_", 1)[1]
    else:
        v2 = html_source
    v += oqs_mapping[v2]
    v.append(T1[v2].strip())
    T.append(v)
algsList = T


SSL_GROUP_MAP = {
    'p256': 'SSL_GROUP_SECP256R1',
    'p384': 'SSL_GROUP_SECP384R1',
    'p521': 'SSL_GROUP_SECP521R1',
    'x25519': 'SSL_GROUP_X25519',
    'x448': 'SSL_GROUP_X448',
}

# Define the KEM hybrid partners to include, based on the user's example and instructions.
ALLOWED_KEM_HYBRID_PARTNERS = {'p256', 'p384', 'x25519', 'p521'}

def encode_oid(oid_str):
    """Encodes an OID string into its ASN.1 hex byte representation."""
    if oid_str is None or oid_str.lower() == 'null':
        return None
    
    try:
        parts = [int(p) for p in oid_str.split('.')]
    except (ValueError, AttributeError):
        return None # Handle cases where oid_str is not a valid string

    if len(parts) < 2:
        return None
        
    encoded_bytes = []
    # First two components are encoded into a single byte: (a * 40) + b
    encoded_bytes.append(parts[0] * 40 + parts[1])

    # Subsequent components use variable-length encoding (base-128)
    for part in parts[2:]:
        if part == 0:
            encoded_bytes.append(0)
            continue
        
        sub_bytes = []
        while part > 0:
            sub_bytes.insert(0, part & 0x7F) # get the last 7 bits
            part >>= 7
        
        # Set the 'more' bit (MSB) for all but the last byte
        for i in range(len(sub_bytes) - 1):
            sub_bytes[i] |= 0x80
        encoded_bytes.extend(sub_bytes)
        
    return ', '.join([f'0x{b:02X}' for b in encoded_bytes])

def main(ALGORITHMS_DATA):
    """Main function to process algorithm data and generate the YAML file."""
    
    kems_map = {}
    sigs_list = []
    
    # --- First Pass: Create base entries for all non-hybrid KEMs ---
    for name, nid, _, oqs_meth, family, _ in ALGORITHMS_DATA:
        if 'KEM' in oqs_meth and '_' not in name:
            if name not in kems_map:
                kems_map[name] = {
                    'family': family,
                    'name': name,
                    'nid': nid,
                    'mix_with': [], # Initialize for hybrids
                    'oqs_meth': oqs_meth
                }

    # --- Second Pass: Process all algorithms to populate data ---
    for name, nid, oid, oqs_meth, family, sec_level in ALGORITHMS_DATA:
        if 'KEM' in oqs_meth:
            match = re.match(r'^([a-z0-9]+)_([a-zA-Z0-9]+.*)$', name)
            if match: # It's a hybrid KEM
                classical_part, base_name = match.groups()
                # Filter based on the allowed list
                if base_name in kems_map and classical_part in ALLOWED_KEM_HYBRID_PARTNERS:
                    mix_entry = {
                        'name': classical_part,
                        'mix_nid': nid,
                        'nid': SSL_GROUP_MAP.get(classical_part)
                    }
                    if mix_entry not in kems_map[base_name]['mix_with']:
                        kems_map[base_name]['mix_with'].append(mix_entry)
        
        elif 'SIG' in oqs_meth:
            # Ignore signature algorithms that are RSA hybrids, as per the implied rule
            if name.startswith('rsa'):
                continue

            sig_entry = {
                'family': family,
                'name': name,
                'oid': oid.replace('.', ' '),
                'oid_encoded': encode_oid(oid),
                'oqs_meth': oqs_meth,
                'code_point': nid,
                'claimed_security_level': sec_level
            }
            sigs_list.append(sig_entry)

    # --- Final Cleanup and Formatting for KEMs ---
    final_kems = list(kems_map.values())
    
    for kem in final_kems:
        if kem['mix_with']:
            kem['mix_with'] = sorted(kem['mix_with'], key=lambda x: x['name'])
            
            # Determine the default partner based on a preference order
            mix_names = [m['name'] for m in kem['mix_with']]
            if 'x25519' in mix_names:
                kem['use_as_default_with'] = 'x25519'
            elif 'p256' in mix_names:
                kem['use_as_default_with'] = 'p256'
            elif 'p384' in mix_names:
                kem['use_as_default_with'] = 'p384'
            elif 'p521' in mix_names:
                kem['use_as_default_with'] = 'p521'
            # No default is set if none of the preferred partners are present
        else:
            # Remove the empty list if no valid hybrids were found
            del kem['mix_with']
            
    # Sort the final lists by name for consistent output
    final_kems.sort(key=lambda x: x['name'])
    sigs_list.sort(key=lambda x: x['name'])
    
    final_data = {
        'kems': final_kems,
        'sigs': sigs_list
    }

    # --- Write to YAML file ---
    with open('crypto_config_generated.yml', 'w') as f:
        yaml.dump(final_data, f, sort_keys=False, default_flow_style=False, width=120)

    print("Successfully generated 'crypto_config_generated.yml'")

if __name__ == '__main__':
    # PyYAML is required. You can install it using: pip install pyyaml
    main(algsList)
