# Sales performance dashboard

Interactive dashboard of the synthetic "1,000,000 Sales Records" sample dataset (orders from January 2010 to July 2017).

Live page: https://chhatrasalaryal.github.io/sales-dashboard/

- `index.html` – the dashboard (D3, no build step)
- `data/cube.json` – sales summed by month, region, item type and channel
- `data/country.json` – sales summed by year, region and country
- `build.py` – script that makes the two data files from the original CSV:
  `python3 build.py 1000000_Sales_Records.csv`
