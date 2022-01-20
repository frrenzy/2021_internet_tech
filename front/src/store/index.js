import Vue from 'vue';
import Vuex from 'vuex';

import api from '@/api/api';
import { cloneObject } from '@/helpers';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    ships: [],
  },

  getters: {
    getShipByID: state => id => state.ships.find(ship => ship.shipID === id),

    getTripByID: state => id => state.ships.find(ship => ship.shipID === id),

    getShips: state => state.ships,

    getFilteredShipsByType: state => shipType => state.ships.filter(ship => ship.shipType === shipType),
  },

  mutations: {
    setShips(state, ships) {
      state.ships = ships;
    },

    addShip(state, ship) {
      state.ships.push(ship);
    },

    addTrip(state, { trip, shipID }) {
      const currentShip = state.ships.find(ship => ship.shipID === shipID);
      currentShip.trips.push(trip);
    },

    updateTrip(state, { shipID, newTrip }) {
      const currentShip = state.ships.find(ship => ship.shipID === shipID);
      const currentTripIndex = currentShip.trips.findIndex(trip => trip.tripID === newTrip.tripID);

      currentShip.trips[currentTripIndex] = { ...newTrip };
    },

    changeTripShip(state, { currentShipID, newShipID, updatedTrip }) {
      const currentShip = state.ships.find(ship => ship.shipID === currentShipID);
      const removableTripIndex = currentShip.trips.findIndex(trip => trip.tripID === updatedTrip.tripID);

      // remove item from array: (itemIndex, numberOfRemovableItems)
      currentShip.trips.splice(removableTripIndex, 1);

      const newShip = state.ships.find(ship => ship.shipID === newShipID);
      newShip.trips.push(updatedTrip);
    },

    deleteTrip(state, { shipID, tripID }) {
      const currentShip = state.ships.find(ship => ship.shipID === shipID);
      const removableTripIndex = currentShip.trips.findIndex(trip => trip.tripID === tripID);

      // remove item from array: (itemIndex, numberOfRemovableItems)
      currentShip.trips.splice(removableTripIndex, 1);
    },
  },

  actions: {
    async getShips({ commit }) {
      try {
        const ships = await api.getShips();
        commit('setShips', ships);
      } catch (e) {
        console.error('Error:', e);
      }
    },

    async addShip({ commit }, ship) {
      await api.addShip(ship);

      commit('addShip', ship);
    },

    async addTrip({ commit }, { shipID, trip }) {
      await api.addTrip(shipID, trip);

      commit('addTrip', {
        trip: cloneObject(trip),
        shipID,
      });
    },

    async updateTrip({ commit }, { shipID, newTrip }) {
      await api.updateTrip(shipID, newTrip.tripID, newTrip);

      commit('updateTrip', {
        shipID,
        newTrip: cloneObject(newTrip),
      });
    },

    async changeTripShip({ commit }, { currentShipID, newShipID, updatedTrip }) {
      await api.changeTripShip(currentShipID, newShipID, updatedTrip.tripID);

      commit('changeTripShip', {
        currentShipID,
        newShipID,
        updatedTrip,
      });
    },

    async deleteTrip({ commit }, { shipID, tripID }) {
      await api.deleteTrip(shipID, tripID);

      commit('deleteTrip', {
        shipID,
        tripID,
      });
    },
  },
});
