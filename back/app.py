from db import *
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)


@app.route('/ships', methods=['GET'])
async def get_all():
    response = await select_all()
    return response


@app.route('/ships', methods=['POST'])
async def add_ship():
    ship_dict = {
        'id': request.json['shipID'],
        'name': request.json['shipName'],
        'type': request.json['shipType']
    }
    await insert_ship(ship_dict)
    return jsonify({"Info": "added"})


@app.route('/ships/<shipID>/trips', methods=['POST'])
async def add_trip(shipID):
    trip_dict = {
        'id': request.json['tripID'],
        'dest': request.json['dest'],
        'cargo': request.json['cargo'],
        'ship_id': shipID
    }
    await insert_trip(trip_dict)
    response = jsonify({'info': f'Trip {trip_dict} was successfully added'})
    return response


@app.route('/ships/<shipID>/trips/<tripID>', methods=['DELETE'])
async def remove_trip(shipID, tripID):
    await delete_trip({'shipID': shipID,
                       'tripID': tripID})
    response = jsonify({'info': f"Task was successfully deleted"})
    return response


@app.route('/ships/<shipID>/trips/<tripID>', methods=['PATCH'])
async def modify_trip(shipID, tripID):
    params = request.json
    await update_trip(params, shipID, tripID)
    response = jsonify({'info': f"Task was successfully updated"})
    return response


@app.route('/ships/<from_shipID>', methods=['PATCH'])
async def move_trip(from_shipID):
    await update_trip({'ship_id': request.json['to_shipID']}, from_shipID, request.json['tripID'])
    response = jsonify({'info': f"Task was successfully moved"})
    return response


if __name__ == '__main__':
    app.run()
