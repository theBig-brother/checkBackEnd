import sqlite3
import json

def export_database_to_console_and_file(db_path, output_file):
    try:
        # 连接到 SQLite 数据库
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # 获取所有表名
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        # 创建一个存储所有表数据的字典
        db_data = {}

        for table_name in tables:
            table_name = table_name[0]
            if table_name == "sqlite_sequence":  # 跳过 SQLite 的系统表
                continue

            # 获取表的所有记录
            cursor.execute(f"SELECT * FROM {table_name};")
            rows = cursor.fetchall()

            # 获取表的列名
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = [column[1] for column in cursor.fetchall()]

            # 将数据存储为字典格式
            db_data[table_name] = {
                "columns": columns,
                "records": rows
            }

            # 输出到控制台
            print(f"Table: {table_name}")
            print(f"Columns: {columns}")
            print("Records:")
            for row in rows:
                print(row)
            print("-" * 50)

        # 将数据保存到文件
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(db_data, f, indent=4, ensure_ascii=False)

        print(f"Database records exported to {output_file} successfully!")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

# 使用示例
if __name__ == "__main__":
    db_path = "db.sqlite3"  # 替换为你的 SQLite 数据库路径
    output_file = "db_export.json"  # 导出的文件名
    export_database_to_console_and_file(db_path, output_file)
