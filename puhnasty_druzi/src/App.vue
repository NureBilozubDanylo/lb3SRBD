<template>
  <div class="wrapper">
    <Header></Header>
    <main class="main">
      <router-view></router-view>
    </main>
  </div>
</template>

<script>
import Header from "./components/Header.vue";
export default {
  name: "App",
  components: {
    Header
  },
};
</script>
