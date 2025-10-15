// API Types
export interface NLQParseRequest {
  prompt: string
  conversation_id?: string
}

export interface NLQParseResponse {
  sql: string
  warnings: string[]
  explain: ExplainObject
  conversation_id: string
}

export interface NLQExecuteRequest {
  sql: string
  result_format?: string
}

export interface NLQExecuteResponse {
  columns: string[]
  rows: any[][]
  inferred_chart?: string
}

export interface NLQQueryRequest {
  prompt: string
  conversation_id?: string
}

export interface NLQQueryResponse {
  columns: string[]
  rows: any[][]
  inferred_chart?: string
  explain: ExplainObject
  sql: string
}

export interface ExplainObject {
  filters: string[]
  groupBy: string[]
  aggregates: string[]
  sourceTables: string[]
}

export interface SchemaTable {
  name: string
  columns: Array<{
    name: string
    type: string
    description: string
  }>
}

export interface SchemaResponse {
  tables: SchemaTable[]
}

export interface ConversationRefineRequest {
  conversation_id: string
  followup: string
}

export interface ConversationRefineResponse {
  columns: string[]
  rows: any[][]
  inferred_chart?: string
  explain: ExplainObject
  sql: string
}

// Auth Types
export interface LoginRequest {
  username: string
  password: string
}

export interface RegisterRequest {
  username: string
  email: string
  password: string
}

export interface AuthResponse {
  access_token: string
  token_type: string
}

// Store Types
export interface QueryState {
  currentQuery: string
  results: NLQQueryResponse | null
  explain: ExplainObject | null
  isLoading: boolean
  error: string | null
  conversationId: string | null
}

export interface ConversationState {
  history: Array<{
    id: string
    prompt: string
    sql: string
    timestamp: Date
  }>
  currentConversationId: string | null
}
