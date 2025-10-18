'use client'

import { useState, useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import { X, Upload, FileImage, AlertCircle } from 'lucide-react'

interface UploadModalProps {
  isOpen: boolean
  onClose: () => void
  onUpload: (file: File) => void
}

export default function UploadModal({ isOpen, onClose, onUpload }: UploadModalProps) {
  const [uploading, setUploading] = useState(false)
  const [error, setError] = useState('')

  const onDrop = useCallback((acceptedFiles: File[]) => {
    const file = acceptedFiles[0]
    if (file) {
      // Validate file type
      if (!file.type.startsWith('image/')) {
        setError('Please upload an image file (JPG, PNG, etc.)')
        return
      }
      
      // Validate file size (10MB max)
      if (file.size > 10 * 1024 * 1024) {
        setError('File size must be less than 10MB')
        return
      }
      
      setError('')
      setUploading(true)
      
      // Simulate upload process
      setTimeout(() => {
        onUpload(file)
        setUploading(false)
      }, 2000)
    }
  }, [onUpload])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png', '.gif', '.bmp', '.tiff']
    },
    multiple: false
  })

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-dark-800 rounded-lg max-w-md w-full max-h-[90vh] overflow-y-auto">
        <div className="flex items-center justify-between p-6 border-b border-dark-700">
          <h2 className="text-xl font-semibold text-white">Upload Medical Report</h2>
          <button
            onClick={onClose}
            className="text-dark-400 hover:text-white transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="p-6">
          <div
            {...getRootProps()}
            className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors ${
              isDragActive
                ? 'border-primary-500 bg-primary-500 bg-opacity-10'
                : 'border-dark-600 hover:border-primary-500'
            }`}
          >
            <input {...getInputProps()} />
            <Upload className="w-12 h-12 text-dark-400 mx-auto mb-4" />
            {isDragActive ? (
              <p className="text-primary-400">Drop the file here...</p>
            ) : (
              <div>
                <p className="text-dark-300 mb-2">
                  Drag & drop a medical report image here, or click to select
                </p>
                <p className="text-sm text-dark-400">
                  Supports: JPG, PNG, GIF, BMP, TIFF (Max 10MB)
                </p>
              </div>
            )}
          </div>

          {error && (
            <div className="mt-4 p-3 bg-red-900 bg-opacity-20 border border-red-500 rounded-lg flex items-center gap-2">
              <AlertCircle className="w-4 h-4 text-red-400" />
              <span className="text-red-400 text-sm">{error}</span>
            </div>
          )}

          {uploading && (
            <div className="mt-4 p-3 bg-primary-900 bg-opacity-20 border border-primary-500 rounded-lg">
              <div className="flex items-center gap-2">
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-primary-400"></div>
                <span className="text-primary-400 text-sm">Processing your report...</span>
              </div>
            </div>
          )}

          <div className="mt-6 flex gap-3">
            <button
              onClick={onClose}
              className="flex-1 btn-secondary"
              disabled={uploading}
            >
              Cancel
            </button>
            <button
              onClick={() => {
                const input = document.querySelector('input[type="file"]') as HTMLInputElement
                input?.click()
              }}
              className="flex-1 btn-primary"
              disabled={uploading}
            >
              {uploading ? 'Processing...' : 'Choose File'}
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
