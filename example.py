#!/usr/bin/python3

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

# immediate SELECT
cursor.execute(
   """SELECT course_id, section, title 
      FROM mines_courses 
      WHERE instructor = 'Painter-Wakefield, Christopher'"""
)

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
 
cursor.close()
db.close()
 
