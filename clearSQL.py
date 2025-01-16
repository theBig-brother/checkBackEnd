import sqlite3

def clear_database(db_path):
    try:
        # 连接到 SQLite 数据库
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # 获取所有表名
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        # 清空每个表的数据
        for table_name in tables:
            table_name = table_name[0]
            if table_name == "sqlite_sequence":  # 跳过 SQLite 的系统表
                continue
            cursor.execute(f"DELETE FROM {table_name};")
            print(f"Cleared table: {table_name}")

        # 重置自增序列（如果有的话）
        cursor.execute("DELETE FROM sqlite_sequence;")

        # 提交更改并关闭连接
        conn.commit()
        print("Database cleared successfully!")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

# 使用示例
if __name__ == "__main__":
    db_path = "db.sqlite3"  # 替换为你的 SQLite 数据库路径
    clear_database(db_path)
