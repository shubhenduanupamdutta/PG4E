# Notes on Hashes and Hash Functions

---

## Hash Function

---

### **A _hash function_ is any function that can be used to map data of arbitrary size to a fixed size.**

- Output of a hash function is fixed in size regardless of the size of the input data like 128 bits, 256 bits, etc.

---

## Uses of Hashes

---

- **Checksum** - See if a message was altered in transit.
- **Cryptography / Signature** - See if a message comes from a trusted source.
- **Good hash functions enable fast lookup of data**
  - Python dictionaries
  - Database tables

---

## Good Hash Functions

---

- **Deterministic** - There can be no randomness - must get the same output for the same input.
- **Uniform Distribution** - Should have an equal chance of generating any value within range of its outputs - values don't cluster or collide.
- **Sensitive** - Any change in input should provide a change in output
- **One-way** - You should not be able to derive the input from the output (cannot reverse)

---

## Special Math for Hash Computation

---

### Bitwise Operators

- `<<` - Left Shift
- `^` - Exclusive OR (XOR)
- `&` - Bitwise AND
- `>>` - Right Shift

```sh
>>> x = 15
>>> y = ord('H')
>>> print('x', x, format(x, '08b'))
x 15 00001111
>>> print('y', y, format(y, '08b'))
y 72 01001000
>>> print('x^y', format(x^y, '08b'))
x^y 01000111
>>> print('x&y', format(x&y, '08b'))
x&y 00001000
>>> print('x<<1', format(x<<1, '08b'))
x<<1 00011110
>>> print('x>>1', format(x>>1, '08b'))
x>>1 00000111
```

---

## The Science/Math of Hashing

---

- Designing Hash Computation is serious work
- National Institute of Standards and Technology (NIST) runs multi-year **competitions** when new hashing algorithms are needed.
- Sometimes algorithms have flaws that are detected years later and we deprecate them.

---

## The **classic** Hash - `MD5`

- For example, the **MD5** algorithm was designed in 1991 and was widely used for many years but it was found to have flaws in 2004 and is now considered deprecated.
- 128 bit hash
- Widely implemented
- Broken for cryptography
  - Can alter data in transit without breaking a signature
  - Rainbow tables use forward computation and storage to reverse MD5 for short input strings (Password Hashing)
- This still can be used for unique identifiers for data that is not security sensitive.

---

## `SHA-256` - A Modern Hash

---

- A family of related hashes called "SHA-2"
- Created in 2001
- There are many hashes which competed to become `SHA-2`
- There are many sizes of `SHA-2` - 256 bit, 512 bit, etc.
