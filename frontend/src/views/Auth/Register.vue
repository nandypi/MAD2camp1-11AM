<template>
    <h1>This is register page</h1>

    <RouterLink to="/">Go Home</RouterLink>
    <br>

    <p>
        Already have an account?
        <RouterLink to="/login">Click here to login</RouterLink>
    </p>

    <form @submit.prevent="Register">

        <input
            v-model="email"
            required
            type="email"
            placeholder="Enter your email"
        >

        <input
            v-model="password"
            required
            type="password"
            placeholder="Enter your password"
        >

        <p :class="messageType">{{ message }}</p>

        <button type="submit">Register</button>

    </form>
</template>

<script setup>
import { RouterLink } from 'vue-router'
import { ref } from 'vue'

let email = ref('')
let password = ref('')

let message = ref('')
let messageType = ref('')

async function Register() {
    try {
        const res = await fetch('http://127.0.0.1:5000/register', {
            method: 'POST',
            body: JSON.stringify({
                email: email.value,
                password: password.value
            }),
            headers: {
                'Content-Type': 'application/json'
            }
        })

        const data = await res.json()

        message.value = data.message

        if (res.ok) {
            messageType.value = 'success'
        } else {
            messageType.value = 'error'
        }
    } catch (error) {
        messageType.value = 'error'
        message.value = 'Unable to connect to server'
    }
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