<template>
<div class="content">
  <Navbar isBoard="true"></Navbar>
  <div class="content">
    <h2 class="text-center mt-4">Order History</h2>
    <div class="d-flex justify-content-center mt-3">
      <div class="mb-3 p-5 col-12 col-md-10 col-lg-8" style="background-color: #f88ea2">
        <div v-if="orderHistory.length === 0">
          <p class="fw-bold fs-4">You haven't placed any orders yet.</p>
        </div>
        <div v-else class="table-responsive">
          <table class="table">
            <thead>
              <tr>
                <th>Product</th>
                <th>Quantity</th>
                <th>Total</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="order in orderHistory" :key="order.id" class="table-success">
                <td>{{ order.name }}</td>
                <td>{{ order.quantity }}</td>
                <td><i class="bi bi-currency-rupee"></i> {{ order.total }}</td>
              </tr>
            </tbody>
          </table>
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
      orderHistory: [],
      token: localStorage.getItem('auth-token'),
    };
  },
  methods: {
    async fetchOrderHistory() {
      try {
        const response = await fetch('http://127.0.0.1:8080/api/order_history', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': this.token,
          },
        });
        const data = await response.json();
        if (response.ok) {
          this.orderHistory = data;
        } else {
          console.error('Failed to fetch order history:', data.message);
        }
      } catch (error) {
        alert('Failed to fetch order history: ' + error.message);
      }
    },
  },
  mounted() {
    this.fetchOrderHistory();
  },
};
</script>

