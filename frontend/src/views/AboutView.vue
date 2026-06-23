<template>
  <div class="about">
    <h1 id="message">...</h1>
    
    <button @click="greetUser()">Greet Me</button>
  </div>

  

</template>

<script setup>

async function greetUser() {
    let message = document.getElementById("message")
    let res = await fetch('http://127.0.0.1:5000/hello')
    const data = await res.json()
    message.innerText = data.message
}

</script>

<style>
@media (min-width: 1024px) {
  .about {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
}
</style>
