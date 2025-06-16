<template>
    <form id="news-form" @submit.prevent="handleNewsSubmit">
            <h3 v-if="props.newsToEdit">Editar Noticia</h3>
            <h3 v-else>Crear Noticia</h3>
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
            <option value="culture">Cultura</option>
        </select>
        <label for="image">Imagen:</label>
        <input type="file" id="image" name="image" @change="onFileChange" accept="image/png, image/jpeg" :required="!props.newsToEdit" />
        <button type="submit">Enviar</button>
    </form>
</template>
<script setup lang="ts">
import { ref, computed, watch, defineProps } from 'vue'
import { useAuthStore } from '../stores/authStore'
import { jwtDecode } from 'jwt-decode'
import { createNews } from '../services/newsService'
import type { News } from '../models/newsModel'

const auth = useAuthStore()

const props = defineProps<{ newsToEdit?: News }>()

const news = ref<Partial<News>>({
  title: '',
  content: '',
  section: '',
  image: '',
})

const imageFile = ref<File | null>(null)

const idAuthor = computed(() => {
  if (!auth.token) return null
  try {
    const decoded: any = jwtDecode(auth.token)
    return decoded.id || null
  } catch {
    return null
  }
})

watch(
  () => props.newsToEdit,
  (val) => {
    if (val) {
      news.value = { ...val }
      imageFile.value = null // No pre-cargar imagen
    }
  },
  { immediate: true }
)

function onFileChange(e: Event) {
  const target = e.target as HTMLInputElement
  if (target.files && target.files.length > 0) {
    imageFile.value = target.files[0]
  }
}

async function handleNewsSubmit() {
  if (!imageFile.value) {
    alert('Por favor, selecciona una imagen.')
    return
  }

  try {

    const data = await createNews(news.value.title || '', news.value.content || '', news.value.section || '', idAuthor.value, imageFile.value)
    alert('Noticia enviada exitosamente')

  } catch (error) {
    console.error('Error al enviar la noticia:', error)
    alert('Error al enviar la noticia')
  }
}

</script>
<style></style>