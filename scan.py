import sys

p = sys.argv[1]
f = open(p, 'rb')
f.seek(0, 2)
size = f.tell()
found = []
pos = 0
chunk = 64 * 1024 * 1024
while pos < size:
    f.seek(pos)
    data = f.read(chunk)
    start = 0
    while True:
        i = data.find(b'\x53\xef', start)
        if i < 0:
            break
        abs_off = pos + i
        if abs_off % 1024 == 0x438 % 1024:
            sb = abs_off - 0x438
            f.seek(sb + 0x480)
            vol = f.read(16).split(b'\x00')[0]
            if vol in (b'system', b'system_ext', b'data', b'cache'):
                found.append((sb, vol.decode(errors='replace')))
        start = i + 1
    pos += chunk
for off, vol in found:
    print(off, vol)
