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

<style>

</style>