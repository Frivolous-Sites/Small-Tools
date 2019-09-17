for i in {248..252} ; do for j in 89.208.$i.{0..255} ; do ping $j -c 2 -W 1 | \
    grep "bytes from" >> ip.txt & done ; done
