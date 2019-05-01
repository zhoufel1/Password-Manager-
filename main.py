#!/usr/bin/env python3

import os
from getpass import getpass
import database_handler as db
from encryption import key_generator, encrypt_password, decrypt_password, hash_password
from passgen import Passgen
from bcrypt import checkpw


def run():
    """Initialize the program"""
    #Create database handler object
    database_handler = db.DatabaseHandler()

    print("======================Password Manager v1.1.1======================")

    #Handle password entry
    trigger = handle_database_input(database_handler)
    key = key_generator(handle_password(trigger, database_handler))
    #Initialize menu options
    user_input = input("\nOptions:\n" + "1. Show entries\n" + "2. Add new entry\n" +
                       "3. Update existing entry\n" + "4. Delete existing entry\n" +
                       "5. Reset database\n" + "6. Exit\n")
    while True:
        if user_input == "1":
            search_input = input("\nOptions:\n" + "1. Search by site\n" +
                                 "2. Search by username\n" + "3. Show all\n")
            if search_input == '1':
                show_selected_site(database_handler, key)
            elif search_input == '2':
                show_selected_username(database_handler, key)
            elif search_input == '3':
                show_all_data(database_handler, key)
        elif user_input == "2":
            handle_data_input(database_handler, key)
        elif user_input == "3":
            handle_row_update(database_handler, key)
        elif user_input == "4":
            handle_row_delete(database_handler, key)
        elif user_input == "5":
            handle_table_delete(database_handler)
        elif user_input == "6":
            #Terminates the program
            return 0
        user_input = input("\nOptions:\n" + "1. Show entries\n" + "2. Add new entry\n" +
                           "3. Update existing entry\n" + "4. Delete existing entry\n" +
                           "5. Reset database\n" + "6. Exit\n")

#Helpers
def handle_database_input(database_handler):
    """Return True if the database already exist. If not, create the database and return False"""
    if not os.path.exists('./account_database.db'):
        print("Creating account database...")
        database_handler.create_database()
        return False 
    else:
        print("Accessing database...")
        return True
    

def handle_password(trigger: bool, database_handler):
    """Return the user-inputted password as a string. If database is already created, check the 
    inputted password with database password. Otherwise, prompt user to create a password for database"""
    if trigger:
        p_input = getpass("Enter your password: ")
        if not checkpw(p_input, database_handler.retrieve_password()):
            raise Exception("Incorrect password")
    else:
        while True:
            p_input = getpass("Enter a password for database: ")
            p_input1 = getpass("Re-enter the password: ")
            if p_input == p_input1:    
                database_handler.set_password(hash_password(p_input))
                break 
            print("*Passwords do not match*")
    return p_input


def show_selected_site(database_handler, key: bytes):
    """Prompt the user to enter a site and print all account information 
    associated with that site"""
    site_input = input("\nEnter site: ").lower().strip(" ")
    queries = database_handler.query_database(site_input, None)
    if len(queries) == 0:
        print("*Info not found*")
    else:
        print("\n============Account Info============")
        for site in queries.keys():
            print("*** " + site + ":")
            for item in queries[site]:
                print(item.username, decrypt_password(item.password, key))
    print("====================================")


def show_selected_username(database_handler, key: bytes):
    """Prompt the user to enter a site and print all account information 
    associated with that site"""
    user_input = input("\nEnter username: ").lower().strip(" ")
    queries = database_handler.query_database(None, user_input)
    if len(queries) == 0:
        print("*Info not found*")
    else:
        print("\n============Account Info============")
        for site in queries:
            for item in queries[site]:
                if item.username == user_input:
                    print("*** " + site + ":")
                    print(item.username, decrypt_password(item.password, key))        
    print("====================================")


def show_all_data(database_handler, key: bytes):   
    """Print all account information in the database"""
    queries = database_handler.query_database()
    print("\n============Account Info============")
    for site in queries:
        print("*** " + site + ":")
        for item in queries[site]:
            print(item.username, decrypt_password(item.password, key))    
    print("====================================")


def handle_data_input(database_handler, key: bytes):
    """Prompts the user to enter account information and store it into the Account table 
    in database as a row""" 
    site = input("\nEnter site: ").lower().strip(" ")
    username = input("Enter username: ").lower().strip(" ")
    if len(database_handler.query_database(site, username)) != 0:
        print("*Item already exists*")
    else:
        try:
            length = input("Password length? ")
            password = Passgen(int(length)).gen_password()
            database_handler.insert_data(site, username, encrypt_password(password, key))
            print(password)
        except:
            print("Invalid entry")    


def handle_row_update(database_handler, key: bytes):
    """Prompts the user to enter account information to update that row 
    with a new generated password"""
    site = input("\nEnter site: ").lower().strip(" ")
    username = input("Enter username: ").lower().strip(" ")
    if len(database_handler.query_database(site, username)) == 0:
        print("*Item not found*")
    else:
        length = input("Length? ")
        password = Passgen(int(length)).gen_password()
        new_password = encrypt_password(password, key)
        database_handler.update_item(site, username, new_password)
        print(password)


def handle_row_delete(database_handler, key: bytes):
    site = input("\nEnter site: ").lower().strip(" ")
    username = input("Enter username: ").lower().strip(" ")
    if len(database_handler.query_database(site, username)) == 0:
        print("*Item not found*")
    else:
        print("*Account info deleted*")
        database_handler.delete_row(site, username) 
    
    
def handle_table_delete(database_handler):
    password = getpass("You are about to wipe account info. Enter password to confirm: ")
    if not checkpw(password, database_handler.retrieve_password()):
        print("*Password incorrect. Aborted*")
    else:
        print("Dropping table...")
        database_handler.drop_tables()


if __name__ == "__main__":
    run()
