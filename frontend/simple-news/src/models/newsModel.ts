export const API_URL = 'http://127.0.0.1:8000/v1/';

export interface News {
  id: number
  title: string
  content: string
  section?: string
  author?: number | string
  image?: string
}