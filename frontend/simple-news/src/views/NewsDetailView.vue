<template>
  <div v-if="news">
    <h2>{{ news.title }}</h2>
    <h3>{{ news.section }}</h3>
    <img :src="API_URL + news.image" alt="Imagen de la noticia" v-if="news.image" />
    <p>{{ news.content }}</p>
    autor: {{ authorName || 'Desconocido' }}
    <p>Fecha: {{ news.date_published ? new Date(news.date_published).toLocaleDateString() : 'Fecha desconocida' }}</p>
  </div>
  <div v-else>Cargando...</div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { API_URL } from '../models/newsModel'
import { fetchNewsById } from '../services/newsService'
import { getAuthorName } from '../services/authorService'
import type { News } from '../models/newsModel'

const route = useRoute()
const news = ref<News | null>(null)
const authorName = ref('')


async function loadNews() {
  news.value = await fetchNewsById(Number(route.params.id))
  if (news.value && news.value.author_id !== undefined) {
    authorName.value = await getAuthorName(Number(news.value.author_id))
  }
}

onMounted(loadNews)

// Vuelve a cargar la noticia si cambia la ruta
watch(
  () => route.params.id,
  () => {
    loadNews() // Solo recarga datos, no redirige
  }
)
</script>