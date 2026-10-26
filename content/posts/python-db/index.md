---
title: "Python & DB"
date: "2024-01-02T12:00:00Z"
slug: "python-db"
description: "Here’s a comprehensive guide on using Python 3 with SQLite3."
categories: ["technical"]
tags: ["db", "python", "sqlite"]
aliases: ["/wps/2024/01/02/python-db/"]
recovered: "Internet Archive snapshot 2026-03-13"
---

`SQLite3` is a lightweight and easy-to-use database engine that is included with Python. It’s perfect for smaller-scale applications, prototyping, or standalone systems. Python’s `sqlite3` module allows seamless integration with SQLite databases.

Here’s a comprehensive guide on using Python 3 with SQLite3.

### Step 1: Importing the `sqlite3` Module

Start by importing the `sqlite3` module in your Python script:

```text
import sqlite3
```

### Step 2: Connecting to a Database

To use an `SQLite` database, establish a connection using `sqlite3.connect()`:

```text
conn = sqlite3.connect('example.db')
```

### Step 3: Creating a Cursor Object

Create a cursor object to interact with the database:

```text
cursor = conn.cursor()
```

### Step 4: Creating a Table

Use the cursor to execute SQL queries. For instance, to create a ‘users’ table:

```text
cursor.execute('''CREATE TABLE IF NOT EXISTS users ( id INTEGER PRIMARY KEY, name TEXT NOT NULL, email TEXT NOT NULL )''')
```

### Step 5: Inserting Data

Insert data into the table using the `execute()` method:

```text
cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", ('John', 'John@example.com')) cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", ('Doe', 'Doe@example.com'))
```

### Step 6: Committing Changes

Save the changes made to the database:

```text
conn.commit()
```

### Step 7: Retrieving Data

Retrieve data from the table using SQL queries:

```text
cursor.execute("SELECT * FROM users") rows = cursor.fetchall() for row in rows: print(row)
```

### Step 8: Closing the Connection

Close the connection to the database when finished:

```text
conn.close()
```

### Conclusion

Python’s integration with SQLite3 makes it effortless to create, manipulate, and manage databases within your Python scripts. SQLite3’s simplicity and Python’s versatility make it an ideal choice for small to medium-scale projects or standalone systems where a lightweight, file-based database is sufficient.

- [github](https://github.com/samarthya/pydb)
