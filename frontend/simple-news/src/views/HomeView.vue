<template>
  <div>
    <h2>Noticias</h2>
    <ul>
      <li v-for="news in newsList" :key="news.id">
        <strong>{{ news.title }}</strong>
        <p>
          {{ news.content.length > 200 ? news.content.slice(0, 200) + '...' : news.content }}
          <template v-if="news.content.length > 200">
            <router-link :to="`/news/${news.id}`">Ver más</router-link>
          </template>
        </p>
      </li>
    </ul>
    <div v-if="loading">Cargando...</div>
    <div v-if="error">{{ error }}</div>

    <!-- Paginador -->
    <div class="pagination" v-if="totalPages > 1">
      <button :disabled="page === 1" @click="changePage(page - 1)">Anterior</button>
      <span>Página {{ page }} de {{ totalPages }}</span>
      <button :disabled="page === totalPages" @click="changePage(page + 1)">Siguiente</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { fetchNews } from '../services/newsService'
import type { News } from '../models/newsModel'

const newsList = ref<News[]>([])
const loading = ref(false)
const error = ref('')
const page = ref(1)
const limit = 10
const totalPages = ref(1)

async function loadNews() {
  loading.value = true
  try {
    const data = await fetchNews(page.value, limit)
    newsList.value = data.news || data.items || []
    totalPages.value = data.total_pages || Math.ceil((data.total || 1) / limit)
  } catch (e: any) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}

function changePage(newPage: number) {
  if (newPage >= 1 && newPage <= totalPages.value) {
    page.value = newPage
  }
}

onMounted(loadNews)
watch(page, loadNews)
</script>