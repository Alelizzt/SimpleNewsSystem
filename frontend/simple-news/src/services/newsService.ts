import { useAuthStore } from '../stores/authStore';
import { API_URL } from '../models/newsModel';


export async function createNews(tittle: string, content: string, section: string, author: number, imageFile: File): Promise<any> {
  const auth = useAuthStore();

  const formData = new FormData();
  formData.append('title', tittle)
  formData.append('content', content)
  formData.append('section', section)
  formData.append('author', String(author))
  if (imageFile) {
    formData.append('image', imageFile);
  }

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

export async function fetchNewsById(id: number) {
  const response = await fetch(`${API_URL}news/${id}`)
  if (!response.ok) throw new Error('No se pudo cargar la noticia')
  return await response.json()
}

export async function updateNews(id: number, formData: FormData) {
  const auth = useAuthStore()
  const response = await fetch(`${API_URL}news/${id}`, {
    method: 'PATCH',
    headers: {
      Authorization: `Bearer ${auth.token}`,
    },
    body: formData,
  })
  const data = await response.json()
  if (!response.ok) {
    throw new Error(data.detail?.[0]?.msg || data.detail || 'Failed to update news')
  } else {
    alert('Noticia actualizada correctamente')
  }
  return data
}


export async function getNotice(newsId: number): Promise<any> {
    try {
        const response = await fetch(`${API_URL}news/${newsId}`, {
            method: 'GET'
        });
        const data = await response.json();
        console.log('Fetched news data:', data);
        return data.username;
    } catch (error) {
        console.error('Error fetching author name:', error);
        return undefined;
    }
}


export async function deleteNews(id: number): Promise<void> {
  const auth = useAuthStore()
  const response = await fetch(`${API_URL}news/${id}`, {
    method: 'DELETE',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${auth.token}`,
    },
  })
  if (!response.ok) {
    throw new Error('No se pudo eliminar la noticia')
  }
}
