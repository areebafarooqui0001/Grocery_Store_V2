import { createRouter, createWebHistory } from "vue-router";

import Login from "../components/Login.vue";
import Register from "../components/Register.vue";

import ManagerHome from "../components/ManagerHome.vue";
import UserHome from "../components/UserHome.vue";
import AdminHome from "../components/AdminHome.vue";

import Cart from "../components/Cart.vue";
import OrderHistory from "../components/OrderHistory.vue";

//import CreateCategory from "../components/CreateCategory.vue";
import EditCategory from "../components/EditCategory.vue";
import DeleteCategory from "../components/DeleteCategory.vue";

//import CreateProduct from "../components/CreateProduct.vue";
import EditProduct from "../components/EditProduct.vue";
import DeleteProduct from "../components/DeleteProduct.vue";
import Managers from "../components/Managers.vue";

const routes = [
  { path: "/", component: Login, name: "Home" },
  { path: "/login", component: Login, name: "Login" },
  { path: "/register", component: Register, name: "register" },
  { path: "/managerhome", component: ManagerHome, name: "ManagerHome" },
  { path: "/userhome", component: UserHome, name: "UserHome" },
  { path: "/adminhome", component: AdminHome, name: "AdminHome" },
  { path: "/cart", component: Cart, name: "Cart" },
  { path: "/order-history", component: OrderHistory, name: "OrderHistory" },
  { path: "/managers", component: Managers, name: "Managers" },
  /*{
    path: "/create_category",
    component: CreateCategory,
    name: "Create_Category",
  },*/
  {
    path: "/edit_category/:Id",
    component: EditCategory,
    name: "EditCategory",
    props: (route) => ({
      Id: parseInt(route.params.Id),
    }),
  },
  {
    path: "/delete_category/:Id",
    component: DeleteCategory,
    name: "DeleteCategory",
    props: (route) => ({
      Id: parseInt(route.params.Id),
    }),
  },

  /*{ path: "/create_product", component: CreateProduct, name: "Create_Product" },*/
  {
    path: "/edit_product/:Id",
    component: EditProduct,
    name: "EditProduct",
    props: (route) => ({
      Id: parseInt(route.params.Id),
    }),
  },
  {
    path: "/delete_product/:Id",
    component: DeleteProduct,
    name: "DeleteProduct",
    props: (route) => ({
      Id: parseInt(route.params.Id),
    }),
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});
export default router;

