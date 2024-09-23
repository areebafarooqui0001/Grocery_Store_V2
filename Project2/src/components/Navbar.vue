<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container-fluid">
      <a class="navbar-brand" href="#">Grocery Store</a>

      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav"
        aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse justify-content-end" id="navbarNav">
        <ul class="navbar-nav">
          <!------------------------------------------------------------------------------------------------->
          <li class="nav-item">
            <router-link class="nav-link active" v-if="isBoard != 'true'" to="/login">Login</router-link>
          </li>
          <li class="nav-item">
            <router-link v-if="isBoard != 'true'" class="nav-link active" to="/register">Register</router-link>
          </li>
          <!------------------------------------------------------------------------------------------------->
          <!--<form class="d-flex" role="search" v-if="role === 'user' && is_login">
            <input type="text" v-model="searchQuery" placeholder="Search products..." />
            <input class="form-control me-2" type="text" v-model="searchQuery" placeholder="Search" aria-label="Search">
            <button class="btn btn-outline-success" type="submit" v-if="is_login">Search</button>
          </form>-->
          <li>
            <router-link v-if="role === 'user'" class="nav-link active" to="/userhome">Home</router-link>
            <router-link v-if="role === 'admin'" class="nav-link active" to="/adminhome">Home</router-link>
            <router-link v-if="role === 'store_manager'" class="nav-link active" to="/managerhome">Home</router-link>
            <!--<router-link v-if="role == none" class="nav-link active" to="/">Home</router-link>-->
          </li>
          <li class="nav-item" v-if="role === 'admin'">
            <router-link class="nav-link active" to="/managers">Managers</router-link>
          </li>

          <li class="nav-item" v-if="role === 'user' && is_login">
            <router-link class="nav-link active" to="/cart">Cart</router-link>
          </li>
          <li class="nav-item" v-if="role === 'user' && is_login">
            <router-link class="nav-link active" to="/order-history">Orders</router-link>
          </li>
          <li class="nav-item" v-if="role === 'store_manager'">
            <span @click="exportData" class="nav-link active" style="cursor: pointer;">
              Export
            </span>
          </li>
          <li class="nav-item" v-if="is_login">
            <button class="nav-link active"  @click="logout">Logout</button>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  props: ['isBoard'],
  data() {
    return {
      // isBoard: false,
      role: localStorage.getItem('role'),
      is_login: localStorage.getItem('auth-token'),
    };
  },
  methods: {
    logout() {
      localStorage.removeItem('auth-token');
      localStorage.removeItem('role');
      this.$router.push({ path: '/login' });
    },
    async exportData() {
      try {
        const url = `http://127.0.0.1:8080/api/store_manager_export`;
        const response = await fetch(url, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            'Authentication-Token': localStorage.getItem('auth-token'),
          },
        });
        const data = await response.json();
        if (response.ok) {
          alert(data.message);
        } else {
          alert(data.message);
        }
      } catch (error) {
        alert("An error occurred: " + error);
      }
    }

  },
};
</script>

