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
        <input type="file" id="image" name="image" @change="onFileChange" accept="image/png, image/jpeg" :required="!newsToEdit" />
        <button type="submit">Enviar</button>
    </form>
</template>
<script setup lang="ts">
import { ref, computed, watch, defineProps } from 'vue'
import { useAuthStore } from '../stores/authStore'
import { jwtDecode } from 'jwt-decode'
import { createNews, updateNews } from '../services/newsService'
import type { News } from '../models/newsModel'
import router from '../router'

const auth = useAuthStore()

const props = defineProps<{ newsToEdit?: News }>()

const news = ref<Partial<News>>({
  title: '',
  content: '',
  section: '',
  image: undefined,
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
  const formData = new FormData()
  formData.append('title', news.value.title || '')
  formData.append('content', news.value.content || '')
  formData.append('section', news.value.section || '')
  if (imageFile.value) {
    formData.append('image', imageFile.value)
  }

  if (!imageFile.value && !props.newsToEdit) {
    alert('Por favor, selecciona una imagen.')
    return
  }

  try {
    let noticia
    if (props.newsToEdit) {
      noticia = await updateNews(props.newsToEdit.id, formData)
      router.push('/news/' + props.newsToEdit.id)
      alert('Noticia actualizada correctamente')
    } else {
      noticia = await createNews(
        news.value.title || '',
        news.value.content || '',
        news.value.section || '',
        idAuthor.value!,
        imageFile.value!
      )
      alert('Noticia creada correctamente')
      console.log('Noticia creada:', noticia)

      // Limpia el formulario
      news.value = { title: '', content: '', section: '', image: undefined }
      imageFile.value = null
      const fileInput = document.getElementById('image') as HTMLInputElement
      if (fileInput) fileInput.value = ''

    }
  } catch (error) {
    console.error('Error al enviar la noticia:', error)
    alert('Error al enviar la noticia')
  }
}

</script>
<style scoped>
#news-form {
  max-width: 900px;
  margin: 2.5rem auto;
  background: #fff;
  border: 1px solid #e2e2e2;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  padding: 2.5rem 2.5rem 2rem 2.5rem;
  display: flex;
  flex-direction: column;
  gap: 1.3rem;
}

#news-form h3 {
  font-family: 'PT Serif', Georgia, 'Times New Roman', Times, serif;
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  color: #121212;
  letter-spacing: 1px;
  text-align: center;
}

#news-form label {
  font-family: 'PT Serif', Georgia, 'Times New Roman', Times, serif;
  font-size: 1.08rem;
  color: #222;
  margin-bottom: 0.2rem;
  letter-spacing: 0.5px;
}

#news-form input[type="text"],
#news-form select {
  font-family: 'PT Serif', Georgia, 'Times New Roman', Times, serif;
  font-size: 1.08rem;
  padding: 0.5rem 0.7rem;
  border: 1px solid #d3d3d3;
  border-radius: 4px;
  background: #fafafa;
  color: #222;
  transition: border 0.2s;
  width: 96%;
}

#news-form textarea {
  width: 96%;
  font-family: 'PT Serif', Georgia, 'Times New Roman', Times, serif;
  font-size: 1.15rem;
  padding: 0.5rem 0.8rem;
  border: 1px solid #d3d3d3;
  border-radius: 4px;
  background: #fafafa;
  color: #222;
  margin-bottom: 1.2rem;
  transition: border 0.2s;
  resize: vertical;
  min-height: 220px;
  max-height: 600px;
  line-height: 1.7;
}

#news-form input[type="file"] {
  font-size: 1rem;
  margin-top: 0.3rem;
}

#news-form button[type="submit"] {
  margin-top: 0.5rem;
  padding: 0.7rem 0;
  font-family: 'PT Serif', Georgia, 'Times New Roman', Times, serif;
  font-size: 1.1rem;
  font-weight: 700;
  background: #e63946;
  color: #fff;
  border: none;
  border-radius: 4px;
  letter-spacing: 1px;
  cursor: pointer;
  transition: background 0.2s;
}

#news-form button[type="submit"]:hover {
  background: #a4161a;
}

@media (max-width: 1000px) {
  #news-form {
    max-width: 98vw;
    padding: 1.2rem 0.7rem;
  }
  #news-form h3 {
    font-size: 1.2rem;
  }
}
</style>