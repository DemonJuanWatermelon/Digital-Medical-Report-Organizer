'use client'

import { FileText, Calendar, AlertTriangle, CheckCircle, Clock } from 'lucide-react'

interface Report {
  id: string
  title: string
  date: string
  status: 'processed' | 'processing' | 'error'
  riskLevel: 'low' | 'medium' | 'high'
  findings: number
}

interface ReportCardProps {
  report: Report
}

export default function ReportCard({ report }: ReportCardProps) {
  const getStatusIcon = () => {
    switch (report.status) {
      case 'processed':
        return <CheckCircle className="w-4 h-4 text-green-400" />
      case 'processing':
        return <Clock className="w-4 h-4 text-yellow-400" />
      case 'error':
        return <AlertTriangle className="w-4 h-4 text-red-400" />
      default:
        return <Clock className="w-4 h-4 text-gray-400" />
    }
  }

  const getRiskColor = () => {
    switch (report.riskLevel) {
      case 'high':
        return 'text-red-400 bg-red-900 bg-opacity-20'
      case 'medium':
        return 'text-yellow-400 bg-yellow-900 bg-opacity-20'
      case 'low':
        return 'text-green-400 bg-green-900 bg-opacity-20'
      default:
        return 'text-gray-400 bg-gray-900 bg-opacity-20'
    }
  }

  return (
    <div className="card hover:bg-dark-750 transition-colors cursor-pointer group">
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-primary-600 rounded-lg flex items-center justify-center">
            <FileText className="w-5 h-5 text-white" />
          </div>
          <div>
            <h3 className="font-semibold text-white group-hover:text-primary-400 transition-colors">
              {report.title}
            </h3>
            <div className="flex items-center gap-2 text-sm text-dark-400">
              <Calendar className="w-3 h-3" />
              {report.date}
            </div>
          </div>
        </div>
        <div className="flex items-center gap-2">
          {getStatusIcon()}
          <span className={`px-2 py-1 rounded-full text-xs font-medium ${getRiskColor()}`}>
            {report.riskLevel.toUpperCase()}
          </span>
        </div>
      </div>

      <div className="space-y-3">
        <div className="flex items-center justify-between text-sm">
          <span className="text-dark-400">Findings:</span>
          <span className="text-white font-medium">{report.findings}</span>
        </div>
        
        <div className="flex items-center justify-between text-sm">
          <span className="text-dark-400">Status:</span>
          <span className="text-white font-medium capitalize">{report.status}</span>
        </div>
      </div>

      <div className="mt-4 pt-4 border-t border-dark-700">
        <button className="w-full text-left text-primary-400 hover:text-primary-300 text-sm font-medium group-hover:underline">
          View Details →
        </button>
      </div>
    </div>
  )
}
