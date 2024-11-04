<template>
    <div class="container">
      <div>menu</div>
      <div class="cats_menu">
        <button @click = "setCatHistory(null)">Home</button>
        <div v-for = "c in this.$store.getters.getCategoryHistory" :key="c.id">
          > <button @click = "getCat({id:c.id,name:c.name})" >{{ c.name }}</button>
        </div>
        
      </div>
      <div class="category-wrapper">
        <div class="category" v-for = "c in this.$store.getters.getCategory" :key="c.id">
          <button @click = "getCat({id:c.id,name:c.name})">{{ c.name }}</button>
        </div>
      </div>
      <div class="products-wrapper">
        <div class="product" v-for = "c in this.$store.getters.getProducts" :key="c.id">
          <p>{{ c.name }}</p>
          <p>{{ c.price }}</p>
          <p>{{ c.description }}</p>
        </div>
      </div>
    </div>
  </template>
  <script>
  export default {
    name: "CategoryC",
    data() {
      return {};
    },
    mounted(){
      this.$store.dispatch('getCategory',{
        id:this.$route.params.id,
      }) 
    },
    methods: {
      getCat(info){
        this.$store.dispatch('getCategory',info) 
      },
      setCatHistory(){
        this.$store.dispatch('getCategory',{id:1,name:''}) 
        this.$store.dispatch('setCategoryHistory',null) 
      }
    },
    computed:{
      
    }
  };
  </script>
  