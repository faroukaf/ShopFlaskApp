from market import db
from market.dbmodels import Item, User

db.session.create_all()

i1 = Item(
    name="IPhone",
    price=1000,
    barcode='11344re52fdd',
    description="good!"
)

db.session.add(i1)
db.session.commit()
