<template>
<div>
    <Navbar isBoard="true"></Navbar>
  <div v-if="managers.length === 0">
        <p class="fw-bold fs-4 mt-3">No manager requests!</p>
      </div>

      <div v-else >
        <div class="card">
            <div class="card-header" style="background-color: #f88ea2">
        <p class="fw-bold fs-4 mt-3 text-center">Manager Approval Requests</p>
            </div>
            <div class="card-body">
        <table class="table table-striped table-bordered table-hover">
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Email</th>
              <th>Approval Status</th>
              <th class="text-center">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="manager in managers" :key="manager.id">
              <td>{{ manager.id }}</td>
              <td>{{ manager.username }}</td>
              <td>{{ manager.email }}</td>
              <td>{{ manager.active }}</td>
              <td>
                  <button v-on:click="handleManagerRequest(manager.id, 'approve')" 
                  :disabled="manager.active == true"
                  class="btn btn-primary">Approve</button>
                  <button v-on:click="handleManagerRequest(manager.id, 'reject')" 
                  :disabled="manager.active == true"
                  class="btn btn-danger" style="margin-left: 5px;">Reject</button>
              </td>
            </tr>
          </tbody>
        </table>
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
      userRole: localStorage.getItem("role"),
      token: localStorage.getItem("auth-token"),
      managers: [],
    };
  },
  methods: {
    async fetchManagers() {
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
          console.log(data.managers)
          this.managers = data|| [];
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
          this.fetchManagers();
        } else {
          alert(data.message);
          this.fetchManagers();
        }
      } catch (error) {
        alert("An error occurred", error);
        this.$router.push({ name: "AdminHome" });
      }
    },
  },
  mounted() {
    this.fetchManagers();

  },

}
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