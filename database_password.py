import pysqlcipher3

def create_encrypted_db(db_path, password):
    # 连接到数据库（如果文件不存在，则创建它）
    conn = pysqlcipher3.connect(db_path)

    # 启用加密功能（这部分是SQLCipher的扩展功能）
    conn.execute(f"PRAGMA key = '{password}';")

    # 创建一个表作为示例
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        );
    ''')

    # 提交事务并关闭连接
    conn.commit()
    conn.close()

# 使用方法
db_path = "encrypted_database.db"
password = "my_secure_password"

create_encrypted_db(db_path, password)
print(f"加密数据库已创建: {db_path}")
