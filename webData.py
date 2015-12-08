from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from database_setup import *
from sqlalchemy.orm import sessionmaker

DBSession = sessionmaker(bind = engine)
session = DBSession()

myFirstRestaurant = Restaurant(name = "Pizza Station")
session.add(myFirstRestaurant)
session.commit()
rets=session.query(Restaurant).all()
for r in rets:
	print r.name

print len(rets)