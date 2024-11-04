import { createStore } from 'vuex'
import router from '../router/index.js'; 

export default createStore({
  state: {
    user:[],
    category:[],
    headCat:1,
    products:[],
    categoryHistory:[],
    allCategories:[],
    totalCats:[],
    productCount:{}
  },
  getters: {
    getUser(state){
      return state.user
    },
    getCategory(state){
      return state.category
    },
    getProducts(state){
      return state.products
    },
    getCategoryHistory(state){
      return state.categoryHistory
    },
    getAllCategories(state){
      return state.allCategories
    },
    getTotalCats(state){
      return state.totalCats
    },
    getProductCount(state){
      return state.productCount
    },
  },
  mutations: {
    setUser(state,payload){
      state.user = payload
    },
    logout(state,payload){
      state.user = payload
    },
    setCategory(state,payload){
      state.category = payload
    },
    setProducts(state,payload){
      state.products = payload
    },
    setHeadCat(state,payload){
      state.headCat = payload
    },
    setCategoryHistory(state,payload){
      if(!payload){
        state.categoryHistory = []
      }else{
        let arr = [];
        for(let a of [...state.categoryHistory,payload]){
          arr.push(a)
          if(payload.id == a.id){
            break;
          }
        }
        state.categoryHistory = arr
      }
    },
    setAllCategories(state,payload){
      state.allCategories = payload
    },
    setTotalCats(state,payload){
      state.totalCats = payload
    },
    setProductCount(state,payload){
      state.productCount = payload
    }
  },
  actions: {
    async login({ commit }, payload) {
        const response = await fetch("http://127.0.0.1:8000/login", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            username: payload.username,
            password: payload.password,
          }),
        });
        let res = await response.json();
        if(res.access_token){
          localStorage.setItem('token', res.access_token);
          localStorage.setItem('username', res.username);
          router.push('/');
        }
        commit('setUser',res)
    },
    async logout({ commit }) {
      commit('logout',[])
    },
    async getCategory({ commit },payload) {
      const response = await fetch(`http://127.0.0.1:8000/categories/${payload.id}`, {
              method: 'GET',
            });
            let res = await response.json()
            if(payload.id != 1){
              commit('setCategoryHistory',payload)
            }
            commit('setHeadCat',payload.id)
            if(res.detail){
              commit('setCategory',[])
            }else{
              commit('setCategory',res)
            }

      const response1 = await fetch(`http://127.0.0.1:8000/categories/${this.state.headCat}/products`, {
              method: 'GET',
            });
            let res1 = await response1.json()  
            commit('setProducts',res1)
    },
    async setCategoryHistory({ commit },payload){
      commit('setCategoryHistory',payload)
    },
    async getAllCategories({ commit }) {
      const response = await fetch(`http://127.0.0.1:8000/allCategories`, {
              method: 'GET',
            });
            let res = await response.json()
            commit('setAllCategories',res.slice(1))
    },
    async getTotalCats({ commit }) {
      const response = await fetch(`http://127.0.0.1:8000/category-totals`, {
              method: 'GET',
            });
            let res = await response.json()
            commit('setTotalCats',res)
    },
    async addNew({commit},payload) {
      commit('setAllCategories',1)
      const response = await fetch(`http://127.0.0.1:8000/add`, {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({
                name: payload.name,
                description: payload.description,
                price: payload.price,
                stock_quantity: payload.stock,
                image_url: payload.image,
                category_id: payload.selectedCategoryId,
              }), 
            });
            let res = await response.json()
            if(res.detail != "Name nust be unique"){
              router.push('/category1');
            }else{
              alert("Name nust be unique")
            }
      
    },
    async productCount({commit},payload) {

      const response = await fetch(`http://127.0.0.1:8000/product-count`, {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({
                category_id: payload.category_id,
              }), 
            });
            let res = await response.json()
            commit('setProductCount',res)
    }
    
  },
  modules: {
  }
})
