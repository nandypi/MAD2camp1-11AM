<script setup>
import { RouterLink } from 'vue-router'
</script>

<template>
  <main class="home">
    <div class="card">
      <h1>Welcome to My Project</h1>

      <p>
        A simple authentication application built with Vue.js.
      </p>

      <div class="buttons">
        <RouterLink to="/login" class="btn primary">
          Login
        </RouterLink>

        <RouterLink to="/register" class="btn secondary">
          Register
        </RouterLink>
      </div>
    </div>
  </main>
</template>

<style scoped>
.home {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #f4f6f8;
}

.card {
  background: white;
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 10px 25px rgba(0,0,0,0.1);
  text-align: center;
  max-width: 500px;
}

h1 {
  margin-bottom: 15px;
}

p {
  color: #666;
  margin-bottom: 25px;
}

.buttons {
  display: flex;
  justify-content: center;
  gap: 15px;
}

.btn {
  text-decoration: none;
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: bold;
}

.primary {
  background: #2563eb;
  color: white;
}

.primary:hover {
  background: #1d4ed8;
}

.secondary {
  border: 2px solid #2563eb;
  color: #2563eb;
}

.secondary:hover {
  background: #eff6ff;
}
</style>