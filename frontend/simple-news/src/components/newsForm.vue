<template>
    <form id="news-form" @submit.prevent="handleNewsSubmit">
        <h3>Crear Noticia</h3>
        <label for="title">Título:</label>
        <input type="text" id="title" name="title" v-model="news.title" required>
        <label for="content">Contenido:</label>
        <textarea id="content" name="content" v-model="news.content" required></textarea>
        <label for="section">Seccion:</label>
        <select id="section" name="section" v-model="news.section" required>
            <option value="sports">Deportes</option>
            <option value="politics">Politica</option>
            <option value="social">Sociedad</option>
            <option value="international">Internacional</option>
            <option value="health">Salud</option>
        </select>
        <label for="image">Imagen:</label>
        <input type="file" id="image" name="image" @change="onFileChange" accept="image/png, image/jpeg" />
        <button type="submit">Enviar</button>
    </form>
</template>
<script setup lang="ts">
import { ref, computed } from 'vue'
import { useAuthStore } from '../stores/authStore'
import { jwtDecode } from 'jwt-decode'
import { createNews } from '../services/newsService'
import type { News } from '../models/newsModel'

const auth = useAuthStore()

const news = ref({
  title: '',
  content: '',
  section: '',
})

const idAuthor = computed(() => {
  if (!auth.token) return null
  try {
    const decoded: any = jwtDecode(auth.token)
    return decoded.id || null
  } catch {
    return null
  }
})

async function handleNewsSubmit() {
  if (!imageFile.value) {
    alert('Por favor, selecciona una imagen.')
    return
  }

  try {

    const data = await createNews(news.value.title, news.value.content, news.value.section, idAuthor.value, imageFile.value)

    console.log('Noticia creada:', data)
    alert('Noticia enviada exitosamente')

  } catch (error) {
    console.error('Error al enviar la noticia:', error)
    alert('Error al enviar la noticia')
  }
}


const imageFile = ref<File | null>(null)

function onFileChange(e: Event) {
  const target = e.target as HTMLInputElement
  if (target.files && target.files.length > 0) {
    imageFile.value = target.files[0]
  }
}

</script>
<style></style>