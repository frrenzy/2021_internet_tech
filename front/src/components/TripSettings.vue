<template>
  <ElDialog
    title="Детали рейса"
    :visible.sync="showDialog"
    width="500px"
    destroy-on-close
    @open="getData"
    @close="$emit('close')"
  >
    <ElForm
      label-position="left"
      label-width="150px"
    >
      <ElFormItem label="Пункт назначения">
        <ElInput v-model="trip.dest" />
      </ElFormItem>

      <ElFormItem v-if="ship.shipType === 'cargo'" label="Груз">
        <ElInput v-model="trip.cargo" />
      </ElFormItem>

      <ElFormItem label="Сменить судно">
        <ElSelect
          v-model="selectedShipID"
          placeholder="Выберите судно"
        >
          <el-option
            v-for="ship in filteredShips"
            :key="ship.shipID"
            :label="ship.shipName"
            :value="ship.shipID">
          </el-option>
        </ElSelect>
      </ElFormItem>

      <ElButton
        type="primary"
        @click="apply()"
      >
        Изменить
      </ElButton>

      <ElButton
        @click="cancel()"
      >
        Отмена
      </ElButton>

      <ElButton
        @click="remove()"
      >
        Удалить рейс
      </ElButton>
    </ElForm>
  </ElDialog>
</template>

<script>
import { cloneObject } from '@/helpers';

export default {
  props: {
    dialogVisible: {
      default: false,
    },

    shipID: {
      default: '',
    },

    tripID: {
      default: '',
    },
  },

  data() {
    return {
      showDialog: false,
      ship: {},
      trip: {},
      selectedShipID: {},
    };
  },

  computed: {
    filteredShips() {
      return this.$store.getters.getFilteredShipsByType(this.ship.shipType);
    },
  },

  methods: {
    getData() {
      this.ship = this.$store.getters.getShipByID(this.shipID);
      this.selectedShipID = this.ship.shipID;
      const tripCopy = this.ship.trips.find(trip => trip.tripID === this.tripID);

      this.trip = cloneObject(tripCopy);
    },

    async apply() {
      if (this.shipID === this.selectedShipID) {
        await this.$store.dispatch('updateTrip', {
          shipID: this.selectedShipID,
          newTrip: cloneObject(this.trip),
        });
      } else {
        await this.$store.dispatch('changeTripShip', {
          currentShipID: this.shipID,
          newShipID: this.selectedShipID,
          updatedTrip: cloneObject(this.trip),
        });
      }
      this.cancel();
    },

    cancel() {
      this.showDialog = false;
    },

    async remove() {
      await this.$store.dispatch('deleteTrip', {
        shipID: this.shipID,
        tripID: this.trip.tripID,
      });
      this.cancel();
    },
  },

  watch: {
    dialogVisible() {
      this.showDialog = this.dialogVisible;
    },
  },
};
</script>
