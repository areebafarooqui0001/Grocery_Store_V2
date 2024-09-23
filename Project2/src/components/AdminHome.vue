<template>
  <div class="content">
    <Navbar isBoard="true"></Navbar>
  <div class="d-flex justify-content-center " style="margin-top:10vh">
    <div class="container">
      <h1 align="center">Admin's Dashboard</h1>
      <div class="card mb-3">
        <div class="card-header" style="background-color: #f88ea2">
      <div v-if="categories.length === 0">
        <p class="fw-bold fs-4 mt-3">No categories available!</p>
        <button @click="openModal" class="btn btn-primary">Create Category</button>
      </div>
<!----------------------Categories edit/delete table + create category------------------------------------>
      <div v-else>
          <h3 class="fw-bold fs-4 mt-3">Categories</h3>
          <button @click="openModal" class="btn btn-primary">Create Category</button>
          </div>
<!--------- Modal ----------------------------------------------------------------------------------------->
    <div v-if="showModal" class="modal" :class="{ 'show': showModal, 'fade': showModal }" tabindex="-1" role="dialog"
    style="background-color: rgba(0, 0, 0, 0.5); display: block; margin-top: 50px;">
        <div class="modal-dialog" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Create Category</h5>
                    <button type="button" class="close" @click="closeModal" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <div class="modal-body">
                    <!--<form @submit.prevent="createCategory">-->
                    <div class="form-group">
                    <label for="categoryName">Category Name:</label>
                    <input type="text" id="categoryName" v-model="category.name" class="form-control"
                           required>
                </div>

                <div class="form-group">
                    <label for="categoryDescription">Category Description:</label>
                    <textarea id="categoryDescription" v-model="category.description"
                              class="form-control" required></textarea>
                </div>

                <button @click="createCategory" class="btn btn-primary">Create</button>
                    <!--</form>-->
                </div>
            </div>
        </div>
    </div>
          <div class="card-body">
          <table class="table table-striped table-bordered table-hover">
            <thead>
              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Description</th>
                <th style="width: 150px;" >Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="category in categories" :key="category.id">
                <td>{{ category.id }}</td>
                <td>{{ category.name }}</td>
                <td>{{ category.description }}</td>
                <td>
                  <router-link class="btn btn-primary" :to="{ name: 'EditCategory', params: { Id: category.id } }">Edit</router-link>
                  <router-link class="btn btn-danger" :to="{ name: 'DeleteCategory', params: { Id: category.id } }" style="margin-left: 5px;">Delete</router-link>
                </td>
              </tr>
            </tbody>
          </table>
          </div>
      </div>
      </div>
<!-- ---------------------------------------------------------------------------------------------------->
      <div class="card mb-3">
        <div class="card-header" style="background-color: #f88ea2">
      <div v-if="products.length === 0">
        <p class="fw-bold fs-4 mt-3">No products available!</p>
        <button @click="openModal2" class="btn btn-primary mb-3">Create Product</button>
      </div>
