# https://www.youtube.com/watch?v=AKQ3XEDI9Mw

from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pathlib import Path

script_dir = Path(__file__).parent
DATABASE = script_dir / "database" / "mydb.db"

Base = declarative_base()

class Person(Base):
  __tablename__ = "people"

  ssn = Column("ssn", Integer, primary_key=True)
  firstname = Column("firstname", String)
  lastname = Column("lastname", String)
  gender = Column("gender", CHAR)
  age = Column("age", Integer)

  def __init__(self, ssn, first, last, gender, age):
    self.ssn = ssn
    self.firstname = first
    self.lastname = last
    self.gender = gender
    self.age = age

  def __repr__(self):
    return f"({self.ssn}) {self.firstname} {self.lastname} ({self.gender}, {self.age})"

class Thing(Base):
  __tablename__ = "things"

  tid = Column("tid", Integer, primary_key=True)
  description = Column("description", String)
  owner = Column(Integer, ForeignKey("people.ssn"))

  def __init__(self, tid, description, owner):
    self.tid = tid
    self.description = description
    self.owner = owner

  def __repr__(self):
    return f"({self.tid}) {self.description} owned by {self.owner}"

engine = create_engine(f"sqlite:///{DATABASE}", echo=True)
Session = sessionmaker(bind=engine)
session = Session()

def initialize_database(session):
  Base.metadata.create_all(bind=engine)

  persons = session.get(Person, 12342)
  if persons is None:
    person = Person(12342, "Mike", "Smith", "m", 35)
    session.add(person)
    session.commit()

    p1 = Person(12343, "Mark", "Smitty", "m", 31)
    p2 = Person(12344, "Anna", "Smidly", "f", 32)
    p3 = Person(12345, "Bob", "Snider", "m", 33)
    session.add(p1)
    session.add(p2)
    session.add(p3)
    session.commit()

  things = session.get(Thing, 1)
  if things is None:
    t1 = Thing(1, "Car", p1.ssn)
    session.add(t1)
    t2 = Thing(2, "Laptop", p1.ssn)
    session.add(t2)
    t3 = Thing(3, "PS5", p2.ssn)
    session.add(t3)
    t4 = Thing(4, "Tool", p3.ssn)
    session.add(t4)
    t5 = Thing(5, "Book", p3.ssn)
    session.add(t5)
    session.commit()

if __name__ == '__main__':
  initialize_database(session)

# results = session.query(Person).all()
# results = session.query(Person).filter(Person.age > "25")
# results = session.query(Person).filter(Person.firstname.like("%M%"))
# results = session.query(Person).filter(Person.firstname.in_(["Anna", "Mark"]))

results = session.query(Thing, Person).filter(Thing.owner == Person.ssn).filter(Person.firstname == "Anna").all()
for r in results:
  print(r)

# using the Sqlite Viewer extension in VSCode to view database
# (.venv)
# activate and install dependencies
# python -m training.sqlalchemy.person
