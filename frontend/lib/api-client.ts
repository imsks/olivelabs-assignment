import axios from 'axios'
import type {
  NLQParseRequest,
  NLQParseResponse,
  NLQExecuteRequest,
  NLQExecuteResponse,
  NLQQueryRequest,
  NLQQueryResponse,
  SchemaResponse,
  ConversationRefineRequest,
  ConversationRefineResponse,
  LoginRequest,
  RegisterRequest,
  AuthResponse
} from '@/types/api'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

// Create axios instance
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add auth token to requests
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Handle auth errors
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// Auth API
export const authAPI = {
  login: async (data: LoginRequest): Promise<AuthResponse> => {
    const response = await apiClient.post('/api/auth/login', data)
    return response.data
  },

  register: async (data: RegisterRequest): Promise<AuthResponse> => {
    const response = await apiClient.post('/api/auth/register', data)
    return response.data
  },
}

// NLQ API
export const nlqAPI = {
  parse: async (data: NLQParseRequest): Promise<NLQParseResponse> => {
    const response = await apiClient.post('/api/nlq/parse', data)
    return response.data
  },

  execute: async (data: NLQExecuteRequest): Promise<NLQExecuteResponse> => {
    const response = await apiClient.post('/api/nlq/execute', data)
    return response.data
  },

  query: async (data: NLQQueryRequest): Promise<NLQQueryResponse> => {
    const response = await apiClient.post('/api/nlq/query', data)
    return response.data
  },
}

// Schema API
export const schemaAPI = {
  describe: async (): Promise<SchemaResponse> => {
    const response = await apiClient.get('/api/schema/describe')
    return response.data
  },
}

// Conversation API
export const conversationAPI = {
  refine: async (data: ConversationRefineRequest): Promise<ConversationRefineResponse> => {
    const response = await apiClient.post('/api/conversation/refine', data)
    return response.data
  },
}

export default apiClient
