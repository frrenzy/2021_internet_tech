<template>
  <div id="app">
    <PageHeader />
    <router-view/>
  </div>
</template>

<script>
import PageHeader from './components/PageHeader.vue';

export default {
  components: {
    PageHeader,
  },
};
</script>

<style lang="scss">
  #app {
    font-family: sans-serif;
    // background: #63d9db;
    background: #e3fcfc;
  }
</style>
