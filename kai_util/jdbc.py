import mysql.connector


# 连接Oracle数据库
class OracleJDbc:

    def __init__(self):
        pass


pass


class MySqlJDbc:

    def __init__(self, url, user, pwd, database):
        self.base = mysql.connector.connect(host=url, user=user, passwd=pwd, database=database)
        self.conn = self.base.cursor()
        pass

    def execute(self, query):
        self.conn.execute(query)
        pass


pass
