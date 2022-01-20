<template>
  <ElDialog
    title="Добавить судно"
    :visible.sync="showDialog"
    width="500px"
    destroy-on-close
    @close="$emit('close')"
  >
    <ElForm
      label-position="left"
      label-width="120px"
    >
      <ElFormItem label="Название судна">
        <ElInput v-model="ship.shipName" />
      </ElFormItem>

      <ElFormItem label="Тип судна">
        <ElRadioGroup v-model="ship.shipType">
          <ElRadio label="cargo">Грузовой</ElRadio>
          <ElRadio label="pass">Пассажирский</ElRadio>
        </ElRadioGroup>
      </ElFormItem>

      <ElButton
        type="primary"
        :disabled="isDisabled"
        @click="addShip()"
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
  },

  data() {
    return {
      showDialog: false,
      ship: {
        shipName: '',
        shipID: '',
        shipType: '',
        trips: [],
      },
    };
  },

  computed: {
    isDisabled() {
      return !this.ship.shipName || !this.ship.shipType;
    },
  },

  methods: {
    addShip() {
      this.ship.shipID = this.generateShipID();

      this.$store.dispatch('addShip', cloneObject(this.ship));

      this.cancel();
    },

    cancel() {
      this.showDialog = false;
      this.clearShipInfo();
    },

    clearShipInfo() {
      this.ship.shipName = '';
      this.ship.shipType = '';
      this.ship.shipID = '';
    },

    generateShipID() {
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
