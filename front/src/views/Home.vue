<template>
  <div class="home">
    <ShipManager />
  </div>
</template>

<script>
// @ is an alias to /src
import ShipManager from '@/components/ShipManager.vue';

export default {
  components: {
    ShipManager,
  },
};
</script>

<style lang="scss" scoped>
  .home {
    margin: 0 50px 0 50px;
  }
</style>
