<template>
  <div class="content">
    <Navbar isBoard="true"></Navbar>
    <div class="d-flex justify-content-center">
      <div class="container">
        <h1 class="fw-bold mt-3 text-center">Welcome to Grocery Store!!</h1>
           <div class="card mb-3" style="background-color: #f88ea2" >
             <div class="card-body">
              <div class="input-group mb-3">
                <span class="input-group-text"><h5>Search : </h5></span>
                <input class="form-control me-2" type="text" v-model="searchQuery" placeholder="Search for products here...           "
                      aria-label="Search" @input="performSearch"/>
              </div>
              </div>
            </div>
        <div v-if="filteredProducts.length === 0">
          <p class="fw-bold fs-4 mt-3">No matching products found.</p>
        </div>
        <div v-else>
          <div class="row row-cols-1 row-cols-md-2 g-4 text-center">
            <ul class="list-group list-group-flush">
              <li class="list-group-item">
                <div class="col">
                  <div class="card mb-3" v-for="product in filteredProducts" :key="product.id">
                    <div class="card-header" style="background-color: #f88ea2">
                      <h2>{{ product.name }}</h2>
                    </div>
                    <div class="card-body">
                      <h5 class="card-text">Description : {{ product.description }}</h5>
                      <h5 class="card-text">Category Name : {{ product.category.name }}</h5>
                      <h5 class="card-text">Mfg_Date : {{ formatDate(product.manufacture_date) }}</h5>
                      <h5 class="card-text">Exp_Date : {{ formatDate(product.expiry_date) }}</h5>
                      <h5 class="card-text">Stock : {{ product.quantity }}</h5>
                      <div class="input-group mb-3">
                        <span class="input-group-text">Rs.</span>
                        <span class="input-group-text">{{ product.rate_per_unit }}</span>
                        <input type="number" class="form-control" v-model="selectedQuantity[product.id]" :min="1" 
                          v-if="product.quantity > 0" :max="product.quantity" :disabled="product.quantity <= 0"
                          style="width: 80px; display: inline; margin-right: 5px;"/>
                        <button v-if="product.quantity > 0" @click="addToCart(product)" class="btn btn-primary btn-sm"
                          :disabled=" selectedQuantity[product.id] <= 0 || selectedQuantity[product.id] >
                              product.quantity" > Add to Cart
                        </button>
                        <span v-else class="btn btn-danger float-end" >Out of Stock </span>
                      </div>
                    </div>
                  </div>
                </div>
              </li>
            </ul>
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
      products: [],
      cart: [],
      searchQuery: "",
      selectedQuantity: {},
      token: localStorage.getItem('auth-token'),
    };
  },
  computed: {
    ///--- Use a computed property for filtered products--------------------------------------------------
    filteredProducts() {
      const query = this.searchQuery.toLowerCase().trim();
      return this.products.filter(
        (product) =>
          product.name.toLowerCase().includes(query) ||
          product.description.toLowerCase().includes(query) ||
          product.category.name.toLowerCase().includes(query)
      );
    },
  },
  methods: {
    performSearch() {
      this.$nextTick(() => {
        //---------It is triggered when the search input changes--------------------------------------
      });
    },
    async addToCart(product) {
      try {
        const response = await fetch('http://127.0.0.1:8080/api/shopping_cart_items', {
          method: 'POST',
          headers: {
            'Authentication-Token': this.token,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            product_id: product.id,
            quantity: this.selectedQuantity[product.id],
            total: product.rate_per_unit * this.selectedQuantity[product.id],
          }),
        });
        const data = await response.json();
        if (response.ok) {
          alert(data.message);
          this.selectedQuantity = {}
        } else {
          console.error('Failed to add product to cart:', data.message);
        }
      } catch (error) {
        console.error('Error adding product to cart:', error.message);
      }
    },
    formatDate(dateString) {
      if (!dateString) {
        return 'N/A';
      }
      const date = new Date(dateString);
      const options = { year: 'numeric', month: 'short', day: 'numeric' };
      return date.toLocaleDateString('en-US', options);
    },
    async fetchProducts() {
      try {
        const response = await fetch(`http://127.0.0.1:8080/api/products`, {
          headers: {
            'Authentication-Token': this.token,
            'Content-Type': 'application/json',
          },
        });
        const data = await response.json();
        if (response.ok) {
          this.products = data.products;
        } else {
          alert(data.message);
          console.error('Failed to add product to cart:', data.message);
        }
      } catch (error) {
        console.error('Error fetching products:', error.message);
      }
    },
  },
  mounted() {
    this.fetchProducts()
  }
};
</script>

