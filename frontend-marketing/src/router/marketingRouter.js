import { createRouter, createWebHistory } from "vue-router";
import MarketLogin from "../pages/MarketingLoginPage.vue";
import MarketDashboard from "../pages/MarketingDashboardPage.vue";

const routes = [
  { path: "/", component: MarketLogin },
  { path: "/marketing/dashboard", component: MarketDashboard },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;