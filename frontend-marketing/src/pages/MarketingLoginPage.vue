<template>
  <div class="login-container">
    <!-- Marketing Portal Title tanpa kotak -->
    <div class="title-container">
      <h1 class="main-title-login">Marketing Portal</h1>
      <p class="subtitle-login">Find Your Story - Content Management System</p>
    </div>

    <!-- Login Form -->
    <div class="login-form-container">
      <div class="login-card">
        <!-- Glow Effect untuk efek timbul -->
        <div class="card-glow"></div>
        
        <div class="login-header">
          <!-- Tulisan Sign In dipisahkan untuk kontrol posisi -->
          <div class="sign-in-wrapper">
            <h2 class="login-title">Sign In</h2>
          </div>
          <p class="login-subtitle">Enter your credentials to access the marketing dashboard</p>
        </div>

        <form @submit.prevent="login" class="login-form">
          <div class="input-group">
            <label for="username" class="input-label">
              <i class="icon-user"></i>
              Username
            </label>
            <input
              id="username"
              v-model="username"
              type="text"
              class="styled-input"
              placeholder="Enter your username"
              required
            />
          </div>

          <div class="input-group">
            <label for="password" class="input-label">
              <i class="icon-lock"></i>
              Password
            </label>
            <input
              id="password"
              v-model="password"
              type="password"
              class="styled-input"
              placeholder="Enter your password"
              required
            />
          </div>

          <button 
            type="submit" 
            class="login-button"
            :disabled="loading"
          >
            <span v-if="!loading">Login</span>
            <span v-else class="loading-spinner"></span>
          </button>
        </form>

        <!-- Error Message -->
        <div v-if="errorMessage" class="error-message">
          <i class="icon-error"></i>
          {{ errorMessage }}
        </div>

        <!-- Footer -->
        <div class="login-footer">
          <p class="footer-text">
            <i class="icon-info"></i>
            Access restricted to marketing team members only
          </p>
        </div>
      </div>
    </div>

    <!-- Background Decoration dengan efek blur -->
    <div class="background-decoration">
      <div class="bg-circle blurred"></div>
      <div class="bg-circle blurred"></div>
      <div class="bg-circle blurred"></div>
      <div class="bg-circle blurred"></div>
      <div class="bg-circle blurred"></div>
    </div>
    
    <!-- Background Overlay untuk efek blur -->
    <div class="background-overlay"></div>
  </div>
</template>

<script>
export default {
  name: 'MarketingLogin',
  data() {
    return {
      username: "",
      password: "",
      errorMessage: "",
      loading: false
    };
  },
  methods: {
    async login() {
      // Reset error message
      this.errorMessage = "";
      this.loading = true;

      try {
        const response = await fetch("http://localhost:5000/login", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            username: this.username,
            password: this.password
          }),
        });

        const data = await response.json();

        if (!data.success) {
          this.errorMessage = data.message || data.error || "Login failed";
          return;
        }

        // Save token
        localStorage.setItem("token", data.token);
        localStorage.setItem("role_id", data.role_id);

        // Check marketing role
        if (data.role_id !== 2) {
          this.errorMessage = "Access denied. Marketing team members only.";
          return;
        }

        // Redirect to marketing dashboard
        this.$router.push("/marketing/dashboard");

      } catch (error) {
        console.error("Login error:", error);
        this.errorMessage = "Connection error. Please try again.";
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  background: 
    /* Base gradient */
    linear-gradient(135deg, 
      rgba(12, 10, 8, 0.98) 0%, 
      rgba(18, 15, 12, 0.98) 25%, 
      rgba(26, 21, 18, 0.98) 50%, 
      rgba(18, 15, 12, 0.98) 75%, 
      rgba(12, 10, 8, 0.98) 100%),
    /* Texture overlay */
    url("data:image/svg+xml,%3Csvg width='100' height='100' viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M11 18c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm48 25c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm-43-7c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm63 31c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM34 90c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm56-76c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM12 86c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm28-65c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm23-11c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-6 60c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm29 22c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zM32 63c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm57-13c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-9-21c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM60 91c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM35 41c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM12 60c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2z' fill='%23983d44' fill-opacity='0.03' fill-rule='evenodd'/%3E%3C/svg%3E");
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  padding: 40px 20px 20px;
  position: relative;
  overflow: hidden;
  backdrop-filter: blur(2px);
}

