<template>
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
import { useAuthStore } from '../stores/authStore'
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

<style scoped>
#login-form {
  max-width: 350px;
  margin: 3rem auto;
  padding: 2rem 2.5rem 1.5rem 2.5rem;
  background: #fff;
  border: 1px solid #e2e2e2;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
}

#login-form label {
  font-family: 'PT Serif', Georgia, 'Times New Roman', Times, serif;
  font-size: 1.08rem;
  color: #222;
  margin-bottom: 0.2rem;
  letter-spacing: 0.5px;
}

#login-form input[type="text"],
#login-form input[type="password"] {
  font-family: 'PT Serif', Georgia, 'Times New Roman', Times, serif;
  font-size: 1.08rem;
  padding: 0.5rem 0.7rem;
  border: 1px solid #d3d3d3;
  border-radius: 4px;
  background: #fafafa;
  color: #222;
  transition: border 0.2s;
}

#login-form input:focus {
  border: 1.5px solid #e63946;
  outline: none;
  background: #fff;
}

#login-form button[type="submit"] {
  margin-top: 0.5rem;
  padding: 0.6rem 0;
  font-family: 'PT Serif', Georgia, 'Times New Roman', Times, serif;
  font-size: 1.1rem;
  font-weight: 700;
  background: #e63946;
  color: #fff;
  border: none;
  border-radius: 4px;
  letter-spacing: 1px;
  cursor: pointer;
  transition: background 0.2s;
}

#login-form button[type="submit"]:hover {
  background: #a4161a;
}

@media (max-width: 500px) {
  #login-form {
    padding: 1.2rem 0.7rem;
    max-width: 98vw;
  }
}
</style>