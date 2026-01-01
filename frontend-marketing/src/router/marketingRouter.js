import { createRouter, createWebHistory } from "vue-router";
import MarketLogin from "../pages/MarketingLoginPage.vue";
import MarketDashboard from "../pages/MarketingDashboardPage.vue";

/**
 * ======================================
 * ROUTES
 * ======================================
 */
const routes = [
  {
    path: "/",
    name: "MarketingLogin",
    component: MarketLogin
  },
  {
    path: "/marketing-dashboard",
    name: "MarketingDashboard",
    component: MarketDashboard,
    meta: {
      requiresAuth: true,
      requiresMarketing: true
    }
  }
];

/**
 * ======================================
 * ROUTER INSTANCE
 * ======================================
 */
const router = createRouter({
  history: createWebHistory(),
  routes
});

/**
 * ======================================
 * GLOBAL ROUTE GUARD
 * ======================================
 */
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("token");
  const roleId = Number(localStorage.getItem("role_id"));

  // 🔒 Route butuh login
  if (to.meta.requiresAuth && !token) {
    next("/");
    return;
  }

  // 🔒 Khusus role MARKETING (RoleID = 2)
  if (to.meta.requiresMarketing && roleId !== 2) {
    localStorage.clear();
    next("/");
    return;
  }

  next();
});

export default router;
