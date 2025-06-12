<template>
  <h2>Awesome Dashboard</h2>
  <button @click="logout">Cerrar sesión</button>

  <NewsForm />

</template>

<script setup lang="ts">
import { logout } from '../services/authService'

import NewsForm from '../components/newsForm.vue'

</script>

<style></style>