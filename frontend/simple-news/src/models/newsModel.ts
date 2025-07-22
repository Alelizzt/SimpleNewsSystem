export const API_URL = import.meta.env.VITE_API_URL;

export interface News {
  id: number
  title: string
  content: string
  section?: string
  author_id?: number | string
  image?: string
  date_published?: string
}