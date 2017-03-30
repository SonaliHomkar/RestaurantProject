from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base,Restaurant,MenuItem


engine = create_engine('sqlite:///restaurantNew.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

veggiBurgers = session.query(MenuItem).filter_by(name='Veggi Burger')
for veggiBurger in veggiBurgers:
    print veggiBurger.id
    print veggiBurger.name
    print veggiBurger.restaurant.name
    print "\n"
    
BurgerKings = session.query(MenuItem).filter_by(id=7).one()
print BurgerKings.price

BurgerKings.price = '$2.00'
session.add(BurgerKings)
session.commit()

print "New price : "  + BurgerKings.price


veggiBurgers = session.query(MenuItem).filter_by(name='Veggi Burger')


for veggiBurger in veggiBurgers:
    print "old price"
    print veggiBurger.id
    print veggiBurger.name
    print veggiBurger.restaurant.name
    print veggiBurger.price
    print "\n"

for veggiBurger in veggiBurgers:
    if veggiBurger.price!='$2.00':
        veggiBurger.price = '$2.00'
        session.add(veggiBurger)
        session.commit()
        


for veggiBurger in veggiBurgers:
    print "New price"
    print veggiBurger.id
    print veggiBurger.name
    print veggiBurger.restaurant.name
    print veggiBurger.price
    print "\n"
