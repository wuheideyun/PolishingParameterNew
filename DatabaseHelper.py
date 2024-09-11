import sqlite3
import hashlib
import sys

from PySide6.QtWidgets import QApplication


class DatabaseHelper:
    def __init__(self, db_name):
        # 初始化数据库连接
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def close(self):
        # 关闭数据库连接
        self.conn.close()

    def create_table(self, create_table_sql):
        """创建数据库表"""
        try:
            self.cursor.execute(create_table_sql)
            self.conn.commit()
            print("表创建成功")
        except sqlite3.Error as e:
            print(f"创建表时出错: {e}")

    def insert(self, table, data):
        """插入数据到表中"""
        try:
            keys = ', '.join(data.keys())
            values = ', '.join(['?'] * len(data))
            sql = f'INSERT INTO {table} ({keys}) VALUES ({values})'
            self.cursor.execute(sql, tuple(data.values()))
            self.conn.commit()
            print("数据插入成功")
        except sqlite3.Error as e:
            print(f"插入数据时出错: {e}")

    def read(self, table, columns='*', conditions=None):
        """读取数据"""
        try:
            sql = f'SELECT {columns} FROM {table}'
            if conditions:
                sql += f' WHERE {conditions}'
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            return result
        except sqlite3.Error as e:
            print(f"读取数据时出错: {e}")
            return None

    def update(self, table, data, conditions):
        """更新表中单条数据"""
        try:
            set_clause = ', '.join([f'{key} = ?' for key in data.keys()])
            sql = f'UPDATE {table} SET {set_clause} WHERE {conditions}'
            self.cursor.execute(sql, tuple(data.values()))
            self.conn.commit()
            print("数据更新成功")
        except sqlite3.Error as e:
            print(f"更新数据时出错: {e}")

    def batch_update(self, table, data_list, conditions):
        """批量更新数据"""
        try:
            for data in data_list:
                self.update(table, data, conditions)
            print("批量更新成功")
        except sqlite3.Error as e:
            print(f"批量更新时出错: {e}")

    def delete(self, table, conditions):
        """从表中删除数据"""
        try:
            sql = f'DELETE FROM {table} WHERE {conditions}'
            self.cursor.execute(sql)
            self.conn.commit()
            print("数据删除成功")
        except sqlite3.Error as e:
            print(f"删除数据时出错: {e}")

    def hash_password(self, password):
        """对密码进行哈希处理"""
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_login(self, table, username, password):
        """验证用户名和密码"""
        try:
            hashed_password = self.hash_password(password)
            sql = f'SELECT * FROM {table} WHERE username = ? AND password_hash = ?'
            self.cursor.execute(sql, (username, hashed_password))
            result = self.cursor.fetchone()
            return result is not None  # 如果存在匹配的账号密码，返回True，否则返回False
        except sqlite3.Error as e:
            print(f"验证登录时出错: {e}")
            return False

    def bulk_insert(self, table, data_list):
        """批量插入数据"""
        try:
            if not data_list:
                print("插入数据为空")
                return
            keys = ', '.join(data_list[0].keys())
            values_placeholder = ', '.join(['?'] * len(data_list[0]))
            sql = f'INSERT INTO {table} ({keys}) VALUES ({values_placeholder})'
            self.cursor.executemany(sql, [tuple(data.values()) for data in data_list])
            self.conn.commit()
            print("批量插入成功")
        except sqlite3.Error as e:
            print(f"批量插入时出错: {e}")

    def test_create_table_sql(self, db):
        create_table_sql = '''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                email TEXT,
                phone TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                status TEXT DEFAULT 'active',
                role TEXT DEFAULT 'user'
            );
            '''
        db.create_table(create_table_sql)

    def test_insert_user(self, db):
        user_data = {
            'username': 'admin',
            'password_hash': db.hash_password('123456'),
            'email': 'admin@example.com',
            'phone': '1234567890'
        }
        db.insert('users', user_data)

    def test_batch_insert_user(self, db):
        data_list = [
            {'username': 'user1', 'password_hash': db.hash_password('pass1'), 'email': 'user1@example.com'},
            {'username': 'user2', 'password_hash': db.hash_password('pass2'), 'email': 'user2@example.com'}
        ]
        db.bulk_insert('users', data_list)

    def test_batch_update_user2(self, db):
        data_list = [
            {'phone': '1111111111', 'status': 'active'},
            {'phone': '2222222222', 'status': 'locked'}
        ]
        db.batch_update('users', data_list, "role = 'user'")

    def test_update_user(self, db):
        update_data = {'phone': '0987654321', 'status': 'suspended'}
        db.update('users', update_data, "username = 'john_doe'")


if __name__ == '__main__':
    app = QApplication(sys.argv)


    db = DatabaseHelper('database.db')


    db.test_create_table_sql(db)
    db.test_insert_user(db)



