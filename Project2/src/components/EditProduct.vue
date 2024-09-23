<template>
<div>
  <Navbar isBoard="true"></Navbar>
  <div class="content">
  <div class="d-flex justify-content-center mt-5">
    <div class="mb-3 p-5 col-10 col-md-6 col-lg-4">
      <div class="card">
        <div class="card-header">
          <h2 align="center">Edit Product</h2>
        </div>
        <div class="card-body">
      <form @submit.prevent="editProduct">
        <div class="mb-3">
          <label for="name" class="form-label">Product Name:</label>
          <input type="text" class="form-control" v-model="product.name" required>
        </div>

        <div class="mb-3">
          <label for="description" class="form-label">Description:</label>
          <textarea class="form-control" v-model="product.description" required></textarea>
        </div>
        <div class="row mb-3">
          <div class="col-md-6">
            <label for="rate_per_unit" class="form-label">Rate per Unit:</label>
            <input type="number" class="form-control" v-model="product.rate_per_unit" required>
          </div>

          <div class="col-md-6">
            <label for="quantity" class="form-label">Stock:</label>
            <input type="number" class="form-control" v-model="product.stock" required>
          </div>
        </div>

        <button type="submit" class="btn btn-primary">Edit Product</button>
      </form>
        </div>
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
      product: {
        name: '',
        description: '',
        rate_per_unit: '',
        stock: '',
        category_id: '',
      },
      token: localStorage.getItem('auth-token'),
      role: localStorage.getItem('role'),
    };
  },

  mounted() {
    this.fetchProduct();
  },
  methods: {
    async fetchProduct() {
      try {
        const response = await fetch(`http://127.0.0.1:8080/api/products?id=${this.$route.params.Id}`, {
          method: 'GET',
          headers: {
            'Authentication-Token': this.token,
            'Content-Type': 'application/json',
          },
        });
        const data = await response.json();
        if (response.ok) {
          this.product = data.product || {};
        } else {
          alert(data.message || 'Failed to fetch product');
        }
      } catch (error) {
        console.error('Error fetching product:', error.message);
        alert('Failed to fetch product');
      }
    },
    async editProduct() {
      const { category_id, ...productWithoutCategoryId } = this.product;
      // productWithoutCategoryId.manufacture_date = this.formatDate(productWithoutCategoryId.manufacture_date);
      // productWithoutCategoryId.expiry_date = this.formatDate(productWithoutCategoryId.expiry_date);
      const productToSend = { ...productWithoutCategoryId, category_id: category_id };

      try {
        const res = await fetch(`http://127.0.0.1:8080/api/products/${this.$route.params.Id}`, {
          method: 'PUT',
          headers: {
            'Authentication-Token': this.token,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(productToSend),
        });
        const data = await res.json();
        if (res.ok) {
          alert(data.message);
        } else {
          alert(data.message || 'Failed to update product');
        }
        if (this.role === "admin"){
            this.$router.push({ path: '/adminhome'})
          } else {
            this.$router.push({ path: '/managerhome'})
          }
      } catch (error) {
        alert('Error updating product: ' + error.message);
      }
    },
  },
};
</script>
  