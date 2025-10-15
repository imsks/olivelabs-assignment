'use client'

import { useState } from 'react'
import { QueryPanel } from '@/components/query/QueryPanel'
import { ResultsView } from '@/components/results/ResultsView'
import { ExplainDrawer } from '@/components/explainability/ExplainDrawer'
import { useQueryStore } from '@/store/query-store'

export default function HomePage() {
  const { currentQuery, results, explain, isLoading } = useQueryStore()
  const [showExplain, setShowExplain] = useState(false)

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-semibold text-gray-900">
                NLQ Full-Stack App
              </h1>
            </div>
            <div className="flex items-center space-x-4">
              <button
                onClick={() => setShowExplain(!showExplain)}
                className="btn-secondary"
                disabled={!explain}
              >
                {showExplain ? 'Hide' : 'Show'} Explanation
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Query Panel */}
          <div className="lg:col-span-1">
            <QueryPanel />
          </div>

          {/* Results */}
          <div className="lg:col-span-2">
            <ResultsView />
          </div>
        </div>
      </main>

      {/* Explain Drawer */}
      {showExplain && explain && (
        <ExplainDrawer
          explain={explain}
          onClose={() => setShowExplain(false)}
        />
      )}
    </div>
  )
}
