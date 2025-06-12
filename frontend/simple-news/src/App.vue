<template>
  <header id="header">
    <h1>
      Simple News!
    </h1>
    <p v-if="username">Bienvenido, {{ username }}!</p>
    <Navbar />
  </header>

  <main>
    <RouterView />
  </main>

  <footer>
    <p>© {{ year }} Simple News! - build with ❤️ with VueJs</p>
  </footer>

</template>
<script setup lang="ts">
import { RouterView } from 'vue-router'
import Navbar from './components/Navbar.vue'
import { useAuthStore } from './stores/authStore'
import { computed } from 'vue'
import { jwtDecode } from 'jwt-decode'

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

const year = new Date().getFullYear();
</script>

<style scoped></style>
