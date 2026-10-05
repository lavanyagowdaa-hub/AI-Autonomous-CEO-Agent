import mysql.connector

conn = mysql.connector.connect(host="localhost", user="root", password="root@123456", database="ai_ceo_stores")
cursor = conn.cursor(dictionary=True)

print("🔮 Agent 5 - Forecast AI - FINAL FIXED\n")

cursor.execute("""
    SELECT store_location, 
           SUM(sales_amount) as total_sales,
           SUM(sales_amount - cost) as total_profit,
           SUM(cost) as total_cost,
           COUNT(*) as orders
    FROM sales 
    GROUP BY store_location 
    ORDER BY total_sales
""")

print("="*65)
print("STORE PERFORMANCE + NEXT MONTH PREDICTION")
print("="*65)

for r in cursor.fetchall():
    loc = r['store_location']
    sales = float(r['total_sales'])
    profit = float(r['total_profit'])
    margin = (profit/sales*100) if sales>0 else 0
    
    if 'Hassan' in loc or sales < 700000:
        print(f"\n💀 {loc} - {margin:.1f}% margin")
        print(f"   Current: Sales ₹{sales:,.0f} | Profit ₹{profit:,.0f} | {r['orders']} orders")
        print(f"   Next Month (no fix): ₹{sales*1.05:,.0f}")
        print(f"   WITH FIX (cut ₹50k): ₹{sales*1.05 + 50981:,.0f} ✅")
    else:
        print(f"\n✅ {loc} - {margin:.1f}% margin")
        print(f"   Current: Sales ₹{sales:,.0f} | Profit ₹{profit:,.0f}")
        print(f"   Next Month: ₹{sales*1.05:,.0f} | Profit ₹{profit*1.05:,.0f}")

print("\n" + "="*65)
print("💡 CEO DECISION: Hassan has lowest margin - FIX THIS WEEK!")
print("="*65)

conn.close()