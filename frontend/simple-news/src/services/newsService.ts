import { useAuthStore } from '../stores/authStore';
import { API_URL } from '../models/newsModel';


export async function createNews(tittle: string, content: string, section: string, author: number, imageFile: File): Promise<any> {
  const auth = useAuthStore();

  const formData = new FormData();
  formData.append('title', tittle)
  formData.append('content', content)
  formData.append('section', section)
  console.log(author, typeof author);
  formData.append('author', String(author))
  formData.append('image', imageFile);

  try {
    const response = await fetch(`${API_URL}news/`, {
      method: 'POST',
      headers: auth.token ? { Authorization: `Bearer ${auth.token}` } : undefined,
      body: formData,
    });

    const data = await response.json();

    if (!response.ok) {
      // Lanza el mensaje de error del backend si existe
      throw new Error(
        data.detail?.[0]?.msg || data.detail || 'Failed to create news with status: ' + response.status
      );
    }

    return data;
  } catch (error) {
    alert('Error creating news: ' + (error instanceof Error ? error.message : 'Unknown error'));
    console.error('Error creating news:', error);
    throw error;
  }
}

export async function fetchNews(page = 1, limit = 10) {
  const response = await fetch(`${API_URL}news/?page=${page}&limit=${limit}`, {
    headers: { accept: 'application/json' }
  });
  if (!response.ok) {
    throw new Error('Error al cargar noticias');
  }
  return await response.json();
}