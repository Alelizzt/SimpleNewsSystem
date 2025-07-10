<template>
  <div class="news-list">
    <h2>Las noticias más recientes...</h2>
    <ul>
      <li v-for="news in newsList" :key="news.id">
        <img :src="API_URL + news.image" alt="Imagen de la noticia" v-if="news.image" class="news-image" />
        <div class="news-content">
          <div class="news-title-row">
            <span class="news-title">{{ news.title }}</span>
            <span class="news-section">{{ news.section }}</span>
          </div>
          <div class="news-actions" v-if="isLoggedIn">
            <button @click="goToEdit(news.id)">📝 Editar</button>
            <button @click="handleDelete(news.id)">❌ Eliminar</button>
          </div>
          <p>
            {{ news.content.length > 200 ? news.content.slice(0, 200) + '...' : news.content }}
            <template v-if="news.content.length > 200">
              <router-link class="see-more-link" :to="`/news/${news.id}`">Ver más</router-link>
            </template>
          </p>
        </div>
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
import { fetchNews, deleteNews } from '../services/newsService'
import { useAuthStore } from '../stores/authStore'
import { useRouter } from 'vue-router'
import { computed } from 'vue'
import type { News } from '../models/newsModel'
import { API_URL } from '../models/newsModel'

const newsList = ref<News[]>([])
const loading = ref(false)
const error = ref('')
const page = ref(1)
const limit = 10
const totalPages = ref(1)
const auth = useAuthStore()
const isLoggedIn = computed(() => !!auth.token)

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

const router = useRouter()

function goToEdit(newsId: number) {
  router.push(`/dashboard/${newsId}`)
}

async function handleDelete(id: number) {
  if (!auth.token) {
    alert('Debes iniciar sesión para eliminar noticias.')
    return
  }
  if (confirm('¿Seguro que quieres eliminar esta noticia?')) {
    try {
      await deleteNews(id)
      // Recarga la lista después de eliminar
      newsList.value = newsList.value.filter(news => news.id !== id)
    } catch (error: any) {
      alert(error.message)
    }
  }
}
onMounted(loadNews)
watch(page, loadNews)
</script>

<style scoped>
.news-list {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  border-radius: 8px;
  background-color: #f9f9f9;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.news-list ul > li {
  display: flex;
  align-items: flex-start;
  gap: 1.2rem;
  margin-bottom: 1.5rem;
  background: #fff;
  border-radius: 8px;
  padding: 1.2rem 0.7rem;
  border-bottom: 1px solid #e2e2e2;
}

.news-image {
  width: 110px;
  height: 80px;
  min-width: 110px;
  min-height: 80px;
  max-width: 110px;
  max-height: 80px;
  aspect-ratio: 11/8;
  object-fit: cover;
  border-radius: 6px;
  border: 1px solid #e2e2e2;
  background: #fafafa;
  margin-right: 1.2rem;
  flex-shrink: 0;
  display: block;
}

.news-content {
  padding: 10px;
}

.news-content a {
  font-family: 'PT Serif', Georgia, 'Times New Roman', Times, serif;
  color: #25292e;
  font-weight: 600;
  text-decoration: none;
  margin-left: 0.3rem;
  transition: color 0.2s, text-decoration 0.2s;
  font-size: 1rem;
}

.news-content a:hover {
  color: #e63946;
  text-decoration: underline;
}

.news-section {
  display: inline-block;
  padding: 5px 10px;
  margin-bottom: 10px;
  border-radius: 16px;
  background-color: #787b80;
  color: white;
  font-size: 0.875rem;
}

.news-title {
  font-size: 1.5rem;
  margin: 0;
  color: #333;
}

.news-title-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.news-actions {
  margin: 10px 0;
}

.news-actions button {
  font-family: 'PT Serif', Georgia, 'Times New Roman', Times, serif;
  font-size: 1rem;
  font-weight: 600;
  margin-right: 10px;
  padding: 0.35rem 1.1rem;
  border: 1px solid #e2e2e2;
  border-radius: 4px;
  background: #fafafa;
  color: #292a2b;
  cursor: pointer;
  transition: background 0.2s, color 0.2s, border 0.2s;
}

.news-actions button:first-child {
  /* Editar */
  border-color: #007bff;
  color: #007bff;
}

.news-actions button:first-child:hover {
  background: #007bff;
  color: #fff;
  border-color: #007bff;
}

.news-actions button:last-child {
  /* Eliminar */
  border-color: #e63946;
  color: #e63946;
}

.news-actions button:last-child:hover {
  background: #e63946;
  color: #fff;
  border-color: #e63946;
}

.pagination {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 20px;
}

.pagination button {
  padding: 10px 15px;
  border: none;
  border-radius: 4px;
  background-color: #292a2b;
  color: white;
  cursor: pointer;
}

.pagination button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.see-more-link {
  font-family: 'PT Serif', Georgia, 'Times New Roman', Times, serif;
  color: #007bff;
  font-weight: 600;
  text-decoration: none;
  margin-left: 0.3rem;
  transition: color 0.2s, text-decoration 0.2s;
  font-size: 1rem;
}

.see-more-link:hover {
  color: #e63946;
  text-decoration: underline;
}
</style>