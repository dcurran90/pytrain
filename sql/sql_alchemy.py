from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

engine = create_engine('sqlite:///:memory:', echo=False)
# To see all sql all the time, change that False to True...
Base = declarative_base()
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String)
    # Explicit linking here to Mail_Address
    mail_addresses = relationship("Mail_Address",\
                                    backref='user',\
                                    cascade="all, delete, delete-orphan")
    def __init__(self, name, fullname, password):
        self.name = name
        self.fullname = fullname
        self.password = password
    def __repr__(self):
        return "<User('%s','%s', '%s')>" % (self.name, self.fullname, self.password)

class Mail_Address(Base):
    __tablename__ = 'mail_addresses'
    id = Column(Integer, primary_key=True)
    mailing_address = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String(2), nullable=False)
    zip_code = Column(Integer, nullable=False)
    # This is so SQLAlchemy knows how to join
    user_id = Column(Integer, ForeignKey('user.id'))
    def __init__(self, mailing_address, city, state, zip_code):
        self.mailing_address = mailing_address
        self.city = city
        self.state = state
        self.zip_code = int(zip_code)
    def __repr__(self):
        return "<Mail_Address('%s, %s %s %d'>" % (self.mailing_address,\
                                                      self.city,\
                                                      self.state,\
                                                      self.zip_code)

class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    # This is how sql alchemy links Address to User
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User", backref=backref('addresses', order_by=id))
    def __init__(self, email_address):
        self.email_address = email_address
    def __repr__(self):
        return "<Address('%s')>" % self.email_address

# This statement creates all the tables in the database
Base.metadata.create_all(engine) 


# This is how you interact with the sql engine
Session = sessionmaker(bind=engine)
session = Session()

# Let's make a basic user....
ed_user = User('ed', 'Ed Jones', 'edspassword')
session.add(ed_user)
our_user = session.query(User).filter_by(name='ed').first() 
print our_user

# you can add multiples like so:
session.add_all([
        User('wendy', 'Wendy Williams', 'wwilliams2012'),
        User('mary', 'Mary Contrary', 'xxg527'),
        User('fred', 'Fred Flinstone', 'barney stinks')])

# See here, ed changes his password. SQLAlchemy detects the change:
ed_user.password = 'f8s7ccs'
print "dirty:", session.dirty

# Also, there are all those new users hanging out in transaction limbo!
print "new:", session.new

# Save your changes
session.commit()


# Let's do some queries. The first one selects name and fullname where
# the name LIKE '%ed%'
print ["%s: %s" % (i.name, i.fullname) for i in session.query(User.name, User.fullname).filter(User.name.like('%ed%')).order_by(User.id)]


# This is the count of the previous statement
print session.query(User).filter(User.name.like('%ed')).count() 


# A new user appears! This time, he has email addresses
jack = User('jack', 'Jack Bean', 'gjffdd')
jack.addresses= [Address(email_address='jack@google.com'),
                 Address(email_address='j25@yahoo.com')]

session.add(jack)
session.commit()

# Now let's re-get him from the db:
jack = jack = session.query(User).filter_by(name='jack').one()
print "Jack's email:", jack.addresses


# Now that we have 2 tables, lets do some joins. This one is an
# implicit join statement. Also, isnt it nice how you can chain
# .filter()?
for u, a in session.query(User, Address).\
        filter(User.id==Address.user_id).\
        filter(Address.email_address=='jack@google.com').\
        all():
    print u, a

jack_again = session.query(User, Address).join(Address).\
    filter(Address.email_address=='jack@google.com').\
    one()

print jack_again

# Now lets give our old pal Ed a mailing_address!

ed = session.query(User).filter(User.name=='ed').one()
ed.mail_addresses = [Mail_Address('123 main st.', 'Arlen', 'TX', '73301'),\
                         Mail_Address('5000 Walzem', 'San Antonio', 'TX', '10101')]
[session.add(ad) for ad in ed.mail_addresses]
session.commit()


# Ed finished moving to to San Antonio because he got a job at Rackspace
session.delete(ed.mail_addresses[0])
session.commit()


# see, all gone.
print "address count should be 1:", session.query(Mail_Address).count()

# Turns out Ed didn't pass the background check and had to be terminated.
session.delete(ed)
session.commit()
print "no more mailing addresses:", session.query(Mail_Address).count()
