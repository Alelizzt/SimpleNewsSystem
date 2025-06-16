<template>
  <h2>Awesome Dashboard</h2>
  <button @click="logout">Cerrar sesión</button>

  <NewsForm :newsToEdit="newsToEdit" />

</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { logout } from '../services/authService'
import { fetchNewsById } from '../services/newsService'
import NewsForm from '../components/newsForm.vue'
import type { News } from '../models/newsModel'

const route = useRoute()
const newsToEdit = ref<News | undefined>(undefined)


onMounted(async () => {
  if (route.params.id) {
    newsToEdit.value = await fetchNewsById(Number(route.params.id))
  }
})
</script>

<style></style>