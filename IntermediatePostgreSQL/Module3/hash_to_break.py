"""A hash function which need to be broken by finding a collision."""


def hash_to_break(input_string: str) -> int:
    """Hash function to break. It is not a good hash function."""
    hv = 0
    pos = 0
    for let in input_string:
        pos = (pos % 3) + 1
        hv = (hv + (pos * ord(let))) % 1_000_000
        print(let, pos, ord(let), hv)
    return hv


if __name__ == "__main__":
    try:
        while True:
            s = input("Enter a string to hash: ")
            print(hash_to_break(s))
    except KeyboardInterrupt:
        print("\nExiting.")

"""Notes for breaking
Since the hash is simple multiplication of position and ASCII int value and then addition.

If we change the position of character where position value is same then we can get same hash value

"""
