'use client'

import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, LineChart, Line, PieChart, Pie, Cell } from 'recharts'

interface ChartRendererProps {
  columns: string[]
  rows: any[][]
  chartType: string
}

export function ChartRenderer({ columns, rows, chartType }: ChartRendererProps) {
  // Transform data for charts
  const chartData = rows.map(row => {
    const dataPoint: any = {}
    columns.forEach((col, index) => {
      dataPoint[col] = row[index]
    })
    return dataPoint
  })

  // Generate colors for pie charts
  const COLORS = ['#3b82f6', '#ef4444', '#10b981', '#f59e0b', '#8b5cf6', '#06b6d4']

  const renderChart = () => {
    switch (chartType) {
      case 'bar':
        return (
          <BarChart data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey={columns[0]} />
            <YAxis />
            <Tooltip />
            <Bar dataKey={columns[1]} fill="#3b82f6" />
          </BarChart>
        )
      
      case 'line':
        return (
          <LineChart data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey={columns[0]} />
            <YAxis />
            <Tooltip />
            <Line type="monotone" dataKey={columns[1]} stroke="#3b82f6" strokeWidth={2} />
          </LineChart>
        )
      
      case 'pie':
        return (
          <PieChart margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
            <Pie
              data={chartData}
              cx="50%"
              cy="50%"
              labelLine={false}
              label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
              outerRadius={80}
              fill="#8884d8"
              dataKey={columns[1]}
            >
              {chartData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip />
          </PieChart>
        )
      
      default:
        return (
          <div className="text-center py-8 text-gray-500">
            Chart type "{chartType}" not supported
          </div>
        )
    }
  }

  if (rows.length === 0) {
    return (
      <div className="text-center py-8 text-gray-500">
        No data available for chart
      </div>
    )
  }

  return (
    <div className="h-96">
      <ResponsiveContainer width="100%" height="100%">
        {renderChart()}
      </ResponsiveContainer>
    </div>
  )
}
