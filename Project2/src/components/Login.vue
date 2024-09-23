<template>
<div>
  <Navbar></Navbar>
  <div class="d-flex justify-content-center mt-5" style="margin-top:30vh" >
        <div class="card">
         <div class="card-header">
            <center><h1>Login</h1></center>
         </div>
         <div class="card-body">
         
          <div class="mb-3 p-5 bg-light">
          <div class="text-danger"> {{error}} </div>
              <label for="user-email" class="form-label">Email address</label>
              <input type="email" class="form-control" id="user-email" 
              placeholder="name@email.com" v-model="cred.email">
        
              <label for="user-password" class="form-label">Password</label>
              <input type="password" id="user-password" class="form-control" v-model="cred.password">
              <button class="btn btn-primary mt-3" @click="login"> Login </button>
              <router-link class="nav-link active" to="/register">Not a user?Register</router-link>
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
        email: null,
        password: null,
      },
      error: null,
    };
  },
  methods: {
    async login() {
      try {
        const response = await fetch("http://127.0.0.1:8080/user-login", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(this.cred),
        });

        const data = await response.json();
        if (response.ok) {
          localStorage.setItem("auth-token", data.token);
          localStorage.setItem("role", data.role);
          if (data.role === "user") {
            this.$router.push({ path: "/userhome" });
          } else if (data.role === "store_manager"){
            this.$router.push({ path: "/managerhome" });
          } else {
            this.$router.push({ path: "/adminhome" });
          }
        } else {
          // alert(data.message)
          this.error = data.message;
        }
      } catch (error) {
        alert(error)
        console.error(error);
      }
    },
  },
};
</script>

  