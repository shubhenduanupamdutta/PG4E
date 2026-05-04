# Notes on JavaScript in 3 Slides (For Python Developer)

---

## Python and JavaScript

---

| Python                                       | JavaScript                       |
| -------------------------------------------- | -------------------------------- |
| Created in 1991 (Pre Web)                    | Created in 1995 (For web)        |
| Interpreted                                  | Interpreted                      |
| Unique Syntax                                | Syntax derived from C            |
| White space is essential                     | White space ignored              |
| Data Structures: Lists, Tuples, Dictionaries | Data Structures: Arrays, Objects |

---

## Rosetta Stone

---

### Python

```python
#! file: rosetta.py
x = {'key': 'value', 'lines': 25}
print(x)
y = ['bob', 'alice']
print(y)

a = 17
if a < 20:
    print('Below 20')
else:
    print('20 or above')

for a in range(5):
    print(a)

print('/a/b/c'.split('/'))

c = 'hello' + '\n' + 'world'
print(c)
```

### JavaScript

```javascript
// file: rosetta.js
const x = { key: "value", lines: 25 };
console.log(x);
const y = ["bob", "alice"];
console.log(y);

const a = 17;
if (a < 20) {
	console.log("Below 20");
} else {
	console.log("20 or above");
}

for (let a = 0; a < 5; a++) {
	console.log(a);
}

console.log("/a/b/c".split("/"));

const c = "hello" + "\n" + "world";
console.log(c);
```
