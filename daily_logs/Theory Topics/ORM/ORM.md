### ORM

Django ORM
│
├── Models
├── Managers (objects)
├── QuerySets
├── Relationships
├── CRUD operations
├── Transactions
└── Database abstraction

- **ORM (Object-Relational Mapper)** is the whole system Django provides for working with databases.
- **QuerySet** is one part of the ORM. It's the object that represents a database query.

For example:

Portfolio.objects.filter(user=request.user)

Breaking it down:

Portfolio → Model
objects → Manager
filter() → Creates a QuerySet
The whole thing is using the Django ORM.

#### Mappings of each files
```
URL  ─────────────► View
View ─────────────► Serializer
Serializer ───────► Model
Model ────────────► Database
```

#### ORM roadmap (targeted)

We'll learn it in the order your project naturally needs it:

Phase 1 — Basics (some already done)
✅ objects
✅ all()
✅ get()
✅ filter()
✅ first()
create()
save()
delete()
Phase 2 — Relationships (very important)
ForeignKey
Reverse relationships
related_name
One-to-many navigation
select_related()
prefetch_related()

You'll definitely use these in your Portfolio ↔ TradeOrder models.

Phase 3 — Query optimization
values()
values_list()
order_by()
annotate()
aggregate()
Q objects
F expressions
Phase 4 — Advanced (later)
Transactions
Managers
Custom QuerySets
Signals (only if needed)