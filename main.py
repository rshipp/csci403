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
    cursor, db = login()

    while True:
        print_commands()
        try:
            action = input("> ")
            if action == 's':
                action_search(cursor, db)
            elif action == 'i':
                action_insert(cursor, db)
            elif action == 'm':
                action_modify(cursor, db)
            elif action == 'd':
                action_delete(cursor, db)
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
    return cursor, db

def action_search(cursor, db):

    print("Search by:")
    print("    a  -  artist")
    print("    g  -  genre")
    print("    k  -  keyword")
    search_type = input("search type> ")
    while search_type not in ['a', 'g', 'k']:
        print("No such type: " + search_type)
        search_type = input("search type> ")

    if search_type == 'a':
        sql = """SELECT album.id, album.title, album.year, artist.name
                 FROM album, artist
                 WHERE lower(artist.name) like lower(%s) and
                       artist.id = album.artist_id
                 GROUP BY album.id, album.title, album.year, artist.name
                 ORDER BY album.id"""
    elif search_type == 'g':
        sql = """SELECT album.id, album.title, album.year, artist.name
                 FROM album, genre, album_genre, artist
                 WHERE lower(genre.genre) like lower(%s) and
                       album_genre.album_id = album.id and
                       album_genre.genre = genre.genre and
                       album.artist_id = artist.id
                 GROUP BY album.id, album.title, album.year, artist.name
                 ORDER BY album.id"""
    elif search_type == 'k':
        sql = """SELECT album.id, album.title, album.year, artist.name
                 FROM album, genre, album_genre, artist
                 WHERE (lower(genre.genre) like lower(%s) or
                        lower(album.title) like lower(%s) or
                        lower(artist.name) like lower(%s)) and
                       (album_genre.album_id = album.id and
                        album_genre.genre = genre.genre and
                        album.artist_id = artist.id)
                 GROUP BY album.id, album.title, album.year, artist.name
                 ORDER BY album.id"""

    print("Search for?")
    query = input("search term> ")
    while not query:
        print("Can't be empty")
        query = input("search term> ")

    # SELECT
    if search_type == 'k':
        cursor.execute(sql, ('%%' + query + '%%','%%' + query + '%%','%%' + query + '%%',))
    else:
        cursor.execute(sql, ('%%' + query + '%%',))

    results = cursor.fetchall()
    for row in results:
        album_id, title, year, artist = row
        print(album_id, '-', title, '(' + str(year) + ')', 'by', artist)
    print()

def action_delete(cursor, db):

    album_id = input("album id> ")
    while True:
        try:
            album_id = int(album_id)
            break
        except ValueError:
            print("Not a number: " + album_id)

    try:
        cursor.execute("""DELETE FROM album_genre
                WHERE album_genre.album_id = %s""", (album_id,))
        cursor.execute("""DELETE FROM album
                WHERE album.id = %s""", (album_id,))
        db.commit()
        print("Done!")
    except pg8000.Error as e:
        print('Database error: ', e.args[2])
        db.rollback()

def action_modify(cursor, db):

    album_id = input("album id> ")
    while True:
        try:
            album_id = int(album_id)
            break
        except ValueError:
            print("Not a number: " + album_id)


    try:
        cursor.execute("""SELECT album.id, album.title, album.year, artist.name
                     FROM album, artist
                     WHERE album.id = %s and
                           album.artist_id = artist.id""", (album_id,))
        results = cursor.fetchone()
        album_id, title, year, artist = results
        print(album_id, '-', title, '(' + str(year) + ')', 'by', artist)
    except pg8000.Error as e:
        print('Database error: ', e.args[2])

    # Title
    album_title = input("new album title> ")
    while not album_title:
        print("Can't be empty")
        album_title = input("new album title> ")
    # Artist
    print("Enter artist name First Last eg.: James Taylor")
    artist_id = None
    while artist_id is None:
        artist_name = input("new artist name> ")
        try:
            cursor.execute("""SELECT id
                         FROM artist
                         WHERE name = %s""", (artist_name,))
            results = cursor.fetchone()[0]
            artist_id = results
        except Exception:
            print("Bad artist name")
    # Year
    album_year = input("new album year> ")
    while not album_year:
        print("Can't be empty")
        album_year = input("new album year> ")
    # Genres
    print("Enter genres as a comma-separated list, eg.: rock,jazz")
    genre_list = input("new genre list> ")
    while not genre_list:
        print("Can't be empty")
        genre_list = input("new genre list> ")
    genres = [g.strip() for g in genre_list.split(',')]

    try:
        cursor.execute("""UPDATE album
                SET title = %s,
                    artist_id = %s,
                    year = %s
                WHERE id = %s""", (album_title, artist_id, album_year, album_id,))
        cursor.execute("""DELETE FROM album_genre
                WHERE album_id = %s""", (album_id,))
        for genre in genres:
            cursor.execute("""INSERT INTO album_genre
                    (album_id, genre)
                    VALUES (%s, %s)""", (album_id, genre,))
        db.commit()
        print("Done!")
    except pg8000.Error as e:
        print('Database error: ', e.args[2])
        print("Probably a bad genre list")
        print("Try again?")
        db.rollback()

def example():

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
