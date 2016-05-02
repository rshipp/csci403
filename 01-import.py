#!/usr/bin/env python3

import getpass
import pg8000
import datetime

def main():
    cursor, db = login()
    import_data(cursor, db)


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


def import_data(cursor, db):


    try:
        with open('data.csv', 'r+') as f:
            csv = f.read().strip().split('\n')

            times = [t.split('-')[1] for t in csv[0].split(',')[7:]]
            rows = csv[1:]

            for row in rows:
                print(row)
                _, segmentid, road, fromroad, toroad, direction, date, *volumes = row.split(',')

                cursor.execute("""SELECT *
                             FROM segments
                             WHERE segment_id = %s and
                                   road = %s and
                                   fromroad = %s and
                                   toroad = %s and
                                   direction = %s""", (segmentid, road,
                                       fromroad, toroad, direction,))

                results = cursor.fetchone()
                if not results:
                    cursor.execute("""INSERT INTO segments
                                 (segment_id, road, fromroad, toroad, direction)
                                 VALUES (%s, %s, %s, %s, %s)""", (segmentid, road,
                                           fromroad, toroad, direction,))

                cursor.execute("""SELECT id
                             FROM segments
                             WHERE segment_id = %s and
                                   road = %s and
                                   fromroad = %s and
                                   toroad = %s and
                                   direction = %s""", (segmentid, road,
                                       fromroad, toroad, direction,))
                fkey_id = cursor.fetchone()[0]

                for i, time in enumerate(times):
                    # insert into volume (segmentid, (date+time), volume)
                    cursor.execute("""INSERT INTO volume
                                 (segment_id, datetime, volume)
                                 VALUES (%s, %s, %s)""", (fkey_id, ' '.join([date, time]),
                                           volumes[i],))

        db.commit()
        print("Done!")
    except pg8000.Error as e:
        print('Database error: ', e.args[2])
        db.rollback()


if __name__ == "__main__":
    main()
