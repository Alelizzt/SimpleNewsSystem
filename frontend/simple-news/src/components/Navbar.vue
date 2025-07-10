<template>
  <nav>
    <ul>
      <li><RouterLink to="/">Home</RouterLink></li>
      <li v-if="isLoggedIn"><RouterLink to="/dashboard">Dashboard</RouterLink></li>
      <li v-if="!isLoggedIn"><RouterLink to="/login">Login</RouterLink></li>
      <li v-if="!isLoggedIn"><RouterLink to="/register">Register</RouterLink></li>
    </ul>
  </nav>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router'
import { useAuthStore } from '../stores/authStore'
import { computed } from 'vue'

const auth = useAuthStore()
const isLoggedIn = computed(() => !!auth.token)
</script>

<style scoped>
nav {
  background: #fff;
  border-bottom: 2px solid #121212;
  padding: 0.5rem 0;
}

ul {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 2.5rem;
  list-style: none;
  margin: 0;
  padding: 0;
}

li {
  margin: 0;
}

a, .router-link-active, .router-link-exact-active {
  font-family: 'PT Serif', Georgia, 'Times New Roman', Times, serif;
  font-size: 1.15rem;
  color: #121212;
  text-decoration: none;
  font-weight: 500;
  letter-spacing: 0.5px;
  padding-bottom: 0.2rem;
  transition: color 0.2s, border-bottom 0.2s;
  border-bottom: 2px solid transparent;
}

a.router-link-exact-active {
  border-bottom: 2px solid #e63946;
  color: #e63946;
}

a:hover {
  color: #e63946;
}

@media (max-width: 700px) {
  ul {
    gap: 1.2rem;
  }
  a, .router-link-active, .router-link-exact-active {
    font-size: 1rem;
  }
}
</style>