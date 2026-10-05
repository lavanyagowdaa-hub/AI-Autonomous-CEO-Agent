import mysql.connector
conn = mysql.connector.connect(host="localhost", user="root", password="root@123456", database="ai_ceo_stores")
cursor = conn.cursor()
for table in ['marketing','support','sales']:
    print(f"\n=== {table.upper()} COLUMNS ===")
    cursor.execute(f"SHOW COLUMNS FROM {table}")
    for col in cursor.fetchall():
        print(col[0])
conn.close()