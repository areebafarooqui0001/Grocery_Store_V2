<template>
  <div>
    <Navbar isBoard="true"></Navbar>
    <div class="d-flex justify-content-center mt-3">
      <div class="mb-4 p-5  col-10 col-md-6 col-lg-4">
        <div class="card">
          <div class="card-header">
            <h2 align="center">Edit Category</h2>
          </div>
          <div  class="card-body">
        <div class="mb-3">
          <label for="category-name" class="form-label">Category Name</label>
          <input type="text" class="form-control" id="category-name" placeholder="Category Name"
            v-model="category.name" />
        </div>
        <div class="mb-3">
          <label for="category-description" class="form-label">Category Description</label>
          <input type="text" class="form-control" id="category-description" placeholder="Category Description"
            v-model="category.description" />
        </div>
        <button class="btn btn-primary" @click="updateCategory">Edit Category</button>
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
      category: {
        name: null,
        description: null,
      },
      token: localStorage.getItem('auth-token'),
      role: localStorage.getItem('role'),
    };
  },
  mounted() {
    this.fetchCategory();
  },
  methods: {
    async updateCategory() {
      try {
        const res = await fetch(`http://127.0.0.1:8080/api/categories/${this.$route.params.Id}`, {
          method: 'PUT',
          headers: {
            'Authentication-Token': this.token,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(this.category),
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
        console.error('Error updating category:', error.message);
        alert('Error updating category: ' + error.message);
      }
    },
    async fetchCategory() {
      try {
        const response = await fetch(`http://127.0.0.1:8080/api/categories?id=${this.$route.params.Id}`, {
          method: 'GET',
          headers: {
            'Authentication-Token': this.token,
            'Content-Type': 'application/json',
          },
        });
        const data = await response.json();
        if (response.ok) {
          this.category = data || {};
        } else {
          alert(data.message || 'Failed to fetch category');
        }
      } catch (error) {
        console.error('Error fetching category:', error.message);
        alert('Failed to fetch category');
      }
    },
  },
};
</script>
  