/* Background Overlay untuk efek blur tambahan */
.background-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(
    circle at 30% 20%,
    rgba(152, 61, 68, 0.1) 0%,
    transparent 50%
  ),
  radial-gradient(
    circle at 70% 80%,
    rgba(184, 124, 124, 0.08) 0%,
    transparent 50%
  );
  pointer-events: none;
  z-index: 1;
}

/* Title Container tanpa kotak */
.title-container {
  text-align: center;
  margin-bottom: 30px;
  margin-top: 10px;
  padding: 0;
  background: transparent;
  border: none;
  box-shadow: none;
  width: 100%;
  max-width: 500px;
  position: relative;
  z-index: 3;
}

/* Judul Marketing Portal tanpa kotak */
.main-title-login {
  font-size: 2rem;
  font-weight: 800;
  background: linear-gradient(135deg, #f8f4ed 0%, #d8a0a5 50%, #b87c7c 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 10px;
  font-family: 'Poppins', sans-serif;
  letter-spacing: -0.02em;
  text-shadow: 
    0 2px 10px rgba(152, 61, 68, 0.3),
    0 4px 20px rgba(0, 0, 0, 0.4);
  position: relative;
  z-index: 3;
}

.subtitle-login {
  font-size: 0.9rem;
  color: rgba(248, 244, 237, 0.9);
  margin-bottom: 0;
  font-weight: 400;
  font-family: 'Poppins', sans-serif;
  letter-spacing: 0.02em;
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.5);
  position: relative;
  z-index: 3;
}

/* Login Form Container */
.login-form-container {
  width: 100%;
  max-width: 400px;
  z-index: 4;
  margin-bottom: 20px;
  position: relative;
}

/* Card Glow Effect */
.card-glow {
  position: absolute;
  top: -15px;
  left: -15px;
  right: -15px;
  bottom: -15px;
  background: radial-gradient(
    circle at 50% 0%,
    rgba(152, 61, 68, 0.15) 0%,
    transparent 70%
  );
  border-radius: 30px;
  filter: blur(20px);
  z-index: 1;
  opacity: 0.7;
  animation: glowPulse 4s ease-in-out infinite;
}

@keyframes glowPulse {
  0%, 100% {
    opacity: 0.5;
    transform: scale(1);
  }
  50% {
    opacity: 0.8;
    transform: scale(1.02);
  }
}

.login-card {
  background: linear-gradient(
    145deg,
    rgba(50, 42, 36, 0.95) 0%,
    rgba(38, 32, 26, 0.95) 100%
  );
  border-radius: 24px;
  padding: 35px 30px;
  border: 1px solid rgba(184, 124, 124, 0.25);
  box-shadow: 
    0 25px 50px -12px rgba(0, 0, 0, 0.8),
    inset 0 1px 0 rgba(255, 255, 255, 0.1),
    inset 0 -1px 0 rgba(0, 0, 0, 0.3),
    0 0 0 1px rgba(152, 61, 68, 0.1);
  backdrop-filter: blur(20px);
  position: relative;
  z-index: 2;
  transform-style: preserve-3d;
  perspective: 1000px;
}

/* Efek hover untuk card */
.login-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(
    145deg,
    rgba(255, 255, 255, 0.05) 0%,
    transparent 50%,
    rgba(0, 0, 0, 0.1) 100%
  );
  border-radius: 24px;
  z-index: -1;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.login-card:hover::before {
  opacity: 1;
}

.login-header {
  text-align: center;
  margin-bottom: 25px;
  position: relative;
  z-index: 3;
}

