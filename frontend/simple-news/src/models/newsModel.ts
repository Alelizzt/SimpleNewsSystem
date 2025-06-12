export interface News {
  id: number
  title: string
  content: string
  section?: string
  author?: number | string
  image_url?: string
  // agrega otros campos según tu API
}