<template>
  <ElDialog
    title="Добавить рейс"
    :visible.sync="showDialog"
    width="500px"
    destroy-on-close
    @open="loadData"
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

      <ElButton
        type="primary"
        :disabled="isDisabled"
        @click="addTrip()"
      >
        Добавить
      </ElButton>

      <ElButton
        @click="cancel()"
      >
        Отмена
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
  },

  data() {
    return {
      showDialog: false,
      ship: {},
      trip: {
        tripID: '',
        dest: '',
        cargo: '',
      },
    };
  },

  computed: {
    isDisabled() {
      const cargoRule = !this.trip.dest || !this.trip.cargo;
      const passRule = !this.trip.dest;

      return this.ship.shipType === 'cargo' ? cargoRule : passRule;
    },
  },

  methods: {
    loadData() {
      this.ship = this.$store.getters.getShipByID(this.shipID);
    },

    async addTrip() {
      this.trip.tripID = this.generateTripID();
      await this.$store.dispatch('addTrip', {
        shipID: this.shipID,
        trip: cloneObject(this.trip),
      });

      this.cancel();
    },

    cancel() {
      this.showDialog = false;
      this.clearTripInfo();
    },

    clearTripInfo() {
      this.trip.tripID = '';
      this.trip.dest = '';
      this.trip.cargo = '';
    },

    generateTripID() {
      const id = +(new Date()).getTime();

      return id;
    },
  },

  watch: {
    dialogVisible() {
      this.showDialog = this.dialogVisible;
    },
  },
};
</script>
