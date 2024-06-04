# 导入所需的库和模块
import mysql.connector.pooling


# 创建一个连接池类，继承自mysql.connector.pooling.MySQLConnectionPool
class MysqlConnectionPool:
    def __init__(self, host, user, password, database, pool_size=5):
        self.config = {
            "host": host,
            "user": user,
            "password": password,
            "database": database,
        }
        self.pool_user = mysql.connector.pooling.MySQLConnectionPool(
                pool_name="user_pool", pool_size=pool_size, **self.config)
        self.pool_question = mysql.connector.pooling.MySQLConnectionPool(
                pool_name="question_pool", pool_size=pool_size, **self.config)

    def get_connection(self, db_name):
        return self.pool_user.get_connection() if db_name == 'user_pool' else self.pool_question.get_connection()


# 创建连接池实例
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "513022",
    "database": "question_test",
    "pool_size": 32
}
pool = MysqlConnectionPool(**db_config)


def get_connection(db_name):
    return pool.get_connection(db_name)
