import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

# --- CONNECT TO YOUR DB ---
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root@123456", # change if your MySQL password is different
    database="ai_ceo_stores"
)

print("🔍 Agent 1 Detective AI Started...\n")

# --- QUERY 1: Profit per Store ---
query = """
SELECT
    s.store_location,
    SUM(s.sales_amount) as total_sales,
    (SELECT SUM(m.spend_amount) FROM marketing m WHERE m.store_location = s.store_location) as total_marketing,
    (SELECT SUM(sp.resolution_cost) FROM support sp WHERE sp.store_location = s.store_location) as total_support
FROM sales s
GROUP BY s.store_location
"""

df = pd.read_sql(query, conn)

# Calculate profit
df['total_marketing'] = df['total_marketing'].fillna(0)
df['total_support'] = df['total_support'].fillna(0)
df['total_cost'] = df['total_marketing'] + df['total_support']
df['profit'] = df['total_sales'] - df['total_cost']
df['profit_margin_%'] = (df['profit'] / df['total_sales'] * 100).round(2)

df = df.sort_values(by='profit')

print("📊 STORE PROFIT REPORT:")
print(df.to_string(index=False))

# --- FIND CULPRIT ---
loss_stores = df[df['profit'] < 0]
profit_stores = df[df['profit'] >= 0]

print("\n" + "="*50)
if not loss_stores.empty:
    print("🚨 LOSS MAKING STORES FOUND:")
    for _, row in loss_stores.iterrows():
        print(f" -> {row['store_location']}: LOSS of ₹{-row['profit']:,.0f} | Sales: ₹{row['total_sales']:,.0f} | Cost: ₹{row['total_cost']:,.0f}")
else:
    print("✅ No loss stores! All profitable")

print(f"\n🏆 BEST STORE: {df.iloc[-1]['store_location']} with Profit ₹{df.iloc[-1]['profit']:,.0f}")
print(f"💀 WORST STORE: {df.iloc[0]['store_location']} with Profit ₹{df.iloc[0]['profit']:,.0f}")

# --- CHART ---
plt.figure(figsize=(10,5))
colors = ['red' if p < 0 else 'green' for p in df['profit']]
plt.bar(df['store_location'], df['profit'], color=colors)
plt.title('AI CEO - Profit by Store (Agent 1 Detective Report)', fontsize=12, fontweight='bold')
plt.ylabel('Profit (₹)')
plt.xticks(rotation=45)
plt.axhline(0, color='black', linewidth=1)
plt.tight_layout()
plt.savefig('agent1_profit_report.png')
print("\n📈 Chart saved as agent1_profit_report.png")

conn.close()