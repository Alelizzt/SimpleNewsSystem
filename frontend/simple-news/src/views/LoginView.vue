<template>
  Login page
  <form id="login-form" @submit.prevent="handleLogin">
    <label for="username">Username:</label>
    <input type="text" id="username" name="username" v-model="form.username" required>
    <label for="password">Password:</label>
    <input type="password" id="password" name="password" v-model="form.password" required>
    <button type="submit">Login</button>
  </form>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'
import { login } from '../services/authService'

const router = useRouter()
const form = ref({
  username: '',
  password: ''
})

async function handleLogin() {
  try {
    const auth = useAuthStore()
    const data = await login(form.value.username, form.value.password)
    if (data.access_token) {
        auth.setToken(data.access_token)
        router.push('/dashboard')
    } else {
        console.error('Login failed: No token received')
    }
  } catch (error) {
    console.error('Error al iniciar sesión', error)
  }
}
</script>