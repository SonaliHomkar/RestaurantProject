from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base,Restaurant,MenuItem

engine = create_engine('sqlite:///restaurantNew.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

#Create a new Entry in Restaurant table

myFirstRestaurant = Restaurant(name = "Naturals")
session.add(myFirstRestaurant)
session.commit()

#Create a new Entry in MenuItem table

cheesepizza = MenuItem(name = "Spinach Ice Cream Burger",description="Made with all natural ingredients",
                       course="Dessert",price="$4.99",restaurant=myFirstRestaurant)
session.query(Restaurant).all()
session.add(cheesepizza)
session.commit()




# read first entry from Restaurant
firstResult = session.query(Restaurant).first()
print "Name :" + firstResult.name

# Read all entries from MenuItem
items = session.query(MenuItem).all()
for item in items:
    print item.name
    print item.description
    print item.course
    print item.price
    
    
print "done"
