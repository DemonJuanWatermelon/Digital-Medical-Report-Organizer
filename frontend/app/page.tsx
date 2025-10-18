'use client'

import { useState } from 'react'
import { Upload, FileText, Brain, Shield, Search, BarChart3 } from 'lucide-react'
import Header from '@/components/Header'
import UploadModal from '@/components/UploadModal'
import ReportCard from '@/components/ReportCard'
import StatsCard from '@/components/StatsCard'

export default function Home() {
  const [isUploadModalOpen, setIsUploadModalOpen] = useState(false)
  const [reports, setReports] = useState([])

  const stats = [
    { label: 'Total Reports', value: '24', icon: FileText, color: 'text-primary-400' },
    { label: 'AI Analysis', value: '18', icon: Brain, color: 'text-green-400' },
    { label: 'High Risk', value: '3', icon: Shield, color: 'text-red-400' },
    { label: 'Processed Today', value: '7', icon: BarChart3, color: 'text-blue-400' },
  ]

  return (
    <div className="min-h-screen">
      <Header onUploadClick={() => setIsUploadModalOpen(true)} />
      
      <main className="container mx-auto px-4 py-8">
        {/* Hero Section */}
        <div className="text-center mb-12">
          <h1 className="text-4xl md:text-6xl font-bold mb-6 bg-gradient-to-r from-primary-400 to-green-300 bg-clip-text text-transparent">
            Digital Medical Report Organizer
          </h1>
          <p className="text-xl text-dark-300 mb-8 max-w-3xl mx-auto">
            Transform your medical reports with AI-powered OCR, intelligent analysis, and secure organization. 
            Upload, analyze, and manage your medical documents with ease.
          </p>
          <button
            onClick={() => setIsUploadModalOpen(true)}
            className="btn-primary text-lg px-8 py-3 rounded-xl flex items-center gap-2 mx-auto"
          >
            <Upload className="w-5 h-5" />
            Upload Report
          </button>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
          {stats.map((stat, index) => (
            <StatsCard
              key={index}
              label={stat.label}
              value={stat.value}
              icon={stat.icon}
              color={stat.color}
            />
          ))}
        </div>

        {/* Recent Reports */}
        <div className="mb-12">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl font-bold text-white">Recent Reports</h2>
            <button className="text-primary-400 hover:text-primary-300 flex items-center gap-2">
              <Search className="w-4 h-4" />
              Search Reports
            </button>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {reports.length === 0 ? (
              <div className="col-span-full text-center py-12">
                <FileText className="w-16 h-16 text-dark-600 mx-auto mb-4" />
                <h3 className="text-xl font-semibold text-dark-300 mb-2">No reports yet</h3>
                <p className="text-dark-400 mb-6">Upload your first medical report to get started</p>
                <button
                  onClick={() => setIsUploadModalOpen(true)}
                  className="btn-primary"
                >
                  Upload Report
                </button>
              </div>
            ) : (
              reports.map((report, index) => (
                <ReportCard key={index} report={report} />
              ))
            )}
          </div>
        </div>
      </main>

      <UploadModal
        isOpen={isUploadModalOpen}
        onClose={() => setIsUploadModalOpen(false)}
        onUpload={(file) => {
          // Handle file upload
          console.log('Uploading file:', file)
          setIsUploadModalOpen(false)
        }}
      />
    </div>
  )
}
