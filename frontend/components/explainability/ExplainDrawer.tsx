'use client'

import { X, Database, Filter, Group, BarChart3 } from 'lucide-react'
import type { ExplainObject } from '@/types/api'

interface ExplainDrawerProps {
  explain: ExplainObject
  onClose: () => void
}

export function ExplainDrawer({ explain, onClose }: ExplainDrawerProps) {
  return (
    <div className="fixed inset-0 z-50 overflow-hidden">
      <div className="absolute inset-0 bg-black bg-opacity-50" onClick={onClose} />
      
      <div className="absolute right-0 top-0 h-full w-96 bg-white shadow-xl">
        <div className="flex items-center justify-between p-4 border-b border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900">Query Explanation</h3>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600"
          >
            <X className="w-5 h-5" />
          </button>
        </div>
        
        <div className="p-4 space-y-6">
          {/* Source Tables */}
          {explain.sourceTables.length > 0 && (
            <div>
              <div className="flex items-center space-x-2 mb-3">
                <Database className="w-4 h-4 text-blue-600" />
                <h4 className="font-medium text-gray-900">Source Tables</h4>
              </div>
              <div className="space-y-1">
                {explain.sourceTables.map((table, index) => (
                  <div key={index} className="text-sm text-gray-600 bg-gray-50 px-3 py-2 rounded">
                    {table}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Filters */}
          {explain.filters.length > 0 && (
            <div>
              <div className="flex items-center space-x-2 mb-3">
                <Filter className="w-4 h-4 text-green-600" />
                <h4 className="font-medium text-gray-900">Filters Applied</h4>
              </div>
              <div className="space-y-1">
                {explain.filters.map((filter, index) => (
                  <div key={index} className="text-sm text-gray-600 bg-green-50 px-3 py-2 rounded">
                    {filter}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Group By */}
          {explain.groupBy.length > 0 && (
            <div>
              <div className="flex items-center space-x-2 mb-3">
                <Group className="w-4 h-4 text-purple-600" />
                <h4 className="font-medium text-gray-900">Grouped By</h4>
              </div>
              <div className="space-y-1">
                {explain.groupBy.map((group, index) => (
                  <div key={index} className="text-sm text-gray-600 bg-purple-50 px-3 py-2 rounded">
                    {group}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Aggregates */}
          {explain.aggregates.length > 0 && (
            <div>
              <div className="flex items-center space-x-2 mb-3">
                <BarChart3 className="w-4 h-4 text-orange-600" />
                <h4 className="font-medium text-gray-900">Aggregations</h4>
              </div>
              <div className="space-y-1">
                {explain.aggregates.map((aggregate, index) => (
                  <div key={index} className="text-sm text-gray-600 bg-orange-50 px-3 py-2 rounded">
                    {aggregate}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Human Readable Explanation */}
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <h4 className="font-medium text-blue-900 mb-2">How this query was built:</h4>
            <p className="text-sm text-blue-800">
              {generateHumanExplanation(explain)}
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}

function generateHumanExplanation(explain: ExplainObject): string {
  const parts = []
  
  if (explain.sourceTables.length > 0) {
    parts.push(`Data was retrieved from ${explain.sourceTables.join(' and ')}`)
  }
  
  if (explain.filters.length > 0) {
    parts.push(`Filtered by ${explain.filters.join(', ')}`)
  }
  
  if (explain.groupBy.length > 0) {
    parts.push(`Grouped by ${explain.groupBy.join(', ')}`)
  }
  
  if (explain.aggregates.length > 0) {
    parts.push(`Aggregated using ${explain.aggregates.join(', ')}`)
  }
  
  return parts.join('. ') + '.'
}
