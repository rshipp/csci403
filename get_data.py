#!/usr/bin/env python

import getpass
import pg8000
import datetime

def main():
    cursor, db = login()
    get_data(cursor, db)


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


def get_data(cursor, db):

    try:
        cursor.execute("""select s.road, s.fromroad, v.volume from
                segments as s, volume as v where v.datetime =
                '2013-03-03 01:00' group by s.road, s.fromroad, v.volume""")

        results = cursor.fetchall()
        with open('results.csv', 'w+') as f:
            for result in results:
                road, crossroad, volume = result
                f.write("{r},{c},{v}\n".format(r=road.strip(), c=crossroad.strip(), v=volume))

        db.commit()
        print("Done!")
    except pg8000.Error as e:
        print('Database error: ', e.args[2])
        db.rollback()


if __name__ == "__main__":
    main()

