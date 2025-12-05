<template>
  <div class="login-page">
    <div class="login-wrapper">
      <!-- Header -->
      <div class="header">
        <h1 class="title">Executive Portal</h1>
        <p class="subtitle">Find Your Story - Content Management System</p>
      </div>

      <!-- Login Card -->
      <div class="login-card">
        <h2 class="card-title">Sign In</h2>
        <p class="card-subtitle">Enter your credentials to access the Executive dashboard</p>

        <!-- Username Field -->
        <div class="input-group">
          <label class="input-label">
            <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
              <circle cx="12" cy="7" r="4"></circle>
            </svg>
            Username
          </label>
          <input
            v-model="username"
            type="text"
            class="input-field"
            placeholder="Enter your username"
          />
        </div>

        <!-- Password Field -->
        <div class="input-group">
          <label class="input-label">
            <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
              <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
            </svg>
            Password
          </label>
          <input
            v-model="password"
            type="password"
            class="input-field"
            placeholder="Enter your password"
          />
        </div>

        <!-- Error Message -->
        <p v-if="errorMsg" class="error-message">{{ errorMsg }}</p>

        <!-- Login Button -->
        <button @click="loginExec" class="login-button">Login</button>

        <!-- Footer Note -->
        <p class="footer-note">
          <svg class="icon-info" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="12" y1="16" x2="12" y2="12"></line>
            <line x1="12" y1="8" x2="12.01" y2="8"></line>
          </svg>
          Access restricted to Executive only
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import api from "../utils/api";

export default {
  name: "ExecLogin",
  data() {
    return {
      username: "",
      password: "",
      errorMsg: "",
    };
  },
  methods: {
    async loginExec() {
      try {
        const res = await api.post("/login", {
          username: this.username,
          password: this.password,
        });

        localStorage.setItem("token", res.data.token);
        localStorage.setItem("role", res.data.role_id);

        this.$router.push("/exec/dashboard");
      } catch (err) {
        this.errorMsg = "Login gagal! Username atau password salah.";
      }
    },
  },
};
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.login-page {
  min-height: 100vh;
  background-color: #221c1c;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}

.login-wrapper {
  width: 100%;
  max-width: 420px;
}

/* Header - Exactly like Marketing Portal */
.header {
  text-align: center;
  margin-bottom: 35px;
}

.title {
  color: #c9a1a1;
  font-size: 42px;
  font-weight: 700;
  margin: 0 0 10px 0;
  letter-spacing: -0.5px;
}

.subtitle {
  color: #ffffff;
  font-size: 14px;
  margin: 0;
  font-weight: 400;
  letter-spacing: 0.3px;
}

/* Login Card - Matching the design exactly */
.login-card {
  background: linear-gradient(145deg, #3a3232 0%, #342e2e 100%);
  border-radius: 24px;
  padding: 45px 40px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
}

.card-title {
  color: #ffffff;
  font-size: 32px;
  font-weight: 600;
  margin: 0 0 8px 0;
  text-align: center;
  letter-spacing: -0.5px;
}

.card-subtitle {
  color: #d4d4d4;
  font-size: 14px;
  margin: 0 0 35px 0;
  text-align: center;
  font-weight: 300;
  line-height: 1.5;
}

/* Input Groups - Exact spacing */
.input-group {
  margin-bottom: 24px;
}

.input-label {
  display: flex;
  align-items: center;
  color: #e8e8e8;
  font-size: 14px;
  font-weight: 500;
  margin-bottom: 10px;
  letter-spacing: 0.2px;
}

.icon {
  width: 18px;
  height: 18px;
  margin-right: 8px;
  color: #c9a1a1;
  flex-shrink: 0;
}

.input-field {
  width: 100%;
  padding: 15px 18px;
  background-color: #1a1515;
  border: 1.5px solid #4a4242;
  border-radius: 12px;
  color: #ffffff;
  font-size: 15px;
  transition: all 0.25s ease;
  font-family: inherit;
}

.input-field::placeholder {
  color: #6a6060;
  font-weight: 300;
}

.input-field:focus {
  outline: none;
  border-color: #b58a8a;
  background-color: #221c1c;
  box-shadow: 0 0 0 3px rgba(181, 138, 138, 0.1);
}

/* Error Message */
.error-message {
  color: #ff8888;
  font-size: 13px;
  margin: -8px 0 20px 0;
  padding: 12px 14px;
  background-color: rgba(255, 107, 107, 0.12);
  border-left: 3px solid #ff6b6b;
  border-radius: 6px;
  font-weight: 400;
}

/* Login Button - Matching exactly */
.login-button {
  width: 100%;
  padding: 16px;
  background: linear-gradient(135deg, #b58585 0%, #a57474 100%);
  color: #ffffff;
  font-size: 16px;
  font-weight: 600;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 12px;
  letter-spacing: 0.3px;
  text-transform: capitalize;
  box-shadow: 0 4px 15px rgba(181, 133, 133, 0.25);
}

.login-button:hover {
  background: linear-gradient(135deg, #c49696 0%, #b58585 100%);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(181, 133, 133, 0.35);
}

.login-button:active {
  transform: translateY(0);
  box-shadow: 0 2px 10px rgba(181, 133, 133, 0.2);
}

/* Footer Note - Exact match */
.footer-note {
  display: flex;
  align-items: center;
  justify-content: center;
  color: #a8a8a8;
  font-size: 12px;
  margin-top: 28px;
  font-weight: 400;
  letter-spacing: 0.2px;
}

.icon-info {
  width: 16px;
  height: 16px;
  margin-right: 7px;
  color: #c9a1a1;
  flex-shrink: 0;
}

/* Responsive - Matching breakpoints */
@media (max-width: 480px) {
  .title {
    font-size: 36px;
  }

  .login-card {
    padding: 35px 30px;
    border-radius: 20px;
  }

  .card-title {
    font-size: 28px;
  }

  .card-subtitle {
    font-size: 13px;
  }
}

@media (max-width: 360px) {
  .login-wrapper {
    max-width: 100%;
  }

  .login-card {
    padding: 30px 25px;
  }
}
</style>