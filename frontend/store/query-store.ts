import { create } from 'zustand'
import { devtools } from 'zustand/middleware'
import type { QueryState, NLQQueryResponse, ExplainObject } from '@/types/api'
import { nlqAPI } from '@/lib/api-client'

interface QueryStore extends QueryState {
  setCurrentQuery: (query: string) => void
  setResults: (results: NLQQueryResponse | null) => void
  setExplain: (explain: ExplainObject | null) => void
  setLoading: (loading: boolean) => void
  setError: (error: string | null) => void
  setConversationId: (id: string | null) => void
  executeQuery: (prompt: string) => Promise<void>
  clearResults: () => void
}

export const useQueryStore = create<QueryStore>()(
  devtools(
    (set, get) => ({
      // Initial state
      currentQuery: '',
      results: null,
      explain: null,
      isLoading: false,
      error: null,
      conversationId: null,

      // Actions
      setCurrentQuery: (query: string) => set({ currentQuery: query }),
      
      setResults: (results: NLQQueryResponse | null) => set({ results }),
      
      setExplain: (explain: ExplainObject | null) => set({ explain }),
      
      setLoading: (isLoading: boolean) => set({ isLoading }),
      
      setError: (error: string | null) => set({ error }),
      
      setConversationId: (conversationId: string | null) => set({ conversationId }),
      
      executeQuery: async (prompt: string) => {
        const { conversationId } = get()
        
        set({ isLoading: true, error: null })
        
        try {
          const response = await nlqAPI.query({
            prompt,
            conversation_id: conversationId || undefined
          })
          
          set({
            results: response,
            explain: response.explain,
            conversationId: response.conversation_id || conversationId,
            isLoading: false
          })
        } catch (error: any) {
          set({
            error: error.response?.data?.detail || 'An error occurred',
            isLoading: false
          })
        }
      },
      
      clearResults: () => set({
        results: null,
        explain: null,
        error: null
      })
    }),
    {
      name: 'query-store',
    }
  )
)
