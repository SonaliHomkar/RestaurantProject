from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base,Restaurant,MenuItem


engine = create_engine('sqlite:///restaurantNew.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


spinach = session.query(MenuItem).filter_by(name='Spinach Ice Cream').one()
print "name : " +  spinach.name
print spinach.id
print spinach.description
print spinach.course
print spinach.price

session.delete(spinach)
session.commit

spinach = session.query(MenuItem).filter_by(name='Spinach Ice Cream').one()
