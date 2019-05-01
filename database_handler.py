#!/usr/bin/env python3

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DatabaseHandler():
    """A class used for handling database operations"""
    #Base class for tables
    Base = declarative_base()
    #Account class for tables
    class Account(Base):
        """An account in the database."""
        __tablename__ = 'account'
        id = Column(Integer, primary_key=True)
        site = Column(String)
        username = Column(String)
        password = Column(String)

        def __repr__(self):
            return "<Account(site='{}', username='{}', password='{}')>".\
                format(self.site, self.username, self.password)

    #Password class for tables
    class Password(Base):
        """A password in the database."""
        __tablename__ = 'password'
        id = Column(Integer, primary_key=True)
        password = Column(String)

    def __init__(self):
        """Initialize the database handler"""
        self.engine = create_engine('sqlite:///account_database.db')
        self.Base.metadata.bind = self.engine
        self.DBSession = sessionmaker(bind = self.engine) 
        self.session = self.DBSession()

    def create_database(self):
        """Creates an sqlite database""" 
        self.Base.metadata.create_all(self.engine)
    #database manipulation
    def insert_data(self, site: str, username: str, password: str):
        """Inserts the site, username, and password into the database"""
        self.session.add(self.Account(site=site, username=username, password=password))
        self.session.commit()

    def query_database(self, site: str = None, username: str = None):
        """Return a dictionary of queries given the site, and or username.
        Input no arguments, site, or site and username"""
        results = {}
        if site is None and username is None:
            query_all = self.session.query(self.Account).all()
            sites = sorted({x.site for x in query_all})
            for item in sites:
                query = self.session.query(self.Account).filter(self.Account.site == item)
                results[item] = [x for x in query]
            return results
        elif site is not None and username is None:
            query = self.session.query(self.Account).\
                filter(self.Account.site.like("%{}%".format(site)))
        elif site is None and username is not None:
            query = self.session.query(self.Account).filter(self.Account.username == username)
        else:
            query = self.session.query(self.Account).\
                filter(self.Account.site == site).filter(self.Account.username == username)
        queries = [x for x in query]
        for instance in queries:
            if instance.site not in results:
                results[instance.site] = [instance]
            else:
                results[instance.site].append(instance)
        return results

    def update_item(self, site: str, username: str, new_password: str):
        """Update the row with site and username with the new_password"""
        query = self.session.query(self.Account).filter(self.Account.site == site).\
            filter(self.Account.username == username)
        query[0].password = new_password
        self.session.commit()

    def drop_tables(self):
        """Drop all tables in the database"""
        self.session.query(self.Account).delete()
        self.session.commit()

    def delete_row(self, site: str, username: str):
        """Delete the row in the database with site and username"""
        self.session.query(self.Account).filter(self.Account.site == site).\
            filter(self.Account.username == username).delete()
        self.session.commit()
    #password
    def set_password(self, password: str):
        """Add password to the password table"""
        self.session.add(self.Password(password=password))
        self.session.commit()

    def retrieve_password(self):
        """Return a string representing the password retrieved from the password table"""
        query = self.session.query(self.Password).all()
        return query[0].password
