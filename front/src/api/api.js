const baseUrl = ' http://127.0.0.1:5000';

export default {
  getShips: async () => {
    const res = await fetch(`${baseUrl}/ships`);
    const data = await res.json();
    return data;
  },

  addShip: async ship => {
    await fetch(`${baseUrl}/ships`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(ship),
    });
  },

  addTrip: async (shipID, trip) => {
    await fetch(`${baseUrl}/ships/${shipID}/trips`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(trip),
    });
  },

  updateTrip: async (shipID, tripID, trip) => {
    await fetch(`${baseUrl}/ships/${shipID}/trips/${tripID}`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        dest: trip.dest,
        cargo: trip.cargo,
      }),
    });
  },

  deleteTrip: async (shipID, tripID) => {
    await fetch(`${baseUrl}/ships/${shipID}/trips/${tripID}`, {
      method: 'DELETE',
    });
  },

  changeTripShip: async (oldShipID, newShipID, tripID) => {
    const idData = {
      to_shipID: newShipID,
      tripID,
    };

    await fetch(`${baseUrl}/ships/${oldShipID}`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(idData),
    });
  },
};
