**New fields in TradeOrder model**
- new TradeOrder model has asset_id and user_id fields added and set `null=True`
user — directly identifies the user who owns the order.
asset — links the order to an Asset record.
- migrate new models, that create migration file `0003_...py`, changing schema without affecting data.

- Verify if the new fields asset_id and user_id in model added has value `None`
```powershell
>>> from trade_app.models import Portfolio, TradeOrder, Asset
>>> Portfolio.objects.count()
25
>>> TradeOrder.objects.count()
15
>>> list(TradeOrder.objects.values("order_id", "symbol", "portfolio_id", "user_id", "asset_id")) 
[{'order_id': 2, 'symbol': 'AAPL', 'portfolio_id': 8, 'user_id': None, 'asset_id': None}, {'order_id': 3, 'symbol': 'META', 'portfolio_id': 12, 'user_id': None, 'asset_id': None}, {'order_id':ymbol': 'MSFT', 'portfolio_id': 7, 'user_id': None, 'asset_id': None}, {'order_id': 6, 'symbol': 'NFLX', 'portfolio_id': 6, 'user_id': None, 'asset_id': None}, {'order_id': 7, 'symbol': 'TSLA', 'portfolio_id': 15, 'user_id': None, 'asset_id': None}, .....]
```


***Add new Models***
- added new models and changed some model fields
| Model       |	Purpose	                            | 
|-------------|-------------------------------------| 
| Asset	      | Stock or ETF being traded           |   
| Trade       |	Actual order execution	            |  
| Holdings	  | Current assets owned in a portfolio |  
| LedgerEntry	| Cash debit/credit records	          |  
 
if we migrate new models, plausibly lose the data. 
we need to create backup file before migrating and perform data migration to retrieve data.

**Data Migration**
1) Backup Existing Data
- creating backup of existing data file `backend project/db.sqlite3` manually

2) Creating empty data migration
```powershell
(venv) PS ..\python\backend project> python manage.py makemigrations trade_app --empty --name backfill_order_owner_and_asset
Migrations for 'trade_app':
  trade_app\migrations\0004_backfill_order_owner_and_asset.py
```
CLI description:
- `makemigrations` creates migration files.
- `--empty` creates a migration without automatically generated database operations.
- `--name` gives the migration a meaningful name.

`0004_backfill_order_owner_and_asset.py` file created 

3) Added function `backfill_order_owner_and_asset`which for every existing order:
- Retrieves its associated portfolio.
- Gets the portfolio owner's user ID.
- Finds or creates an Asset using the order's existing symbol.
- Assigns the owner to order.user_id.
- Assigns the asset to order.asset_id.
- Saves only those two updated fields.

`get_or_create()` is important because multiple orders can refer to the same asset. We want one Asset record per unique symbol, rather than creating duplicates.

Why apps.get_model() instead of importing models directly?
Migrations should use the historical model definitions associated with that point in the migration history. This helps migrations continue to work even when the current application models change later.

4) Apply Data migration
Migration applies n run backfill function
```powershell
(venv) PS ..\python\backend project> python .\manage.py migrate trade_app                       
Operations to perform:      
  Apply all migrations: trade_app
Running migrations:
  Applying trade_app.0004_backfill_order_owner_and_asset... OK
```

5) Verify migration:
```powershell
>>> from trade_app.models import TradeOrder, Asset
# Verify if user is null
>>> TradeOrder.objects.filter(user__isnull=True).count()
0
# Verify if asset is null
>>> TradeOrder.objects.filter(asset__isnull=True).count()
0
# asset count
>>> Asset.objects.count()
12
# match the asset symbol with old symbols
>>> all(    order.symbol == order.asset.symbol and order.user_id == order.portfolio.user_id  
  for order in orders)
True
```

*Result:* All 15 existing orders were successfully backfilled and verified. We had 12 unique Asset records.

***Key learning:***
Concept         | Purpose
----------------|-------------------------------------------------
Database backup | Protect existing database data
Schema migration| Change database structure
Data migration  | Update existing records
RunPython       | Execute custom Python logic during a migration
migrate         |Apply pending migrations

**Why we did this:** We needed to preserve existing orders while changing the database relationships. We populated the new fields first so that we could safely remove the old symbol field and make the new relationships mandatory.

**Summarizing Data Migration Steps:**
Step	| Command/action	      | Purpose
------|-----------------------|--------------------
1	    | Copy db.sqlite3	      | Backup
2	    | makemigrations --empty| Create blank migration
3	    | Edit 0004...py	      | Write backfill logic
4	    | migrate trade_app	    | Execute migration
5	    | Django shell checks	  | Verify data

**key distinction:** A *schema migration* adds the columns; a *data migration* fills them with meaningful values.