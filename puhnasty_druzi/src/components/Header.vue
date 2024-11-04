<script>
export default {
  name: "HeaderC",
  data() {
    return {
    };
  },
  methods: {
    logout() {
      localStorage.removeItem('token');
      localStorage.removeItem('username');
      this.$store.dispatch('logout')
      this.$router.push({name:'login'})
    }
  },
  computed: {
    username() {
      let a = this.$store.getters.getUser.username;
      if(localStorage.getItem('username')){
        return localStorage.getItem('username')
      }
      return a;
    }
  }
};
</script>
<template>
  <header class="header">
    <div class="container">
      <div class="header-wrapper">
        <router-link :to="{ name: 'main' }"> Home </router-link>
        <div class="header-menu">
          <router-link :to="{ name: 'category', params: { id: 1 } }"> Goods </router-link>
          <router-link :to="{ name: 'add'}"> Add </router-link>
          <router-link :to="{ name: 'statistic'}"> Statistic </router-link>
          <router-link v-if="username" :to="{ name: 'cart' }">{{ username }}</router-link>
          <router-link v-else>
            <router-link :to="{ name: 'login' }">Login</router-link>
          </router-link>
          <router-link :to="{ name: 'cart' }"> Cart </router-link>
          <button v-if="username" class="logout" @click ="logout">Logout</button>
        </div>
      </div>
    </div>
  </header>
</template>
