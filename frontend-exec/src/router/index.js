import { createRouter, createWebHistory } from "vue-router";
import ExecLogin from "../pages/ExecLogin.vue";
import ExecDashboard from "../pages/ExecDashboard.vue";

const routes = [
  { path: "/", redirect: "/exec/login" },
  { path: "/exec/login", component: ExecLogin },
  { path: "/exec/dashboard", component: ExecDashboard },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;