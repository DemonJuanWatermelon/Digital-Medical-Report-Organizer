'use client'

import { useState } from 'react'
import { Menu, X, Upload, User, LogOut, Settings } from 'lucide-react'

interface HeaderProps {
  onUploadClick: () => void
}

export default function Header({ onUploadClick }: HeaderProps) {
  const [isMenuOpen, setIsMenuOpen] = useState(false)
  const [isUserMenuOpen, setIsUserMenuOpen] = useState(false)

  return (
    <header className="bg-dark-800 border-b border-dark-700 sticky top-0 z-50">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-gradient-to-r from-primary-500 to-green-400 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-sm">DM</span>
            </div>
            <span className="text-xl font-bold text-white">Medical Organizer</span>
          </div>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center space-x-8">
            <a href="#" className="text-dark-300 hover:text-white transition-colors">
              Dashboard
            </a>
            <a href="#" className="text-dark-300 hover:text-white transition-colors">
              Reports
            </a>
            <a href="#" className="text-dark-300 hover:text-white transition-colors">
              Analytics
            </a>
            <button
              onClick={onUploadClick}
              className="btn-primary flex items-center gap-2"
            >
              <Upload className="w-4 h-4" />
              Upload
            </button>
          </nav>

          {/* User Menu */}
          <div className="hidden md:flex items-center space-x-4">
            <div className="relative">
              <button
                onClick={() => setIsUserMenuOpen(!isUserMenuOpen)}
                className="flex items-center space-x-2 text-dark-300 hover:text-white transition-colors"
              >
                <div className="w-8 h-8 bg-primary-600 rounded-full flex items-center justify-center">
                  <User className="w-4 h-4" />
                </div>
                <span>John Doe</span>
              </button>
              
              {isUserMenuOpen && (
                <div className="absolute right-0 mt-2 w-48 bg-dark-700 rounded-lg shadow-lg py-2 z-50">
                  <a href="#" className="flex items-center px-4 py-2 text-dark-300 hover:bg-dark-600 hover:text-white">
                    <Settings className="w-4 h-4 mr-3" />
                    Settings
                  </a>
                  <a href="#" className="flex items-center px-4 py-2 text-dark-300 hover:bg-dark-600 hover:text-white">
                    <LogOut className="w-4 h-4 mr-3" />
                    Sign Out
                  </a>
                </div>
              )}
            </div>
          </div>

          {/* Mobile Menu Button */}
          <button
            onClick={() => setIsMenuOpen(!isMenuOpen)}
            className="md:hidden text-dark-300 hover:text-white"
          >
            {isMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </div>

        {/* Mobile Navigation */}
        {isMenuOpen && (
          <div className="md:hidden py-4 border-t border-dark-700">
            <nav className="flex flex-col space-y-4">
              <a href="#" className="text-dark-300 hover:text-white transition-colors">
                Dashboard
              </a>
              <a href="#" className="text-dark-300 hover:text-white transition-colors">
                Reports
              </a>
              <a href="#" className="text-dark-300 hover:text-white transition-colors">
                Analytics
              </a>
              <button
                onClick={onUploadClick}
                className="btn-primary flex items-center gap-2 w-full justify-center"
              >
                <Upload className="w-4 h-4" />
                Upload Report
              </button>
            </nav>
          </div>
        )}
      </div>
    </header>
  )
}
