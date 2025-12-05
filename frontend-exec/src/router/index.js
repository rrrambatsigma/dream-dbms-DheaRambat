import { createRouter, createWebHistory } from "vue-router";
import ExecLogin from "../pages/ExecLogin.vue";
import ExecDashboard from "../pages/ExecDashboard.vue";

const routes = [
  {
    path: "/exec/login",
    name: "ExecLogin",
    component: ExecLogin,
  },
  {
    path: "/exec/dashboard",
    name: "ExecDashboard",
    component: ExecDashboard,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
