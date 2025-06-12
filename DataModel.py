import json

from PySide6.QtCore import QObject, Signal
import sqlite3

class DataModel(QObject):
    dataChanged = Signal()  # 数据变化信号

    def __init__(self, db_path):
        super().__init__()
        self.db_path = db_path
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        # 初始化时检查并创建表结构
        self.initialize_tables()
        self.device_mapping = {
            "1": "single",
            "2": "double",
            "3": "equal"
        }
        self.mode_mapping = {
            "3": "self_order",
            "4": "equal",
            "5": "cross",
            "6": "order"
        }

    def initialize_tables(self):
        # 检查并创建 keys 表
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS keys (
                key_id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                key TEXT NOT NULL,
                fingerprint TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'active'
            );
        """)

        # 检查并创建 param 表
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS param (
                ID INTEGER PRIMARY KEY AUTOINCREMENT, 
                production TEXT, 
                num INTEGER, 
                mode TEXT, 
                motion_param TEXT(256), 
                swing_mode TEXT, 
                device_name TEXT, 
                full_motion_param TEXT(512), 
                belt_speed INTEGER, 
                ceramic_width INTEGER, 
                beam_swing_speed INTEGER, 
                stay_time INTEGER
            );
        """)

        # 检查并创建 users 表
        self.cursor.execute("""
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
        """)

        # 提交事务
        self.connection.commit()
    def fetch_data(self):
        """从数据库获取数据"""
        self.cursor.execute("SELECT rowid,  mode, swing_mode,belt_speed,ceramic_width,beam_swing_speed,stay_time,stay_time,device_name,full_motion_param FROM param")
        return self.cursor.fetchall()

    def add_data(self, params, current_mode, values, swing_mode,device_name):
        """向数据库新增数据"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                # 将 params 字典序列化为 JSON 字符串
                full_motion_param_json = json.dumps(params)
                data = [
                    (params['lineEdit_production_volume'],
                     params['lineEdit_num_input'],
                     current_mode,
                     values,
                     swing_mode,
                     device_name,
                     full_motion_param_json,
                     params['lineEdit_belt_speed'],
                     params['lineEdit_ceramic_width'],
                     params['lineEdit_beam_swing_speed'],
                     params['lineEdit_stay_time_output'])
                ]
                cursor.executemany(
                    'INSERT INTO param (production, num, mode, motion_param, swing_mode,device_name,full_motion_param,belt_speed,ceramic_width,beam_swing_speed,stay_time) VALUES (?,?,?,?,?,?,?,?,?,?,?)',
                    data
                )
                conn.commit()
                print("Data inserted successfully.")
                self.dataChanged.emit()  # 发出数据变化信号
                print('Signal data change: New data is added')
                return True
        except sqlite3.Error as e:
            print(f"Error inserting data: {e}")
            return False

    def delete_data(self, row_id):
        """从数据库删除数据"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM param WHERE rowid=?", (row_id,))
                print("Data deleted successfully.")
                self.dataChanged.emit()  # 发出数据变化信号
                print('Signal data change: Delete data')
        except sqlite3.Error as e:
            print(f"Error deleting data: {e}")

    def delete_multiple_data(self, row_ids):
        """批量删除数据"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                # 使用 executemany 批量删除
                cursor.executemany("DELETE FROM param WHERE rowid=?", [(row_id,) for row_id in row_ids])
                conn.commit()  # 确保事务提交
                print(f"Deleted {len(row_ids)} rows successfully.")
                self.dataChanged.emit()  # 发出数据变化信号
        except sqlite3.Error as e:
            print(f"Error deleting multiple data: {e}")

    def query(self, row_id):
        """根据 rowid 查询数据，并将 full_motion_param 反序列化为字典"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT production, num, mode, motion_param, swing_mode, device_name, full_motion_param FROM param WHERE rowid=?",
                    (row_id,)
                )
                result = cursor.fetchone()
                if result:
                    # 将 full_motion_param 反序列化为字典
                    full_motion_param_dict = json.loads(result[6])
                    # 返回查询结果和反序列化后的字典
                    return {
                        "production": result[0],
                        "num": result[1],
                        "mode": result[2],
                        "motion_param": result[3],
                        "swing_mode": result[4],
                        "device_name": result[5],
                        "full_motion_param": full_motion_param_dict  # 反序列化后的字典
                    }
                else:
                    print(f"No data found for rowid {row_id}")
                    return None
        except sqlite3.Error as e:
            print(f"Error querying data: {e}")
            return None

    def query_full(self, row_ids):
        """根据 row_ids 数组查询所有匹配的数据，并将 full_motion_param 反序列化为字典数组"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                # 构建 SQL 查询语句
                query = """
                SELECT device_name,swing_mode, full_motion_param
                FROM param
                WHERE rowid IN ({})
                """.format(",".join("?" for _ in row_ids))  # 动态生成占位符

                # 执行查询
                cursor.execute(query, row_ids)
                results = cursor.fetchall()

                # 将 full_motion_param 反序列化为字典数组
                data_list = []
                for result in results:
                    full_motion_param_dict = json.loads(result[2])  # 反序列化
                    full_motion_param_dict['device'] = self.device_mapping.get(full_motion_param_dict['device'])
                    full_motion_param_dict['mode'] = self.mode_mapping.get(full_motion_param_dict['mode'])
                    data_list.append(full_motion_param_dict)

                return data_list  # 返回字典数组
        except sqlite3.Error as e:
            print(f"Error querying multiple data: {e}")
            return []
    def close(self):
        """关闭数据库连接"""
        self.connection.close()