import aiosqlite
import sqlite3
from flask import jsonify


async def select_all():
    conn = await aiosqlite.connect('back/tm.db')
    conn.row_factory = aiosqlite.Row
    query = "with a as (" \
            "select id || ';' || dest || ';' || cargo as trip" \
            "     , ship_id " \
            "from trips" \
            ")" \
            "select id" \
            "     , name" \
            "     , type" \
            "     , group_concat(trip) as trips " \
            "from ships " \
            "left join a " \
            "on a.ship_id = id " \
            "group by id, name, type"
    cur = await conn.execute(query)
    ships = await cur.fetchall()
    await cur.close()
    await conn.close()
    return jsonify([{
        'shipID': ship['id'],
        'shipName': ship['name'],
        'shipType': ship['type'],
        'trips': [{
            'tripID': trip.split(';')[0],
            'dest': trip.split(';')[1],
            'cargo': trip.split(';')[2]
        } for trip in (ship['trips'].split(',') if ship['trips'] is not None else [])]
    } for ship in ships])


async def insert_ship(ship_dict):
    conn = await aiosqlite.connect('back/tm.db')
    await conn.execute('insert into ships values (:id, :name, :type)', ship_dict)
    await conn.commit()
    await conn.close()


async def insert_trip(trip_dict):
    conn = await aiosqlite.connect('back/tm.db')
    await conn.execute('insert into trips values (:id, :dest, :cargo, :ship_id)', trip_dict)
    await conn.commit()
    await conn.close()


async def delete_trip(params):
    conn = await aiosqlite.connect('back/tm.db')
    await conn.execute('delete from trips '
                       'where ship_id = :shipID '
                       'and id = :tripID', params)
    await conn.commit()
    await conn.close()


async def update_trip(params, ship_id, trip_id):
    conn = await aiosqlite.connect('back/tm.db')

    query = "update trips set {0} where id = :trip_id and ship_id = :r_ship_id".format(
        ', '.join([f"{key} = :{key}" for key in params]))
    params['trip_id'] = trip_id
    params['r_ship_id'] = ship_id

    await conn.execute(query, params)
    await conn.commit()
    await conn.close()

# ???????????????????????????? ????????????????????
if __name__ == '__main__':
    init = [
            {
                "shipID": 0,
                "shipName": "????????????",
                "shipType": "pass",
                "trips": [
                    {
                        "tripID": 0,
                        "dest": "??????????????",
                        "cargo": ""
                    },
                    {
                        "tripID": 1,
                        "dest": "????????????????",
                        "cargo": ""
                    }
                ]
            },
            {
                "shipID": 1,
                "shipName": "????????????????",
                "shipType": "cargo",
                "trips": [
                    {
                        "tripID": 2,
                        "dest": "??????????????????",
                        "cargo": "??????????????"
                    },
                    {
                        "tripID": 3,
                        "dest": "??????????????????",
                        "cargo": "??????????????"
                    }
                ]
            },
            {
                "shipID": 2,
                "shipName": "??????????????",
                "shipType": "pass",
                "trips": [
                ]
            }
        ]
    sconn = sqlite3.connect('back/tm.db')
    sconn.execute('delete from ships where 1 = 1')
    sconn.execute('delete from trips where 1 = 1')
    sconn.commit()
    query_ships = 'insert into ships values (?, ?, ?)'
    query_trips = 'insert into trips values (?, ?, ?, ?)'
    sships = []
    strips = []
    for sship in init:
        sships.append((sship['shipID'], sship['shipName'], sship['shipType']))
        for strip in sship['trips']:
            strips.append((strip['tripID'], strip['dest'], strip['cargo'], sship['shipID']))
    sconn.executemany(query_ships, sships)
    sconn.executemany(query_trips, strips)
    sconn.commit()
    sconn.close()
