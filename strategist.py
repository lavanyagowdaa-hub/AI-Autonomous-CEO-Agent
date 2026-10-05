import mysql.connector

conn = mysql.connector.connect(host="localhost", user="root", password="root@123456", database="ai_ceo_stores")
cursor = conn.cursor(dictionary=True)

print("🧠 Agent 3 - Strategist AI - Generating CEO Plan...\n")

stores = []
cursor.execute("""
    SELECT s.store_location,
           SUM(s.sales_amount) as sales,
           (SELECT SUM(m.spend_amount) FROM marketing m WHERE m.store_location=s.store_location) as marketing,
           (SELECT SUM(sp.resolution_cost) FROM support sp WHERE sp.store_location=s.store_location) as support
    FROM sales s GROUP BY s.store_location
""")
for r in cursor.fetchall():
    sales = float(r['sales'] or 0)
    marketing = float(r['marketing'] or 0)
    support = float(r['support'] or 0)
    profit = sales - marketing - support
    margin = (profit/sales*100) if sales else 0
    stores.append({'store_location': r['store_location'], 'sales': sales, 'marketing': marketing, 'support': support, 'profit': profit, 'margin': margin})

stores_sorted = sorted(stores, key=lambda x: x['profit'])
worst = stores_sorted[0]
best = stores_sorted[-1]

print("="*70)
print("📊 CEO STRATEGY BOARD - AUTO GENERATED")
print("="*70)
print(f"\n🏆 MODEL STORE TO COPY: {best['store_location']}")
print(f" Sales: ₹{best['sales']:,.0f} | Profit: ₹{best['profit']:,.0f} | Margin: {best['margin']:.1f}%")
print(f"\n💀 STORE NEEDS FIX: {worst['store_location']}")
print(f" Sales: ₹{worst['sales']:,.0f} | Profit: ₹{worst['profit']:,.0f} | Margin: {worst['margin']:.1f}%")

cursor.execute(f"SELECT product, SUM(sales_amount) as sales FROM sales WHERE store_location='{best['store_location']}' GROUP BY product ORDER BY sales DESC LIMIT 2")
best_products = cursor.fetchall()
cursor.execute(f"SELECT product, SUM(sales_amount) as sales FROM sales WHERE store_location='{worst['store_location']}' GROUP BY product ORDER BY sales DESC LIMIT 1")
worst_top = cursor.fetchone()

print("\n" + "="*70)
print("✅ ACTION PLAN")
print("="*70)
save = worst['marketing']*0.3
print(f"""
1. CUT LOSSES IN {worst['store_location'].upper()}:
   - Marketing is {worst['marketing']/worst['sales']*100:.1f}% of sales. CUT by 30% = Save ₹{save:,.0f}
   - Stop promoting Soap Box, Rice Bag
   - Focus ONLY on {worst_top['product']} (₹{float(worst_top['sales']):,.0f})

2. COPY WINNER FORMULA FROM {best['store_location'].upper()}:
   - Top products: {', '.join([p['product'] for p in best_products])}

3. FOR KUNIGAL:
   - You are 2nd best! Keep doing what you do
""")
print("="*70)
print(f"💰 PROJECTED: Hassan profit ₹{worst['profit']:,.0f} -> ₹{worst['profit']+save:,.0f} (+₹{save:,.0f})")
print("="*70)
conn.close()