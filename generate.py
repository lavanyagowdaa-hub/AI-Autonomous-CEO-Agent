import pandas as pd, numpy as np, os
from datetime import datetime, timedelta
np.random.seed(42)
desktop = os.path.join(os.path.expanduser("~"), "Desktop")
stores = ["Kunigal","Tumkur","Bangalore-Indiranagar","Bangalore-Koramangala","Mysore","Mandya","Hassan","Chitradurga","Davangere","Shimoga"]
platforms = ["Instagram","Google Ads","Local Banner","Whatsapp"]
issues = ["Delivery Delay","Damaged Product","Payment Failed","Stock Out","Return Request"]

m=[]
for i in range(1,201):
    m.append([i, stores[np.random.randint(0,10)], platforms[np.random.randint(0,4)], np.random.randint(500,15001), (datetime(2024,1,1)+timedelta(days=int(np.random.randint(0,601)))).date()])
pd.DataFrame(m, columns=["spend_id","store_location","platform","spend_amount","spend_date"]).to_csv(os.path.join(desktop,"marketing.csv"), index=False)

sup=[]
for i in range(1,151):
    sup.append([i, stores[np.random.randint(0,10)], issues[np.random.randint(0,5)], np.random.randint(100,2001), (datetime(2024,1,1)+timedelta(days=int(np.random.randint(0,601)))).date()])
pd.DataFrame(sup, columns=["ticket_id","store_location","issue_type","resolution_cost","ticket_date"]).to_csv(os.path.join(desktop,"support.csv"), index=False)
print("marketing.csv and support.csv also on Desktop now")