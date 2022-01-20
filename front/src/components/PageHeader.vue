<template>
  <div class="header">
    <div class="title">Панель администратора морского порта</div>
    <div class="btn-wrapper">
      <el-button
        class="add-ship-btn"
        @click="shipDialogVisible = true"
      >
        Добавить судно <i class="el-icon-plus el-icon-right"></i>
      </el-button>
    </div>

    <AddShipDialog
      :dialogVisible.sync="shipDialogVisible"
      @close="shipDialogVisible = false"
    />
  </div>
</template>

<script>
import AddShipDialog from './AddShipDialog.vue';

export default {
  components: {
    AddShipDialog,
  },

  data() {
    return {
      shipDialogVisible: false,
    };
  },
};
</script>

<style lang="scss" scoped>
  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
    height: 60px;
    top: 0;
    background: #e3ffe4;
    padding-left: 50px;
    padding-right: 50px;
    box-shadow: 0px 4px 8px 0px rgba(34, 60, 80, 0.2);
    border: 1px solid #e3ffe4;

    .title {
      font-size: 20px;
      font-weight: bold;
    }

    .add-ship-btn {
      display: block;
      margin-right: 100px;
    }
  }
</style>
