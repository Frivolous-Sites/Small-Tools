CHUNK_SIZE = 90000000 # 90MB = 90,000,000 Bytes
file_number = 1
with open('A.mp4', 'rb') as f:
    chunk = f.read(CHUNK_SIZE)
    while chunk:
        with open('A_' + str(file_number), 'wb') as chunk_file:
            chunk_file.write(chunk)
        file_number += 1
        chunk = f.read(CHUNK_SIZE)


files = ["A_1", "A_2", "A_3", "A_4", "A_5"]
output_file = "B.mp4"
out_data = b''
for fn in files:
    with open(fn, 'rb') as fp:
        out_data += fp.read()
with open(output_file, 'wb') as fi:
    fi.write(out_data)
