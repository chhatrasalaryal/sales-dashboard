# Aggregates the 1M-row sales file into small cubes for the dashboard.
import pandas as pd, json, sys
src = sys.argv[1]
df = pd.read_csv(src)
df['od'] = pd.to_datetime(df['Order Date'], format='%m/%d/%Y')
df['sd'] = pd.to_datetime(df['Ship Date'], format='%m/%d/%Y')
df['ship_days'] = (df.sd - df.od).dt.days
df['month'] = df.od.dt.strftime('%Y-%m')
df['year'] = df.od.dt.year.astype(str)
code = open(__file__).read()
def agg(keys):
    g = df.groupby(keys).agg(orders=('Order ID', 'size'), units=('Units Sold', 'sum'),
        revenue=('Total Revenue', 'sum'), cost=('Total Cost', 'sum'), profit=('Total Profit', 'sum'),
        ship_days_sum=('ship_days', 'sum')).reset_index()
    for c in ['revenue', 'cost', 'profit']: g[c] = g[c].round(2)
    g = g.rename(columns={'Region': 'region', 'Item Type': 'item', 'Sales Channel': 'channel', 'Order Priority': 'priority', 'Country': 'country'})
    return g
meta = [{"label": "build.py", "value": code, "type": "code", "lang": "python"}, {"label": "Input", "value": "1000000_Sales_Records.csv (1,000,000 rows)"}]
for name, keys in {'cube': ['month', 'Region', 'Item Type', 'Sales Channel'],
                   'country': ['year', 'Region', 'Country']}.items():
    g = agg(keys)
    json.dump({"rows": g.to_dict('records'), "meta": meta}, open(f'{name}.json', 'w'), separators=(',', ':'))
    print(name, len(g))
dup = df['Order ID'].duplicated(keep=False)
print('dup order id rows', dup.sum(), 'full dup rows', df.drop(columns=['od','sd','ship_days','month','year']).duplicated().sum())
