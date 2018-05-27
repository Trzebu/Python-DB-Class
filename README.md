# Python-DB-Class
A very simple class to simplify basic operations with MySQL

## Requirements
* Python 3
* PyMySql

## How to use
### Class init:

```python
db = DB(host, user, password, database, resultToAssoc)
```
* host - MySQL server IP
* user - MySQL user
* password - MySQL password
* database - Database name
* resultToAssoc - If you set True, your MySQL results will be in the associative array

### Examples
#### 1. Query

```python
print(db.query("SELECT * FROM users").results())
>>> [{'id': 1, 'login': 'Test1', 'password': 'test'}, {'id': 2, 'login': 'Test2', 'password': 'test'}]
```

#### 2. Query

```python
print(db.query("SELECT id FROM users WHERE login = %s", 'Test1').first())
>>> [{'id': 1}]
````

#### 3. Get

```python
print(db.get('users', ['login', '=', 'Test1']).first())
>>> [{'id': 1, 'login': 'Test1', 'password': 'test}]
```

#### 4. Get only id and login

```python
print(db.getBy('users', ['id', 'login'], ['id', '=', '1']).first())
>>>[{'id': 1, 'login': 'Test1'}]
````

#### 5. Delete

```python
# if the removal was successful in the "count()" method, you will get the number of deleted records
print(db.delete('users', ['id', '=', '1']).count())
>>> 1
```

#### 6. Update

```python
# if the update was successful in the "count()" method, you will get the number of updated records
print(db.update('users', {'password': 'test1212'}, ['id', '=', '1']).count())
>>> 1
```

#### 7. Insert

```python
print(db.insert('users', {'login': 'NewUser', 'password': 'password'}).count())
>>> 1
```

##### Besides you can use:
* db.results() - get all rows 
* db.first() - get first row in array with records
##### Also in get, getBy and delete you can use this operators:
* = 
* >, <
* >=, <=
