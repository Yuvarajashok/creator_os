import axios, { AxiosInstance } from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

class ApiService {
  private api: AxiosInstance

  constructor() {
    this.api = axios.create({
      baseURL: API_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    })

    this.api.interceptors.request.use((config) => {
      const token = localStorage.getItem('token')
      if (token) {
        config.headers.Authorization = `Bearer ${token}`
      }
      return config
    })

    this.api.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          localStorage.removeItem('token')
          window.location.href = '/login'
        }
        return Promise.reject(error)
      }
    )
  }

  async register(data: { email: string; password: string; full_name: string }) {
    const response = await this.api.post('/api/v1/auth/register', data)
    return response.data
  }

  async login(username: string, password: string) {
    const formData = new FormData()
    formData.append('username', username)
    formData.append('password', password)

    const response = await this.api.post('/api/v1/auth/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    })
    return response.data
  }

  async getCurrentUser() {
    const response = await this.api.get('/api/v1/auth/me')
    return response.data
  }

  async getPages() {
    const response = await this.api.get('/api/v1/pages/')
    return response.data
  }

  async getPage(pageId: string) {
    const response = await this.api.get(`/api/v1/pages/${pageId}`)
    return response.data
  }

  async createPage(data: { instagram_username: string; bio?: string }) {
    const response = await this.api.post('/api/v1/pages/', data)
    return response.data
  }

  async updatePage(pageId: string, data: any) {
    const response = await this.api.put(`/api/v1/pages/${pageId}`, data)
    return response.data
  }

  async deletePage(pageId: string) {
    await this.api.delete(`/api/v1/pages/${pageId}`)
  }

  async getPagePosts(pageId: string) {
    const response = await this.api.get(`/api/v1/posts/page/${pageId}`)
    return response.data
  }

  async createPost(data: any) {
    const response = await this.api.post('/api/v1/posts/', data)
    return response.data
  }

  async updatePost(postId: string, data: any) {
    const response = await this.api.put(`/api/v1/posts/${postId}`, data)
    return response.data
  }

  async deletePost(postId: string) {
    await this.api.delete(`/api/v1/posts/${postId}`)
  }

  async getIntelligenceScore(pageId: string, days: number = 30) {
    const response = await this.api.get(`/api/v1/intelligence/${pageId}?days=${days}`)
    return response.data
  }
}

export default new ApiService()
