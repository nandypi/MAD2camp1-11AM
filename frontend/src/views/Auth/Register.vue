<template>
  <div class="register-page">
    <div class="register-card">
      <h1>Create Account 🚀</h1>
      <p class="subtitle">Join us by creating your account</p>

      <form @submit.prevent="Register">
        <div class="input-group">
          <label for="email">Email</label>
          <input
            v-model="email"
            required
            type="email"
            id="email"
            placeholder="Enter your email"
          />
        </div>

        <div class="input-group">
          <label for="password">Password</label>
          <input
            v-model="password"
            required
            type="password"
            id="password"
            placeholder="Create a password"
          />
        </div>

        <p v-if="message" :class="messageType" class="message">
          {{ message }}
        </p>

        <button type="submit" class="register-btn">
          Register
        </button>
      </form>

      <div class="links">
        <RouterLink to="/">← Back to Home</RouterLink>

        <p>
          Already have an account?
          <RouterLink to="/login">Login</RouterLink>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'
import { ref } from 'vue'

const email = ref('')
const password = ref('')

const message = ref('')
const messageType = ref('')

async function Register() {
  try {
    const res = await fetch('http://127.0.0.1:5000/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        email: email.value,
        password: password.value
      })
    })

    const data = await res.json()

    message.value = data.message

    if (res.ok) {
      messageType.value = 'success'
      email.value = ''
      password.value = ''
    } else {
      messageType.value = 'error'
    }
  } catch (error) {
    message.value = 'Unable to connect to server'
    messageType.value = 'error'
  }
}
</script>

<style scoped>
* {
  box-sizing: border-box;
}

.register-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #4f46e5, #2563eb);
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
}

.register-card {
  width: 100%;
  max-width: 420px;
  background: #fff;
  padding: 35px;
  border-radius: 18px;
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.15);
}

.register-card h1 {
  text-align: center;
  margin-bottom: 8px;
  color: #222;
}

.subtitle {
  text-align: center;
  color: #777;
  margin-bottom: 30px;
}

.input-group {
  margin-bottom: 18px;
}

.input-group label {
  display: block;
  margin-bottom: 6px;
  font-weight: 600;
  color: #444;
}

.input-group input {
  width: 100%;
  padding: 13px 15px;
  border: 1px solid #dcdcdc;
  border-radius: 10px;
  font-size: 15px;
  transition: 0.3s;
}

.input-group input:focus {
  outline: none;
  border-color: #2563eb;
  box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.15);
}

.register-btn {
  width: 100%;
  padding: 14px;
  margin-top: 10px;
  background: #2563eb;
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 16px;
  cursor: pointer;
  transition: 0.3s;
}

.register-btn:hover {
  background: #1d4ed8;
}

.message {
  text-align: center;
  margin: 10px 0;
  font-weight: bold;
}

.success {
  color: #16a34a;
}

.error {
  color: #dc2626;
}

.links {
  margin-top: 25px;
  text-align: center;
}

.links a {
  color: #2563eb;
  text-decoration: none;
  font-weight: 600;
}

.links a:hover {
  text-decoration: underline;
}

.links p {
  margin-top: 15px;
  color: #666;
}
</style>