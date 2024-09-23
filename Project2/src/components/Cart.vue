<template>
<div>
  <Navbar isBoard="true"></Navbar>
  <div class="content">
  <h1 class="text-center mt-4">Shopping Cart</h1>
  <div class="d-flex justify-content-center mt-3">
      <div class="mb-3 p-5 col-12 col-md-10 col-lg-10">
        <div class="card">
          <div class="card-header" style="background-color: #f88ea2">
        <div v-if="ShoppingCartItems.length === 0">
          <p class="fw-bold fs-4">Your cart is empty.</p>
        </div>
        <div v-else class="table-responsive">
          <h3 class="fw-bold fs-4 mt-3">Your Cart Items</h3>
        </div>
        <div class="card-body">
          <table class="table">
            <thead>
              <tr>
                <th>Product</th>
                <th>Quantity</th>
                <th>Total</th>
                <th style="width: 180px;"></th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in ShoppingCartItems" :key="item.id" class="table-success">
                <!-- Table Rows for Cart Items -->
                <td>{{ item.product }}</td>
                <td>{{ item.quantity }}</td>
                <td><i class="bi bi-currency-rupee"></i> {{ item.total }}</td>
                <td style="width: 150px;">
                  <button @click="removeFromCart(item)" class="btn btn-danger btn-sm float-end">Remove from Cart</button>
                </td>
              </tr>
              <!-- Buy Cart Button -->
              <tr>
                <td colspan="3">
                  <span class="fw-bold fs-5 mt-2">Grand Total: <i class="bi bi-currency-rupee"></i> {{ cart_total }}</span>
                </td>
                <td colspan="">
                  <button @click="buyCart" class="btn btn-primary btn-block float-end">Buy</button>
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
      ShoppingCartItems: [],
      cart_total: 0,
      token: localStorage.getItem('auth-token'),
    };
  },
  methods: {
    async buyCart() {
      try {
        const response = await fetch(`http://127.0.0.1:8080/api/cart_purchase`, {
          method: 'POST',
          headers: {
            'Authentication-Token': this.token,
          },
        });
        const data = await response.json();
        if (response.ok) {
          alert(data.message);
        } else {
          alert(data.message);
          console.error('Failed to add product to cart:', data.message);
        }
        this.$router.push({ path: "/userhome" });
      } catch (error) {
        alert('Failed to buy cart: ' + error.message);
      }
    },

    async removeFromCart(item) {
      try {
        const response = await fetch(`http://127.0.0.1:8080/api/shopping_cart_items/${item.id}`, {
          method: 'DELETE',
          headers: {
            'Authentication-Token': this.token,
          },
        });   
        const data = await response.json();
        if (response.ok) {
          alert(data.message);
        } else {
          alert(data.message);
          console.error('Failed to add product to cart:', data.message);
        }
        this.fetchCartItems(); // Fetch updated cart items after removal
      } catch (error) {
        console.error('Failed to remove product from cart:', error.message);
        alert('Failed to remove product from cart: ' + error.message);
      }
    },
    
    async fetchCartItems() {
      try {
        const response = await fetch('http://127.0.0.1:8080/api/shopping_cart_items', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': this.token,
          },
        });
        const data = await response.json();
        if (response.ok) {
          this.ShoppingCartItems = data.cart_products;
          this.cart_total = data.cart_total;
        } else {
          console.error(data.message);
        } 
      } catch (error) {
        alert('Failed to fetch cart items: ' + error.message);
      }
    }    
  },
  mounted() {
    this.fetchCartItems(); 
  },
};
</script>