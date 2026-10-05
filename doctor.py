import mysql.connector
import pandas as pd

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root@123456",
    database="ai_ceo_stores"
)
cursor = conn.cursor(dictionary=True)

print("🩺 Agent 2 - Doctor AI Diagnosing...\n")

worst_store = "Hassan"
print(f"Investigating weakest store: {worst_store}\n")

# 1. MARKETING
print("="*60)
print("1️⃣ MARKETING SPEND ANALYSIS")
print("="*60)
cursor.execute("""
    SELECT store_location, SUM(spend_amount) as total_spend,
           COUNT(*) as campaigns,
           AVG(spend_amount) as avg_per_campaign
    FROM marketing 
    GROUP BY store_location ORDER BY total_spend DESC
""")
for row in cursor.fetchall():
    flag = "🔴 HIGHEST SPEND!" if row['store_location']==worst_store else ""
    print(f"{row['store_location']:25} Spend: ₹{row['total_spend']:,.0f} | Campaigns: {row['campaigns']} {flag}")

cursor.execute(f"""
    SELECT platform, SUM(spend_amount) as spend, COUNT(*) as cnt
    FROM marketing WHERE store_location='{worst_store}'
    GROUP BY platform ORDER BY spend DESC
""")
print(f"\n  -> {worst_store} platform breakdown:")
for r in cursor.fetchall():
    print(f"     {r['platform']}: ₹{r['spend']:,.0f} ({r['cnt']} times)")

# 2. SUPPORT
print("\n" + "="*60)
print("2️⃣ CUSTOMER SUPPORT BURDEN")
print("="*60)
cursor.execute("""
    SELECT store_location, COUNT(*) as tickets,
           SUM(resolution_cost) as total_cost,
           AVG(resolution_cost) as avg_cost
    FROM support GROUP BY store_location ORDER BY total_cost DESC
""")
for row in cursor.fetchall():
    flag = "🔴 MOST COMPLAINTS!" if row['store_location']==worst_store else ""
    print(f"{row['store_location']:25} Tickets: {row['tickets']} | Cost: ₹{row['total_cost']:,.0f} {flag}")

cursor.execute(f"""
    SELECT issue_type, COUNT(*) as cnt, SUM(resolution_cost) as cost
    FROM support WHERE store_location='{worst_store}'
    GROUP BY issue_type ORDER BY cost DESC
""")
print(f"\n  -> {worst_store} issue breakdown:")
for r in cursor.fetchall():
    print(f"     {r['issue_type']}: {r['cnt']} tickets | ₹{r['cost']:,.0f}")

# 3. SALES
print("\n" + "="*60)
print("3️⃣ SALES PERFORMANCE")
print("="*60)
cursor.execute("""
    SELECT store_location, COUNT(*) as transactions,
           SUM(sales_amount) as sales,
           AVG(sales_amount) as avg_sale
    FROM sales GROUP BY store_location ORDER BY sales ASC
""")
for row in cursor.fetchall():
    flag = "🔻 LOWEST SALES" if row['store_location']==worst_store else ""
    print(f"{row['store_location']:25} Sales: ₹{row['sales']:,.0f} | Avg: ₹{row['avg_sale']:,.0f} {flag}")

cursor.execute(f"""
    SELECT product, COUNT(*) as orders, SUM(sales_amount) as sales
    FROM sales WHERE store_location='{worst_store}'
    GROUP BY product ORDER BY sales DESC
""")
print(f"\n  -> {worst_store} product breakdown:")
for r in cursor.fetchall():
    print(f"     {r['product']}: ₹{r['sales']:,.0f} ({r['orders']} orders)")

print("\n" + "="*60)
print("💊 DOCTOR'S FINAL DIAGNOSIS")
print("="*60)
cursor.execute(f"SELECT SUM(spend_amount) as m FROM marketing WHERE store_location='{worst_store}'")
m_spend = cursor.fetchone()['m'] or 0
cursor.execute(f"SELECT SUM(resolution_cost) as s FROM support WHERE store_location='{worst_store}'")
s_cost = cursor.fetchone()['s'] or 0
cursor.execute(f"SELECT SUM(sales_amount) as sa FROM sales WHERE store_location='{worst_store}'")
sales = cursor.fetchone()['sa'] or 0
marketing_pct = (m_spend / sales * 100) if sales else 0
print(f"Store: {worst_store} | Sales ₹{sales:,.0f} | Marketing ₹{m_spend:,.0f} ({marketing_pct:.1f}%) | Support ₹{s_cost:,.0f}")
print("\n✅ Diagnosis done. Ready for Agent 3 - Strategist AI")

conn.close()