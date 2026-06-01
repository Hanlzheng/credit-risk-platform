import axios from 'axios'

const client = axios.create({
  baseURL: 'http://localhost:5000',
  headers: {
    'Content-Type': 'application/json'
  }
})

client.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export const registerUser = (data) =>
  client.post('/api/v1/auth/register', data)

export const loginUser = (data) =>
  client.post('/api/v1/auth/login', data)

export const predictRisk = (data) =>
  client.post('/api/v1/predict', data)

export default client