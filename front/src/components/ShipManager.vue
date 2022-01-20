<template>
  <div class="ships-manager">
    <ElCard
      class="box-card ship-card"
      v-for="(ship, shipKey) in ships"
      :key="shipKey"
    >
      <div
        slot="header"
        class="card-header"
      >
        <div class="ship-name">{{ ship.shipName }}</div>
        <div class="ship-type">{{ shipType(ship.shipType) }}</div>
      </div>
      <div
        v-if="!ship.trips.length"
        class="ship-trips-empty"
      >
        Нет рейсов
      </div>

      <ul
        v-else
        class="ship-trips"
      >
        <li
          class="trip"
          v-for="(trip, tripKey) in ship.trips"
          :key="tripKey"
        >
          <div class="trip-info">
            <div class="trip-dest"><span>Точка назначения:</span><br> {{ trip.dest }}</div>
            <div v-if="ship.shipType === 'cargo'" class="trip-cargo"><span>Груз:</span><br> {{ trip.cargo }}</div>
          </div>

          <ElButton @click="changeShip(ship.shipID, trip.tripID)">
            Настройки рейса <i class="el-icon-s-tools el-icon-right"></i>
          </ElButton>
        </li>
      </ul>
      <ElButton @click="showTripDialog(ship.shipID)">
        Добавить рейс <i class="el-icon-plus el-icon-right"></i>
      </ElButton>
    </ElCard>

    <AddTripDialog
      :dialogVisible.sync="tripDialogVisible"
      :shipID="currentShipID"
      @close="closeTripDialog"
    />
    <TripSettings
      :dialogVisible.sync="tripSettingsVisible"
      :shipID="currentShipID"
      :tripID="currentTripID"
      @close="closeTripSettings"
    />
  </div>
</template>

<script>
import AddTripDialog from './AddTripDialog.vue';
import TripSettings from './TripSettings.vue';

export default {
  components: {
    AddTripDialog,
    TripSettings,
  },

  async created() {
    await this.$store.dispatch('getShips');
    this.ships = this.getShips;
  },

  data() {
    return {
      ships: [],
      tripDialogVisible: false,
      tripSettingsVisible: false,
      currentShipID: '',
      currentTripID: '',
    };
  },

  computed: {
    getShips() {
      return this.$store.getters.getShips;
    },
  },

  methods: {
    showTripDialog(ID) {
      this.currentShipID = ID;
      this.tripDialogVisible = true;
    },

    closeTripDialog() {
      this.tripDialogVisible = false;
      this.currentShipID = '';
    },

    changeShip(shipID, tripID) {
      this.currentShipID = shipID;
      this.currentTripID = tripID;
      this.tripSettingsVisible = true;
    },

    async closeTripSettings() {
      this.tripSettingsVisible = false;
      this.currentShipID = '';
      this.currentTripID = '';
    },

    shipType(shipType) {
      return shipType === 'cargo' ? 'Грузовой' : 'Пассажирский';
    },
  },
};
</script>

<style lang="scss" scoped>
  .ships-manager {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    padding: 10px 0 0 0;
  }

  .ship-card {
    margin: 30px 30px 30px 0;
    width: 600px;
    background: #fff6f0;

    .card-header {
      font-size: 18px;

      .ship-name {
        font-weight: bold;
      }

      .ship-name,
      .ship-type {
        margin: 5px 0;
      }
    }
  }

  .ship-trips {
    margin: 10px 0;
    padding: 0;
    list-style: none;
    font-size: 18px;

    &-empty {
      margin: 10px 0;
      font-size: 18px;
      // font-weight: bold;
      font-style: italic;
    }

    .trip {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin: 5px 0;
      padding: 10px;
      border: 1px solid #CECECE;
      border-radius: 5px;
      background: #ffebeb;

      &-info {
        display: flex;
        flex-direction: column;
        max-width: 300px;

        .trip-dest,
        .trip-cargo {
          overflow: hidden;
          text-overflow: ellipsis;
        }
      }

      span {
        font-weight: bold;
      }
    }
  }
</style>
