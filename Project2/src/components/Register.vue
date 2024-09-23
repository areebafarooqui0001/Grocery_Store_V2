<template>
<div>
  <Navbar></Navbar>
  <div class="d-flex justify-content-center mt-5" style="margin-top:30vh" >
    <div class="card">
     <div class="card-header">
        <h1 align="center">Register</h1>
     </div>
     <div class="card-body">
     
      <div class="mb-3 p-5 bg-light">
      <div class="text-danger"> {{error}} </div>
          <label for="user-email" class="form-label">Email address</label>
          <input type="email" class="form-control" id="user-email" 
          placeholder="name@email.com" v-model="cred.email">

          <label for="user-name" class="form-label">Name</label>
          <input type="text" id="user-name" class="form-control" v-model="cred.name">
    
          <label for="user-password" class="form-label">Password</label>
          <input type="password" id="user-password" class="form-control" v-model="cred.password">
          
          <label for="roleSelect" class="form-label">Role</label>
          <select id="roleSelect" class="form-select mb-2" v-model="cred.role">
            <option value="user">User</option>
            <option value="store_manager">Store Manager</option>
          </select>

          <button class="btn btn-primary mt-3" @click="register"> Register </button>
          <router-link class="nav-link active" to="/login">Already a user?Login</router-link>
      </div>
     </div>
      </div>

</div>
</div>
</template>
  
<script>
import Navbar from "./Navbar.vue";
export default {
  components: {
    Navbar,
  },
  data() {
    return {
      cred: {
        name: null,
        email: null,
        password: null,
        role: null, // Default role is 'user'
      },
      error: null,
    };
  },
  methods: {
    async register() {
      try {
        console.log("Register method called");
        const res = await fetch("http://127.0.0.1:8080/user-register", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(this.cred),
        });

        const data = await res.json();

        if (res.ok) {
          alert(data.message);
          // Optionally, you can navigate to the login page or perform other actions after successful registration
          this.$router.push({ path: "/login" });
        } else {
          this.error = data.message;
        }
      } catch (error) {
        console.error("Error during registration:", error);
      }
    },
  },
};
</script>
  
  