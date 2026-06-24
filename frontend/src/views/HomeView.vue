<script setup>
import { RouterLink } from 'vue-router'
import TheWelcome from '../components/TheWelcome.vue'
</script>

<template>

  <main>
    <!-- <TheWelcome /> -->
    <h1>Welcome to My Project</h1>

    <RouterLink to="/login">Login</RouterLink>
    <br>
    <RouterLink to="/register">Register</RouterLink>

  </main>
</template>
