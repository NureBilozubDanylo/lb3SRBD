<template>
  <div class="login">
    <div class="container">
      <div class="login-wrapper">
        <h2 class="login-head">Account Log in</h2>
        <input
          type="text"
          class="login-input"
          v-model="username"
          placeholder="Username"
        />
        <input
          type="text"
          class="login-input"
          v-model="password"
          placeholder="Password"
        />
        <div class="login-btn">
          <button class="login-btn-button" @click="tryLogin">Log in</button>
        </div>
        <div class="login-other">
          <p class="login-other-f">Forgot passwod?</p>
          <router-link :to="{ name: 'register' }">
            <p class="login-other-f">Register Now</p>
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "LoginC",
  data() {
    return {
      username: "",
      password: "",
    };
  },
  methods: {
    async tryLogin() {
      this.$store.dispatch('login',{
        username:this.username,
        password:this.password
      }) 
      
    },
  },
};
</script>
