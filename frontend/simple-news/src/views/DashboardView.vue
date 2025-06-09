<template>
  <div>
    <h2>Awesome Dashboard</h2>
    <p v-if="username">Bienvenido, {{ username }}!</p>
    <p v-else>No se pudo obtener el usuario.</p>
    <button @click="logout">Cerrar sesión</button>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useAuthStore } from '../stores/auth'
import { jwtDecode } from 'jwt-decode'
import { logout } from '../services/authService'

const auth = useAuthStore()

const username = computed(() => {
  if (!auth.token) return null
  try {
    const decoded: any = jwtDecode(auth.token)
    return decoded.username || decoded.sub || null
  } catch {
    return null
  }
})

</script>

<style>

</style>