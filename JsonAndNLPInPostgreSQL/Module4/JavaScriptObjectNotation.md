# Notes on JavaScript Object Notation (JSON)

---

## Data Serialization

---

**Data Serialization** is a problem when we are passing data between different languages or different systems of same language across the network.

### Two most common data structure we use in programming languages are **Linear Structure** and **Key Value Structure**

| Language   | Linear Structure       | Key Value Structure               |
| ---------- | ---------------------- | --------------------------------- |
| Python     | `list()` [1, 2, 3]     | `dict()` {"a": 1, "b": 2}         |
| JavaScript | `Array` [1, 2, 3]      | `Object` {"a": 1, "b": 2}         |
| PHP        | `Array` array(1, 2, 3) | `Array` array('a' => 1, 'b' => 2) |
| Java       | `ArrayList`            | `HashMap`                         |

We need a language independent way to serialize these data structures so that we can pass them across the network and use them in different languages.

We _serialize_ the data structure on one end and _deserialize_ it on the other end. Another term for this is **marshalling** and **unmarshalling**.

- **Serialization**: The process of converting a data structure into a format that can be easily stored or transmitted.
- **Deserialization**: The process of converting the serialized data back into its original data structure.

### XML - Initial Solution

A long time ago we used to use XML for this purpose. It is a markup language that uses tags to define elements. It is human readable but not very efficient for machines to parse.
It's a tree of tags. It is verbose and not very efficient for machines to parse.

For XML server side needed to convert native data structure into XML format and client side needed to convert XML format back into native data structure. This was a lot of overhead and not very efficient.

### JSON - Current Solution

Now a days we request only small amount of data from server side to update just a bit/corner of the webpage. This enables reactivity and better user experience.
`XML` is not suitable for this purpose because it is verbose and not very efficient for machines to parse. `JSON` is a better solution because it is lightweight and easy for machines to parse, especially in JavaScript.
Since JSON is native data structure in JavaScript, it is very easy to use and parse in JavaScript. It is also supported in many other languages, making it a good choice for data serialization.

David Crockford came up with a subset of JavaScript that can be used for data serialization and called it JSON. It is a lightweight data interchange format that is easy for humans to read and write, and easy for machines to parse and generate.

Slowly JSON becomes very dominant. Specially when JS was used for both client side and server side, JSON became the de facto standard for data serialization.

---

## Notes on Interview with David Crockford

---

- JSON has no versioning. It is not supposed to change.
- People automatically started preferring JSON over XML because it is more lightweight and easier to parse.
- JSON is a subset of JavaScript. It is a data format that is based on JavaScript syntax.
- JSON is a text format that is completely language independent but uses conventions that are familiar to programmers of the C-family of languages, including C, C++, C#, Java, JavaScript, Perl
