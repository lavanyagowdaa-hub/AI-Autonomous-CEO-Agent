import pandas as pd, mysql.connector
conn = mysql.connector.connect(host="localhost", user="root", password="root@123456", database="ai_ceo_stores")
for table in ["sales","marketing","support"]:
    df = pd.read_sql(f"SELECT * FROM {table}", conn)
    df.to_csv(f"{table}.csv", index=False)
    print(f"Saved {table}.csv")
conn.close()