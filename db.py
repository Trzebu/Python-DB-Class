import pymysql

class DB:
    _host = None
    _user = None
    _password = None
    _database = None
    _cursor = None
    _connection = None
    _results = None
    _count = None
    _resultToAssoc = None

    def __init__(self, host, user, password, db, resultToAssoc = True):
        self._host = host
        self._user = user
        self._password = password
        self._database = db
        self._resultToAssoc = resultToAssoc

    def _open(self):
        try:
            self._connection = pymysql.connect(host = self._host, user = self._user, password = self._password, db = self._database)
            if self._resultToAssoc:
                self._cursor = self._connection.cursor(pymysql.cursors.DictCursor)
            else:
                self._cursor = self._connection.cursor()
        except pymysql.InternalError as error:
            code, message = error.args
            print("[DB Class]-=FatalError=-", code, message)

    def _close(self):
        self._cursor.close()
        self._connection.close()

    def query(self, sql, values = []):
        self._open()
        self._count = self._cursor.execute(sql, values)
        if self._count > 0:
            self._results = self._cursor.fetchall()
        self._connection.commit()
        self._close()
        return self

    def _action(self, action, table, where):
        if len(where) == 3:
            operators = ['=', '>', '<', '>=', '<=']

            field = where[0]
            operator = where[1]
            value = str(where[2])

            if operator in operators:
                sql = str(action) + ' FROM ' + str(table) + ' WHERE ' + str(field) + ' ' + str(operator) + ' %s'
                return self.query(sql, value)

            else:
                print('[DB Class]-=warning=- Operator %s is uncorrect.' % (operator))
        else:
            print('[DB Class]-=warning=- Second parametr must have 3 arguments, but %s given.' % (len(where)))

    def insert(self, table, fields):
        sql = "INSERT INTO " + table
        keys = []
        values_amount = []
        values = []
        if type(fields) is dict:
            for i, j in fields.items():
                keys.append(i)
                values.append(j)
                values_amount.append('%s')
        else:
            print("[DB Class]-=warning=- Fields they must be in dict.")

        sql += " (" + ','.join(keys) + ")" + " VALUES (" + ','.join(values_amount) + ")"
        return self.query(sql, values)

    def update(self, table, fields, where):
        if len(where) == 3:
            operators = ['=', '>', '<', '>=', '<=']
            field = where[0]
            operator = where[1]
            value = str(where[2])

            if operator in operators:
                sql = "UPDATE " + table + " SET "
                keys = []
                values = []

                if type(fields) is dict:
                    for i, j in fields.items():
                        keys.append(i + '=%s')
                        values.append(j)

                    sql += ','.join(keys) + ' WHERE ' + field + operator + '\'' + value + '\''
                    return self.query(sql, values)

                else:
                   print("[DB Class]-=warning=- Fields they must be in dict.") 
            else:
                print('[DB Class]-=warning=- Operator %s is uncorrect.' % (operator))
        else:
            print('[DB Class]-=warning=- Second parametr must have 3 arguments, but %s given.' % (len(where)))

    def get(self, table, where):
        return self._action("SELECT *", table, where)

    def getBy(self, table, columns, where):
        keys = []
        for i in columns:
            keys.append(i)
        sql = "SELECT " + ','.join(keys)
        return self._action(sql, table, where)

    def delete(self, table, where):
        return self._action("DELETE", table, where)

    def results(self):
        return self._results

    def first(self):
        return self._results[0]

    def count(self):
        return self._count