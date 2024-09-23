<template>
<div>
    <Navbar isBoard="true"></Navbar>
    <div class="row justify-content-center mt-5" >
      <div class="col-md-4 col-lg-4 col-12 ">
        <div class="card">
          <div class="card-header" style="background-color: #f88ea2">
          <h1 aligh="center">Delete Product</h1>
        </div>
          <div class="card-body">
            <h4 class="card-title text-center">
              Are you sure, you want to Delete this product?
            </h4>
            <form @submit.prevent="deleteProduct">
              <button type="submit" class="btn btn-danger float-end">Delete</button>
            </form>
          </div>
        </div>
      </div>
    </div>
</div>
  </template>
  
  <script>
  import Navbar from "./Navbar.vue";
  
  export default {
    props: ['Id'],
    components: {
      Navbar,
    },
    data() {
      return {
        token: localStorage.getItem("auth-token"),
        role: localStorage.getItem('role'),
      };
    },
    methods: {
      async deleteProduct() {
        try {
          const res = await fetch(`http://127.0.0.1:8080/api/products/${this.$route.params.Id}`, {
            method: 'DELETE',
            headers: {
              'Authentication-Token': this.token,
            },
          });
  
          const data = await res.json();
          if (res.ok) {
            alert(data.message);
          } else {
            alert(data.message);
          }
          if (this.role === "admin"){
            this.$router.push({ path: '/adminhome'})
          } else {
            this.$router.push({ path: '/managerhome'})
          }
        } catch (error) {
          alert(error.message);
        }
      },
    },
  };
  </script>
  
  <style scoped></style>
  