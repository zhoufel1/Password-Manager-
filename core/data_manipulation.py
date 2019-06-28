import os
import bcrypt
import time
import passwords
import encryption as enc
import pyperclip as clip
import dynamic_search as ds
import getpass as gp
import database as db


def create_database(database: db.Database) -> bool:
    if not os.path.exists('./account_database.db'):
        print("Creating account database...")
        database.create_database()
        return False
    print("Accessing database...")
    return True


def handle_password(trigger: bool, database: db.Database) -> str:
    if trigger:
        entry = gp.getpass("Enter your password: ")
        if not bcrypt.checkpw(entry.encode(),
                              database.retrieve_password()):
            raise Exception("Incorrect password")
        return entry

    while True:
        first_entry = gp.getpass("Enter a password for database: ")
        second_entry = gp.getpass("Re-enter the password: ")
        if first_entry == second_entry:
            database.set_password(enc.hash_password(first_entry))
            return first_entry

        os.system('clear')
        print("*Passwords do not match*")
        time.sleep(1)
        os.system('clear')


def show_search(database: db.Database, key: bytes) -> None:
    if ds.check_database_empty(database):
        return None
    else:
        search_result = ds.user_enter_query(database)
        if search_result == '\x1b':
            return None
        results = ds.fuzzy_search(search_result, database)
        op = ds.build_menu_options(results)
        if len(op) == 1:
            clip.copy(enc.decrypt_password(op[1].password, key))
        else:
            os.system('tput cnorm')
            while True:
                u_input = input("Enter option: ").strip()
                if u_input.isnumeric() and int(u_input) <= len(op):
                    pw = enc.decrypt_password(op[int(u_input)].password, key)
                    clip.copy(pw)
                    break

        os.system('clear')
        print("Password copied")
        time.sleep(1)
        os.system('tput civis')


def show_all(database: db.Database, key: bytes) -> None:
    queries = database.query_all_entries()
    if not queries:
        print("No items found\n")
    else:
        print("\n━━━━━━━━━━━━Account Info━━━━━━━━━━━━")
        for site in queries:
            print("*** " + site + ":")
            for item in queries[site]:
                print(item.username, enc.decrypt_password(item.password, key))
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")


def input_data(database: db.Database, key: bytes) -> None:
    os.system('tput cnorm')
    site = input("\nEnter site: ").lower().strip(" ")
    username = input("Enter username: ").lower().strip(" ")

    if database.query_site_and_user(site, username) != {}:
        os.system('clear')
        print("*Item already exists*")
        time.sleep(1)
    else:
        while True:
            length = input("Password length? ")
            if length.isnumeric():
                password = passwords.generate_password(int(length))
                database.insert_data(site,
                                     username,
                                     enc.encrypt_password(password,
                                                          key))
                clip.copy(password)
                os.system('clear')
                print("Password copied!")
                time.sleep(1)
                os.system('tput civis')
                return None


def input_existing_data(database: db.Database, key: bytes) -> None:
    os.system('tput cnorm')
    site = input("\nEnter site: ").lower().strip(" ")
    username = input("Enter username: ").lower().strip(" ")
    password = input("Enter password: ")

    if database.query_site_and_user(site, username) != {}:
        os.system('clear')
        print("*Item already exists*")
        time.sleep(1)
    else:
        database.insert_data(site,
                             username,
                             enc.encrypt_password(password, key))
        os.system('clear')
        print("Account information stored")
        time.sleep(1)
    os.system('tput civis')


def update_data(database: db.Database, key: bytes) -> None:
    if ds.check_database_empty(database):
        return None
    else:
        os.system('tput cnorm')
        search_result = ds.user_enter_query(database)
        if search_result == '\x1b':
            return None
        results = ds.fuzzy_search(search_result, database)
        op = ds.build_menu_options(results)
        if len(op) == 1:
            selection = op[1]
        else:
            while True:
                u_input = input("Enter option: ").strip()
                if u_input.isnumeric() and int(u_input) <= len(op):
                    selection = op[int(u_input)]
                    break
        password = passwords.generate_password(int(input("Length? ")))
        new_password = enc.encrypt_password(password, key)
        database.update_item(selection.site,
                             selection.username,
                             new_password)
        os.system('clear')
        print("Password copied")
        time.sleep(1)
        os.system('tput civis')


def delete_data(database: db.Database) -> None:
    if ds.check_database_empty(database):
        return None
    else:
        os.system('tput cnorm')
        search_result = ds.user_enter_query(database)
        if search_result == '\x1b':
            return None
        results = ds.fuzzy_search(search_result, database)
        op = ds.build_menu_options(results)
        if len(op) == 1:
            selection = op[1]
        else:
            while True:
                u_input = input("Enter option: ").strip()
                if u_input.isnumeric() and int(u_input) <= len(op):
                    selection = op[int(u_input)]
                    break
        os.system('clear')
        database.delete_row(selection.site,
                            selection.username)
        print("Account info deleted")
        time.sleep(1)
        os.system('tput civis')


def delete_all(database: db.Database) -> None:
    password = gp.getpass("You are about to wipe account info. " +
                          "Enter password to confirm: ")
    os.system('clear')
    if not bcrypt.checkpw(password.encode(),
                          database.retrieve_password()):
        print("*Password incorrect. Aborted*")
        time.sleep(1)
    else:
        database.drop_tables()
        print("All account information deleted")
        input("\nPress Enter to continue...")
