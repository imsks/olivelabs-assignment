'use client'

import { useState } from 'react'
import { useQueryStore } from '@/store/query-store'
import { DataTable } from './DataTable'
import { ChartRenderer } from './ChartRenderer'
import { Table, BarChart3 } from 'lucide-react'

export function ResultsView() {
  const { results, isLoading } = useQueryStore()
  const [activeTab, setActiveTab] = useState<'table' | 'chart'>('table')

  if (isLoading) {
    return (
      <div className="card">
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600 mx-auto mb-4"></div>
            <p className="text-gray-600">Processing your query...</p>
          </div>
        </div>
      </div>
    )
  }

  if (!results) {
    return (
      <div className="card">
        <div className="text-center py-12">
          <Table className="w-12 h-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No Results Yet</h3>
          <p className="text-gray-600">
            Enter a natural language query to see results here
          </p>
        </div>
      </div>
    )
  }

  const hasChart = results.inferred_chart && results.inferred_chart !== 'null'

  return (
    <div className="card">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-lg font-semibold text-gray-900">Results</h2>
        
        {hasChart && (
          <div className="flex space-x-1 bg-gray-100 rounded-lg p-1">
            <button
              onClick={() => setActiveTab('table')}
              className={`px-3 py-1 rounded-md text-sm font-medium transition-colors ${
                activeTab === 'table'
                  ? 'bg-white text-gray-900 shadow-sm'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              <Table className="w-4 h-4 inline mr-1" />
              Table
            </button>
            <button
              onClick={() => setActiveTab('chart')}
              className={`px-3 py-1 rounded-md text-sm font-medium transition-colors ${
                activeTab === 'chart'
                  ? 'bg-white text-gray-900 shadow-sm'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              <BarChart3 className="w-4 h-4 inline mr-1" />
              Chart
            </button>
          </div>
        )}
      </div>

      {activeTab === 'table' ? (
        <DataTable 
          columns={results.columns} 
          rows={results.rows} 
        />
      ) : (
        <ChartRenderer
          columns={results.columns}
          rows={results.rows}
          chartType={results.inferred_chart || 'bar'}
        />
      )}
    </div>
  )
}
