"""An example of simple hash function."""

# This is a terrible hash function but it should give a good idea.
while True:
    txt = input("Enter a string to hash: ")
    if len(txt) < 1:
        break

    hv = 0
    for let in txt:
        hv = ((hv << 1) ^ ord(let)) & 0xFFFFFF
        if hv < 2000:  # noqa: PLR2004
            print(let, format(ord(let), "08b"), format(hv, "16b"), format(ord(let), "03d"), hv)
    print(format(hv, "08x"), hv)
