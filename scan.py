import sys

p = sys.argv[1]
f = open(p, 'rb')
f.seek(0, 2)
size = f.tell()
found = []
pos = 0
chunk = 64 * 1024 * 1024
carry = b''
while pos < size:
    f.seek(pos)
    data = carry + f.read(chunk)
    start = 0
    while True:
        i = data.find(b'\x53\xef', start)
        if i < 0:
            break
        abs_off = pos - len(carry) + i
        sb = abs_off - 0x438
        if sb >= 0:
            f.seek(sb + 0x480)
            vol = f.read(16).split(b'\x00')[0]
            if vol in (b'system', b'system_ext', b'data', b'cache', b'vendor'):
                found.append((sb, vol.decode(errors='replace')))
        start = i + 1
    carry = data[-1:]
    pos += chunk
seen = set()
for off, vol in found:
    if off not in seen:
        seen.add(off)
        print(off, vol)
