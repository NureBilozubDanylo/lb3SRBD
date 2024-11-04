<template>
    <div class="container">
      <h1>Add new good</h1>
      <div>
            <label for="category-select">Виберіть категорію:</label>
            <select v-model="selectedCategoryId" id="category-select">
            <option v-for="category in this.$store.getters.getAllCategories" :key="category.id" :value="category.id">
                {{ category.name }}
            </option>
            </select>
            <div class="add-block">
                <p>Назва</p>
                <input type="text" v-model="name" >
            </div>
            <div class="add-block">
                <p>Опис</p>
                <input type="text" v-model="description" >
            </div>
            <div class="add-block">
                <p>Ціна</p>
                <input type="number" v-model="price" >
            </div>
            <div class="add-block">
                <p>Кількість на складі</p>
                <input type="number" v-model="stock" >
            </div>
            <div class="add-block">
                <p>Зображення</p>
                <input type="text" v-model="image" >
            </div>
       </div>
       <button @click = "add">Add</button>
    </div>
  </template>
  <script>
  export default {
    name: "AddNewC",
    data() {
      return {
        selectedCategoryId: 2,
        name:"",
        description:"",
        price:0,
        stock:0,
        image:"",
      };
    },
    mounted(){
      this.$store.dispatch('getAllCategories')
    },
    methods: {
        async add() {
            this.$store.dispatch('addNew',{
                selectedCategoryId:this.selectedCategoryId,
                name:this.name,
                description:this.description,
                price:this.price,
                stock:this.stock,
                image:this.image,
            }) 
      
        },
    },
    computed:{
      
    }
  };
  </script>
  