import React, { useState, useEffect } from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import Dashboard from './pages/Dashboard'
import Cameras from './pages/Cameras'
import Plates from './pages/Plates'
import Gates from './pages/Gates'
import Sites from './pages/Sites'
import Settings from './pages/Settings'
import SideMenu from './components/SideMenu'

function App() {
  const [sidebarOpen, setSidebarOpen] = useState(true)

  return (
    <BrowserRouter>
      <div className="flex h-screen bg-dark-900 text-gray-100">
        {/* Sidebar */}
        <SideMenu isOpen={sidebarOpen} setIsOpen={setSidebarOpen} />
        
        {/* Main Content */}
        <div className="flex-1 flex flex-col overflow-hidden">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/cameras" element={<Cameras />} />
            <Route path="/plates" element={<Plates />} />
            <Route path="/gates" element={<Gates />} />
            <Route path="/sites" element={<Sites />} />
            <Route path="/settings" element={<Settings />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </div>
        
        {/* Toast Notifications */}
        <Toaster
          position="top-right"
          toastOptions={{
            duration: 3000,
            style: {
              background: '#1a1a1a',
              color: '#fff',
              border: '1px solid #3a3a3a',
            },
          }}
        />
      </div>
    </BrowserRouter>
  )
}

export default App