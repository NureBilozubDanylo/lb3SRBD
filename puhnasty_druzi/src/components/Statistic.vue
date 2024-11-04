<template>
    <div class="container">
      <h1>Кількіть грошей в кожній категорії</h1>
      <div v-for = "c in this.$store.getters.getTotalCats" :key="c.category_id">
          <p v-if="c.category_id != 1 && c.total_value ">{{c.category_name + ": " + c.total_value }} грн</p>
       </div>

      <h1 class="mbt">Кількіть товарів в заданій категорії</h1>
      <h3>Оберіть категорію</h3>
      <label for="category-select">Виберіть категорію:</label>
            <select v-model="selectedCategoryId" id="category-select">
            <option v-for="category in this.$store.getters.getAllCategories" :key="category.id" :value="category.id">
                {{ category.name }}
            </option>
            </select>
      <p>В цій категорії {{ this.$store.getters?.getProductCount?.product_count }} різних товарів</p>
    </div>
  </template>
  <script>

  export default {
    name: "StatisticC",
    data() {
      return {
        selectedCategoryId: 2,
      };
    },
    mounted(){
      this.$store.dispatch('getTotalCats')
      this.$store.dispatch('getAllCategories')
      this.$store.dispatch('productCount',{
          category_id:this.selectedCategoryId
        })
    },
    methods: {
        
    },
    computed:{
      
    },
    watch:{
      selectedCategoryId(){
        this.$store.dispatch('productCount',{
          category_id:this.selectedCategoryId
        })
      }
    }
  };
  </script>
  