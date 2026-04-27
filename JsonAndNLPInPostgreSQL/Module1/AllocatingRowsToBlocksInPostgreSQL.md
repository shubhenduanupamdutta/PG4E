# Notes on Allocating Rows to Blocks in PostgreSQL

---

## Row data layout

---

- Row data is stored in blocks of 8KB in PostgreSQL, usually.
- Each block can contain multiple rows, depending on the size of the rows and the block.
- 8KiB blocks are the default size, this makes calculating block offsets easier, as 8KiB = 8192 bytes, and thus block offsets can be calculated using powers of 2.
- Block is often the unit of locking and caching.
- A block are stored one after another in the disk.

### Block Layout

- Each block has a header, which contains metadata about the block, such as the number of rows, size of free space, and **pointers to the rows (called offsets)**.
- The rows are stored from the back of the block towards the front.
- Start of the block contains offsets, which point to the location of the rows in the block. These offsets are stored at the start of the block.
- **Offsets grow from the front of the block towards the back, while rows grow from the back of the block towards the front. Rest of the block is _free space_**.
- Since columns can be of variable length, this means that the size of the rows can vary, and thus the number of rows that can fit in a block can also vary.
- When a row is updated, the position of rows (i.e. offsets) may change, as the size of the row may change, and thus the offsets need to be updated accordingly.

- **Key point to take away - we read entire block in the memory. So we need to know where the row starts in the memory.**
