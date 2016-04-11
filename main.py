#!/usr/bin/env python3

# example.py
#
# CSCI 403 example Python script
#
# Author: C. Painter-Wakefield
# Modified: 10/31/2015
#
# This script does a couple of SELECT queries against tables in public, then
# creates a table and attempts some modification queries on it.  Examples are
# given of prepared queries using parameters, exception handling, and
# very basic input/output.

import getpass
import pg8000

def main():
    #cursor = login()
    cursor = None

    print_commands()
    while True:
        try:
            action = input("> ")
            if action == 's':
                action_search(cursor)
            elif action == 'i':
                action_insert(cursor)
            elif action == 'm':
                action_modify(cursor)
            elif action == 'd':
                action_delete(cursor)
            elif action == 'q':
                raise EOFError
            else:
                print("No such command: " + action)

        except EOFError:
            try:
                cursor.close()
                db.close()
            except Exception:
                pass
            exit()

def print_commands():
    print("Commands:")
    print("    s  -  search")
    print("    i  -  insert")
    print("    m  -  modify")
    print("    d  -  delete")
    print("    q  -  quit")

def login():
    login = input('login: ')
    secret = getpass.getpass('password: ')

    credentials = {'user'    : login,
                   'password': secret,
                   'database': 'csci403',
                   'host'    : 'flowers.mines.edu'}

    try:
        db = pg8000.connect(**credentials)
    except pg8000.Error as e:
        print('Database error: ', e.args[2])
        exit()

    # uncomment next line if you want every insert/update/delete to immediately
    # be applied; you can remove all db.commit() and db.rollback() statements
    #db.autocommit = True

    cursor = db.cursor()
    return cursor

def action_search(cursor):

    print("Search by:")
    print("    a  -  artist")
    print("    g  -  genre")
    print("    k  -  keyword")
    search_type = input("search type> ")
    while search_type not in ['a', 'g', 'k']:
        print("No such type: " + search_type)
        search_type = input("search type> ")

    if search_type == 'a':
        sql = """SELECT course_id, section, title
                 FROM mines_courses
                 WHERE instructor = 'Painter-Wakefield, Christopher'"""
    elif search_type == 'g':
        sql = """SELECT course_id, section, title
                 FROM mines_courses
                 WHERE instructor = 'Painter-Wakefield, Christopher'"""
    elif search_type == 'k':
        sql = """SELECT course_id, section, title
                 FROM mines_courses
                 WHERE instructor = 'Painter-Wakefield, Christopher'"""

    print("Search for?")
    query = input("search term> ")
    while not query:
        print("Can't be empty")
        query = input("search term> ")

    # immediate SELECT
    cursor.execute(sql)

    results = cursor.fetchall()
    for row in results:
        course_id, section, title = row
        print(course_id, section, title)
    print()

    # prepared SELECT
    faculty = input('Enter faculty as lastname, firstname: ')
    query = """SELECT course_id, section, title
               FROM mines_courses
               WHERE instructor LIKE %s"""

    cursor.execute(query, ('%%' + faculty + '%%',))

    results = cursor.fetchall()
    for row in results:
        course_id, section, title = row
        print(course_id, section, title)

    print_commands()


def action_modify(cursor):

    # DDL code
    query = "CREATE TABLE foo (x text PRIMARY KEY)"
    try:
        cursor.execute(query)
    except pg8000.Error as e:
        print('Database error: ', e.args[2])
        db.rollback() # necessary after error, unless autocommitting

    # modification queries with exception handling
    query = "INSERT INTO foo VALUES (%s)"
    try:
        cursor.execute(query, ('testing 1 2 3',))
        db.commit()
    except pg8000.Error as e:
        print('Database error: ', e.args[2])
        db.rollback() # necessary after error, unless autocommitting

    # second time should cause an integrity constraint violation
    try:
        cursor.execute(query, ('testing 1 2 3',))
        db.commit()
    except pg8000.Error as e:
        print('Database error: ', e.args[2])
        db.rollback() # necessary after error, unless autocommitting

    # bad SELECT query with exception handling
    query = "SELECT FROM foo WHERE blah = arg"
    try:
        cursor.execute(query)
    except pg8000.Error as e:
        print('Database error: ', e.args[2])


if __name__ == "__main__":
    main()