<!--------------------------Product edit/delete table + product creation--------------------------------->
      <div v-else >
        <h3 class="fw-bold fs-4 mt-3">Products</h3>
        <button @click="openModal2" class="btn btn-primary mb-3">Create Product</button>
    </div>
    <!-- Modal 2 ---------------------------------------------------------------------------------------->
    <div v-if="showModal2" class="modal" :class="{ 'show': showModal, 'fade': showModal }" tabindex="-1" 
    role="dialog" style="background-color: rgba(0, 0, 0, 0.5); display: block; margin-top: 50px;">
        <div class="modal-dialog" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Create Product</h5>
                    <button type="button" class="close" @click="closeModal2" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <div class="modal-body">
                    <!--<form @submit.prevent="createProduct">-->
                    <form @submit.prevent="addProduct">
                    <label for="category" class="form-label">Category:</label>
    <select class="form-select" v-model="product.category_id" required>
    <option v-for="category in categories" :value="category.id" :key="category.id">{{category.name}}</option>
    </select>
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
            <label for="manufacture_date" class="form-label">Manufacture Date:</label>
            <input type="date" class="form-control" v-model="product.manufacture_date" required>
          </div>

          <div class="col-md-6">
            <label for="expiry_date" class="form-label">Expiry Date:</label>
            <input type="date" class="form-control" v-model="product.expiry_date">
          </div>
        </div>

        <div class="row mb-3">
          <div class="col-md-6">
            <label for="rate_per_unit" class="form-label">Rate per Unit:</label>
            <input type="number" class="form-control" v-model="product.rate_per_unit" required>
          </div>

          <div class="col-md-6">
            <label for="quantity" class="form-label">Quantity:</label>
            <input type="number" class="form-control" v-model="product.quantity" required>
          </div>
        </div>
    
        <button type="submit" class="btn btn-primary">Add Product</button>
    
                </form>
                </div>
            </div>
        </div>
      </div>
      <div classs="card-body">
        <table class="table table-bordered">
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Description</th>
              <th>Category</th>
              <th>Dates</th>
              <th>Price</th>
              <th>Stock</th>
              <th style="width: 150px;" >Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="product in products" :key="product.id">
              <td>{{ product.id }}</td>
              <td>{{ product.name }}</td>
              <td>{{ product.description }}</td>
              <td>{{ product.category.name }}</td>
              <td>
                <span style="display: block;">Mfg_Date: {{ formatDate(product.manufacture_date) }}</span>
                <span style="display: block;">Exp_Date: {{ formatDate(product.expiry_date) }}</span>
              </td>
              <td><i class="bi bi-currency-rupee"></i> {{ product.rate_per_unit }}</td>
              <td>{{ product.quantity }}</td>
              <td>
                  <router-link class="btn btn-primary" :to="{ name: 'EditProduct', params: { Id: product.id } }">Edit</router-link>
                  <router-link class="btn btn-danger" :to="{ name: 'DeleteProduct', params: { Id: product.id } }" style="margin-left: 5px;">Delete</router-link>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      </div>
        </div>

      <!---------------------------------------------------------------------------------------->
      <div class="card mb-3"> 
        <div class="card-header" style="background-color: #f88ea2">
      <div v-if="category_requests.length === 0">
        <p class="fw-bold fs-4 mt-3">No category requests!</p>
      </div>

      <div v-else >
        <p class="fw-bold fs-4 mt-3 ">Manager's Category Requests</p>
      </div>
      <div class="card-body">
        <table class=" table table-striped table-bordered table-hover">
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Request</th>
              <th>Approval Status</th>
              <th style="width: 180px;">Requests</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="category in category_requests" :key="category.id">
              <td>{{ category.id }}</td>
              <td>{{ category.name }}</td>
              <td>{{ category.request }}</td>
              <td>{{ category.is_approved }}</td>
              <td>
                  <button v-on:click="handleCategoryRequest(category.id, 'approve')" 
                  :disabled="category.is_approved == true"
                  class="btn btn-primary">Approve</button>
                  <button v-on:click="handleCategoryRequest(category.id, 'reject')" 
                  :disabled="category.is_approved == true"
                  class="btn btn-danger" style="margin-left: 5px;">Reject</button>
              </td>
            </tr>
          </tbody>
        </table>
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
  components: {
    Navbar,
  },
  data() {
    return {
      showModal: false,
      showModal2 : false,
      category: {
        name: null,
        description: null,
      },
      product: {
        name: '',
        description: '',
        manufacture_date: '',
        expiry_date: '',
        rate_per_unit: '',
        quantity: '',
        category_id: '',
      },
      userRole: localStorage.getItem("role"),
      token: localStorage.getItem("auth-token"),
      categories: [],
      products: [],
      //users: [],
      category_requests: [],
    };
  },
  methods: {
    formatDate(dateString) {
      if (!dateString) {
        return 'N/A';
      }
      const date = new Date(dateString);
      const options = { year: 'numeric', month: 'short', day: 'numeric' };
      return date.toLocaleDateString('en-US', options);
    },
    formatDate(dateString) {
      const date = new Date(dateString);
      if (isNaN(date.getTime())) {
        return null;
      }
      return date.toISOString().split('T')[0];
    },
    openModal() {
            console.log('Opening modal');
            this.showModal = true;
            console.log('After opening modal:', this.showModal);
        },
    closeModal() {
            console.log('Closing modal');
            this.showModal = false;
            console.log('After closing modal:', this.showModal);
        },
    openModal2() {
            console.log('Opening modal2');
            this.showModal2 = true;
            console.log('After opening modal2:', this.showModal2);
        },
    closeModal2() {
            console.log('Closing modal2');
            this.showModal2 = false;
            console.log('After closing modal2:', this.showModal2);
        },
    async createCategory() {
        try {
        const res = await fetch('http://127.0.0.1:8080/api/categories', {
          method: 'POST',
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
          this.$router.push({ path: '/adminhome'})
          this.closeModal();
        
      } catch (error) {
        console.error('Error creating category:', error.message);
        alert('Error creating category: ' + error.message);
      }
    },
    async addProduct() {
      const { category_id, ...productWithoutCategoryId } = this.product;
      productWithoutCategoryId.manufacture_date = this.formatDate(productWithoutCategoryId.manufacture_date);
      productWithoutCategoryId.expiry_date = this.formatDate(productWithoutCategoryId.expiry_date);
      const productToSend = { ...productWithoutCategoryId, category_id: category_id };
      
      const res = await fetch('http://127.0.0.1:8080/api/products', {
        method: 'POST',
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
          alert(data.message);
        }this.closeModal2();
        if (this.role === "admin"){
          this.$router.push({ path: '/adminhome'})
        }
    },
    async fetchProducts() {
      try {
        const response = await fetch(`http://127.0.0.1:8080/api/products`, {
          method: 'GET',
          headers: {
            'Authentication-Token': this.token,
            'Content-Type': 'application/json',
          },
        });
        const data = await response.json();
        if (response.ok) {
          this.products = data.products || [];
        } else {
          alert(data.message || 'Failed to fetch products');
        }
      } catch (error) {
        console.error('Error fetching products:', error.message);
        alert('Failed to fetch products');
      }
    },
    async fetchCategories() {
      try {
        const response = await fetch(`http://127.0.0.1:8080/api/categories`, {
          method: 'GET',
          headers: {
            'Authentication-Token': this.token,
            'Content-Type': 'application/json',
          },
        });
        const data = await response.json();
        if (response.ok) {
          console.log(data.categories)
          this.categories = data.categories || [];
        } else {
          alert(data.message || 'Failed to fetch categories');
        }
      } catch (error) {
        console.error('Error fetching categories:', error.message);
        alert('Failed to fetch categories');
      }
    },
    /*async fetchUsers() {
      try {
        const response = await fetch(`http://127.0.0.1:8080/users`, {
          method: 'GET',
          headers: {
            'Authentication-Token': this.token,
            'Content-Type': 'application/json',
          },
        });
        const data = await response.json();
        if (response.ok) {
          console.log(data.users)
          this.users = data|| [];
        } else {
          alert(data.message || 'Failed to fetch users');
        }
      } catch (error) {
        console.error('Error fetching users:', error.message);
        alert('Failed to fetch users');
      }
    },
    async handleManagerRequest(id, action) {
      try {
        const url = `http://127.0.0.1:8080/store_manager_request/${id}/${action}`;
        const response = await fetch(url, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            'Authentication-Token': this.token,
          },
        });
        const data = await response.json();
        if (response.ok) {
          alert(data.message);
          this.fetchUsers();
        } else {
          alert(data.message);
          this.fetchUsers();
        }
      } catch (error) {
        alert("An error occurred", error);
        this.$router.push({ name: "AdminHome" });
      }
    },*/
    async fetchCatgeoryRequests() {
      try {
        const response = await fetch(`http://127.0.0.1:8080/category_requests`, {
          method: 'GET',
          headers: {
            'Authentication-Token': this.token,
            'Content-Type': 'application/json',
          },
        });
        const data = await response.json();
        if (response.ok) {
          console.log(data)
          this.category_requests = data|| [];
        } else {
          alert(data.message || 'Failed to fetch category requests');
        }
      } catch (error) {
        console.error('Error fetching category requests:', error.message);
        alert('Failed to fetch category requests');
      }
    },
    async handleCategoryRequest(id, action) {
      try {
        const url = `http://127.0.0.1:8080/category_request/${id}/${action}`;
        const response = await fetch(url, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            'Authentication-Token': this.token,
          },
        });
        const data = await response.json();
        if (response.ok) {
          alert(data.message);
          this.fetchCatgeoryRequests();
          this.fetchProducts();
          this.fetchCategories();
        } else {
          alert(data.message);
          this.fetchCatgeoryRequests();
          this.fetchProducts();
          this.fetchCategories();
        }
      } catch (error) {
        alert("An error occurred", error);
        this.$router.push({ name: "AdminHome" });
      }
    },
  },
  mounted() {
    this.fetchProducts();
    this.fetchCategories();
    //this.fetchUsers();
    this.fetchCatgeoryRequests();
  },
};
</script>
<style>
    table {
        width: 100%;
        border-collapse: collapse;
        margin-bottom: 20px;
    }

    th, td {
        border: 1px solid #333;
        text-align: left;
        padding: 8px;
    }

    th {
        background-color: #f2f2f2;
    }

    tr:hover {
        background-color: #f5f5f5;
    }
</style>