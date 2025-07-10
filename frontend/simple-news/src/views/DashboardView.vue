<template>
  <div class="dashboard-header">
    <h2>Awesome Dashboard</h2>
    <button class="logout-btn" @click="logout">Cerrar sesión</button>
  </div>
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

<style scoped>
.dashboard-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 900px;
  margin: 2.5rem auto 1.5rem auto;
  padding: 0 2.5rem;
}

h2 {
  font-family: 'PT Serif', Georgia, 'Times New Roman', Times, serif;
  font-size: 2.2rem;
  font-weight: 700;
  color: #121212;
  letter-spacing: 1px;
  margin: 0;
}

.logout-btn {
  padding: 0.5rem 1.5rem;
  font-family: 'PT Serif', Georgia, 'Times New Roman', Times, serif;
  font-size: 1.05rem;
  font-weight: 700;
  background: #e63946;
  color: #fff;
  border: none;
  border-radius: 4px;
  letter-spacing: 1px;
  cursor: pointer;
  transition: background 0.2s;
}

.logout-btn:hover {
  background: #a4161a;
}

@media (max-width: 1000px) {
  .dashboard-header {
    max-width: 98vw;
    padding: 0 0.7rem;
  }
  h2 {
    font-size: 1.3rem;
  }
}
</style>