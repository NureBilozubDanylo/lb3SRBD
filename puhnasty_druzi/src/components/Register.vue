<template>
    <div class="login">
      <div class="container">
        <div class="login-wrapper">
          <h2 class="login-head">Register</h2>
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
            <button class="login-btn-button" @click="tryRegister">Register</button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: "RegisterC",
    data() {
      return {
        username: "",
        password: "",
      };
    },
    methods: {
      async tryRegister() {
        try {
          const response = await fetch("http://127.0.0.1:8000/register", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              username: this.username,
              password: this.password,
            }),
          });
          let res = await response.json();
          console.log(res);
        } catch (error) {
          console.log(error);
        }
      },
    },
  };
  </script>
  