/* Wrapper untuk Sign In untuk kontrol posisi */
.sign-in-wrapper {
  margin-bottom: 4px; /* DIKURANGI dari 6px */
  transform: translateY(-5px); /* DIGESER KE ATAS */
}

.login-title {
  font-size: 1.7rem;
  color: #f8f4ed;
  font-weight: 700;
  font-family: 'Poppins', sans-serif;
  text-shadow: 
    0 2px 4px rgba(0, 0, 0, 0.5),
    0 0 20px rgba(184, 124, 124, 0.2);
  letter-spacing: -0.01em;
  margin: 0; /* Hapus margin bottom */
}

.login-subtitle {
  font-size: 0.85rem;
  color: rgba(248, 244, 237, 0.85);
  margin: 0;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.5);
}

/* Form Styles */
.login-form {
  display: flex;
  flex-direction: column;
  gap: 18px;
  position: relative;
  z-index: 3;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.input-label {
  display: flex;
  align-items: center;
  gap: 8px;
  color: rgba(248, 244, 237, 0.95);
  font-size: 0.9rem;
  font-weight: 500;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
}

.input-label::before {
  font-family: 'Material Icons';
  font-size: 18px;
}

.icon-user::before {
  content: "person";
  color: #d8a0a5;
}

.icon-lock::before {
  content: "lock";
  color: #d8a0a5;
}

.icon-error::before {
  content: "error";
  color: #ff7b7b;
}

.icon-info::before {
  content: "info";
  color: #d8a0a5;
}

.styled-input {
  padding: 15px 18px;
  background: rgba(18, 15, 12, 0.9);
  border: 1px solid rgba(184, 124, 124, 0.35);
  border-radius: 14px;
  color: #f8f4ed;
  font-size: 1rem;
  transition: all 0.3s ease;
  outline: none;
  box-shadow: 
    inset 0 2px 4px rgba(0, 0, 0, 0.3),
    0 1px 0 rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(5px);
}

.styled-input:focus {
  border-color: #b87c7c;
  box-shadow: 
    0 0 0 3px rgba(184, 124, 124, 0.25),
    inset 0 2px 4px rgba(0, 0, 0, 0.3);
  background: rgba(22, 18, 15, 0.95);
  transform: translateY(-1px);
}

.styled-input::placeholder {
  color: rgba(248, 244, 237, 0.4);
}

/* Login Button dengan efek timbul */
.login-button {
  padding: 16px;
  background: linear-gradient(
    145deg,
    #b87c7c 0%,
    #983944 100%
  );
  color: #f8f4ed;
  border: none;
  border-radius: 14px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 48px;
  box-shadow: 
    0 8px 20px rgba(152, 61, 68, 0.4),
    0 4px 6px rgba(0, 0, 0, 0.3),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
  position: relative;
  overflow: hidden;
  z-index: 1;
}

.login-button::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(
    145deg,
    rgba(255, 255, 255, 0.1) 0%,
    transparent 50%,
    rgba(0, 0, 0, 0.1) 100%
  );
  border-radius: 14px;
  z-index: -1;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.login-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 
    0 12px 25px rgba(152, 61, 68, 0.5),
    0 6px 8px rgba(0, 0, 0, 0.4),
    inset 0 1px 0 rgba(255, 255, 255, 0.3);
  background: linear-gradient(
    145deg,
    #c58c8c 0%,
    #a54954 100%
  );
}

.login-button:hover:not(:disabled)::before {
  opacity: 1;
}

.login-button:active:not(:disabled) {
  transform: translateY(0);
  box-shadow: 
    0 4px 10px rgba(152, 61, 68, 0.4),
    0 2px 4px rgba(0, 0, 0, 0.3),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
}

.login-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

