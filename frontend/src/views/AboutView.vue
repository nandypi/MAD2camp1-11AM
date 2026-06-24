<template>

  <RouterLink to="/">Go to Home</RouterLink>
  <div class="about">
    <h1>This is an about page!</h1>

    <h2 id="message">...</h2>
    
    <button @click="greetUser()">Greet Me</button>
  </div>

</template>

<script setup>
import { RouterLink } from 'vue-router';

async function greetUser() {
    let message = document.getElementById("message")
    let res = await fetch('http://127.0.0.1:5000/hello')
    const data = await res.json()
    message.innerText = data.message
}

</script>

<style>

</style>
