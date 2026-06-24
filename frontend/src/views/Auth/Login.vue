<template>
    <h1>This is login page</h1>

    <RouterLink to="/">Go Home</RouterLink>
    <br>
    <p>Don't have an account? <RouterLink to="/register">Click here to register</RouterLink></p>
    
    <form @submit.prevent="Login">

        <!-- <div>{{ email}},{{ password }}</div> --> <!-- uncomment to see the vue values -->

        <input v-model="email" required type="email" name="email" id="email" placeholder="Enter your email">
        <input v-model="password" required type="password" name="password" id="password" placeholder="Enter your password...">

        <p :class="messageType">{{ message }}</p>
        <button type="submit">Submit</button>

    </form>
    
</template>

<script setup>
import { RouterLink } from 'vue-router';
import { ref } from 'vue';

let email = ref('user@gmail.com')
let password = ref('password')
let message = ref('')
let messageType = ref('')

async function Login() {
    let res = await fetch('http://127.0.0.1:5000/login', {
        method: "POST",
        body: JSON.stringify({"email": email.value, "password": password.value}),
        headers: {"Content-Type": 'application/json'}
    })
    let data = await res.json()
    message.value = data.message
    if (res.ok) {
        messageType.value = 'success'
        // console.log('token is ', data.token)
        localStorage.setItem('token', data.token)
    } else {
        messageType.value = 'error'
    }
    // console.log(data)
}

</script>

<style scoped>
.success {
    color: green;
}
.error {
    color: red;
}
</style>