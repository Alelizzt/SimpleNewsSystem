<template>
  <div v-if="news">
    <h2>{{ news.title }}</h2>
    <h3>{{ news.section }}</h3>
    <img :src="API_URL + news.image" alt="Imagen de la noticia" v-if="news.image" />
    <p>{{ news.content }}</p>
  </div>
  <div v-else>Cargando...</div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { fetchNewsById } from '../services/newsService'
import type { News } from '../models/newsModel'
import { API_URL } from '../models/newsModel'

const route = useRoute()
const news = ref<News | null>(null)

console.log(news)

onMounted(async () => {
  news.value = await fetchNewsById(Number(route.params.id))
})
</script>