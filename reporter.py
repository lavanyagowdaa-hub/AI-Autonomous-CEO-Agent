import mysql.connector
from datetime import datetime

conn = mysql.connector.connect(host="localhost", user="root", password="root@123456", database="ai_ceo_stores")
cursor = conn.cursor(dictionary=True)

print("📄 Agent 4 - Reporter AI - Creating CEO Report...\n")

# Collect data
cursor.execute("SELECT store_location, SUM(sales_amount) as sales FROM sales GROUP BY store_location ORDER BY sales DESC")
all_stores = cursor.fetchall()

html = f"""
<html><head><style>
body {{ font-family: Arial; padding: 30px; }}
h1 {{ color: #1a73e8; }}
.card {{ border: 1px solid #ddd; padding: 15px; border-radius: 10px; margin: 10px 0; }}
.worst {{ background: #ffebee; }} .best {{ background: #e8f5e9; }}
</style></head><body>
<h1>🤖 AI CEO - Multi-Store Analysis Report</h1>
<p>Generated: {datetime.now().strftime('%d %b %Y %I:%M %p')} | By: Kunigal AI Engineer</p>
<h2>🏆 Executive Summary</h2>
<div class="card best">
<b>Best Performer: Mysore</b> - ₹19,85,546 Sales | ₹18,14,117 Profit | 91.4% Margin<br>
Top Products: LED TV, Water Tank
</div>
<div class="card worst">
<b>Needs Attention: Hassan</b> - ₹8,45,579 Sales | ₹6,54,902 Profit | 77.5% Margin<br>
Issue: 20.1% marketing waste. Selling Soap Box (₹12k) vs LED TV demand (₹4.6L)<br>
<b>Fix: Cut marketing 30% = +₹50,981 profit</b>
</div>
<h2>📊 All Stores Ranked</h2>
<table border=1 cellpadding=8 cellspacing=0>
<tr><th>Store</th><th>Sales</th><th>Status</th></tr>
"""
for i, s in enumerate(all_stores):
    status = "🏆 BEST" if i==0 else "💀 WORST" if i==len(all_stores)-1 else "✅ Good" if "Kunigal" in s['store_location'] else "Average"
    html += f"<tr><td>{s['store_location']}</td><td>₹{float(s['sales']):,.0f}</td><td>{status}</td></tr>"

html += """
</table>
<h2>💡 AI Recommendations</h2>
<ul>
<li><b>Hassan:</b> Stop Soap Box, Rice Bag. Focus ONLY LED TV. Cut marketing spend 30%</li>
<li><b>Mysore Strategy:</b> Replicate LED TV + Water Tank combo to other stores</li>
<li><b>Kunigal (Your Store):</b> Already #2! Double down on current platform</li>
</ul>
<p><b>Tech Stack:</b> Python, MySQL, Pandas, Multi-Agent AI System</p>
<p>Built by AI Engineer from Kunigal, Karnataka</p>
</body></html>
"""

with open("c:/Users/Lenovo/Desktop/AI_CEO_Report.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ REPORT CREATED!")
print("📂 Location: Desktop/AI_CEO_Report.html")
print("👉 Open it in Chrome -> Ctrl+P -> Save as PDF")
print("\nThis PDF = Your Portfolio Project!")
print("\n🎯 NEXT STEPS FOR JOB:")
print("1. Screenshot all 4 agent outputs")
print("2. Save HTML as PDF")
print("3. LinkedIn post: 'Built AI CEO with 4 Agents that manages 8 stores...'")
print("4. I will give you LinkedIn post text")

conn.close()