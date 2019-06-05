from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Base, CatItem, User
#engine = create_engine("postgresql+psycopg2://tstuser:tstpassword@localhost/test")
engine = create_engine("postgresql+psycopg2://catalog:udacity@localhost/catalog")
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Create dummy users
User1 = User(name="Robo Barista", email="tinnyTim@udacity.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)

User2 = User(name="John Smith", email="BigJohn@udacity.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User2)

session.commit()

# Menu for UrbanBurger
category1 = Category(user_id=1, name="Inkjet Printers")

session.add(category1)
session.commit()

CatItem2 = CatItem(user_id=1, name="HP Deskjet 3788", description="All in one A4 4800 dpi usb wi-fi color inkjet",
                     price="$67.50",
                     #course="Entree",
                     category=category1)

session.add(CatItem2)
session.commit()


CatItem1 = CatItem(user_id=2, name="HP Officejet 7110", description="15 ppm A3 usb wi-fi Inkjet",
                     price="$72.99", 
                     #course="Appetizer", 
                     category=category1)

session.add(CatItem1)
session.commit()

CatItem2 = CatItem(user_id=1, name="HP Deskjet Advantage 5075 AIO", description="10 PPM 4800DPI A4 USB WI-FI COLOR INKJET",
                     price="$55.50", 
                     #course="Entree", 
                     category=category1)

session.add(CatItem2)
session.commit()





CatItem7 = CatItem(user_id=1, name="HP Deskjet 2130",
                     description="7.5 ppm A4  usb 4800 dpi", price="$33.49", 
                     #course="Entree", 
                     category=category1)

session.add(CatItem7)
session.commit()

CatItem8 = CatItem(user_id=2, name="HP DESKJET 2630 AIO", description="7.5 PPM 4800 DPI A4 USB WI-FI",
                     price="$45.99", 
                     #course="Entree", 
                     category=category1)

session.add(CatItem8)
session.commit()


# Menu for Super Stir Fry
category2 = Category(user_id=2, name="SSD HARD DRIVE")

session.add(category2)
session.commit()

CatItem1 = CatItem(user_id=1, name="Pho", description="WD GREEN SSD 128GB ",
                     price="$50",category=category2)

session.add(CatItem1)
session.commit()




print ("added menu items!")