/* Loading Spinner */
.loading-spinner {
  width: 20px;
  height: 20px;
  border: 3px solid rgba(248, 244, 237, 0.3);
  border-radius: 50%;
  border-top-color: #f8f4ed;
  animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Error Message */
.error-message {
  margin-top: 18px;
  padding: 14px 18px;
  background: linear-gradient(135deg, 
    rgba(152, 57, 68, 0.2) 0%, 
    rgba(152, 57, 68, 0.1) 100%);
  border: 1px solid rgba(152, 57, 68, 0.4);
  border-radius: 14px;
  color: #ff9e9e;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  gap: 10px;
  animation: slideIn 0.3s ease;
  backdrop-filter: blur(5px);
  box-shadow: 
    inset 0 1px 0 rgba(255, 255, 255, 0.1),
    0 4px 12px rgba(152, 57, 68, 0.2);
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Login Footer */
.login-footer {
  margin-top: 25px;
  text-align: center;
  padding-top: 18px;
  border-top: 1px solid rgba(248, 244, 237, 0.15);
  position: relative;
  z-index: 3;
}

.footer-text {
  color: rgba(248, 244, 237, 0.7);
  font-size: 0.8rem;
  margin: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
}

/* Background Decoration dengan efek blur */
.background-decoration {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
  overflow: hidden;
  z-index: 0;
}

.bg-circle {
  position: absolute;
  border-radius: 50%;
}

.bg-circle.blurred {
  background: radial-gradient(circle, 
    rgba(184, 124, 124, 0.1) 0%, 
    transparent 70%);
  filter: blur(40px);
}

.bg-circle.blurred:nth-child(1) {
  width: 400px;
  height: 400px;
  top: 10%;
  left: 5%;
  opacity: 0.4;
}

.bg-circle.blurred:nth-child(2) {
  width: 300px;
  height: 300px;
  bottom: 15%;
  right: 10%;
  opacity: 0.3;
}

.bg-circle.blurred:nth-child(3) {
  width: 200px;
  height: 200px;
  top: 60%;
  left: 75%;
  opacity: 0.25;
}

.bg-circle.blurred:nth-child(4) {
  width: 250px;
  height: 250px;
  top: 30%;
  right: 70%;
  opacity: 0.2;
}

.bg-circle.blurred:nth-child(5) {
  width: 350px;
  height: 350px;
  bottom: 40%;
  left: 60%;
  opacity: 0.15;
}

/* Responsive Design */
@media (max-width: 768px) {
  .login-container {
    padding: 30px 15px 15px;
    backdrop-filter: blur(3px);
  }

  .login-card {
    padding: 30px 25px;
    backdrop-filter: blur(15px);
  }

  .card-glow {
    filter: blur(15px);
  }

  .sign-in-wrapper {
    margin-bottom: 3px;
    transform: translateY(-4px);
  }

  .bg-circle.blurred:nth-child(1),
  .bg-circle.blurred:nth-child(5) {
    width: 300px;
    height: 300px;
  }

  .bg-circle.blurred:nth-child(2),
  .bg-circle.blurred:nth-child(4) {
    width: 200px;
    height: 200px;
  }

  .bg-circle.blurred:nth-child(3) {
    width: 150px;
    height: 150px;
  }
}

@media (max-width: 480px) {
  .login-container {
    padding-top: 25px;
  }
  
  .login-card {
    padding: 25px 20px;
    backdrop-filter: blur(12px);
  }
  
  .card-glow {
    top: -10px;
    left: -10px;
    right: -10px;
    bottom: -10px;
    filter: blur(12px);
  }
  
  .sign-in-wrapper {
    margin-bottom: 2px;
    transform: translateY(-3px);
  }
}

/* Untuk layar yang sangat kecil (tinggi kurang dari 700px) */
@media (max-height: 700px) {
  .login-container {
    padding-top: 20px;
    padding-bottom: 15px;
  }
  
  .login-card {
    padding: 25px 20px;
    backdrop-filter: blur(15px);
  }
  
  .sign-in-wrapper {
    margin-bottom: 2px;
    transform: translateY(-4px);
  }
}
</style>