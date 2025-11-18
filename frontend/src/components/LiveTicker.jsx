import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import axios from 'axios'

export default function LiveTicker() {
  const [plates, setPlates] = useState([])
  const [currentIndex, setCurrentIndex] = useState(0)

  useEffect(() => {
    fetchRecentPlates()
    const interval = setInterval(fetchRecentPlates, 10000) // Refresh every 10 seconds
    return () => clearInterval(interval)
  }, [])

  useEffect(() => {
    if (plates.length > 0) {
      const interval = setInterval(() => {
        setCurrentIndex((prev) => (prev + 1) % plates.length)
      }, 3000) // Change plate every 3 seconds
      return () => clearInterval(interval)
    }
  }, [plates])

  const fetchRecentPlates = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/plates?limit=10')
      setPlates(response.data)
    } catch (error) {
      console.error('Error fetching plates:', error)
    }
  }

  const currentPlate = plates[currentIndex]

  return (
    <div className="bg-dark-800 border border-dark-600 rounded-xl p-4 overflow-hidden">
      <div className="flex items-center justify-between mb-2">
        <h3 className="text-sm font-bold text-gray-400">CANLI GİRİŞLER</h3>
        <div className="flex items-center space-x-1">
          <div className="w-2 h-2 bg-red-500 rounded-full pulse-glow"></div>
          <span className="text-xs text-gray-500">CANLI</span>
        </div>
      </div>

      <div className="relative h-16 flex items-center">
        {plates.length === 0 ? (
          <div className="text-center w-full text-gray-500 text-sm">
            Son giriş bekleniyor...
          </div>
        ) : (
          <motion.div
            key={currentIndex}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.5 }}
            className="w-full"
          >
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-4">
                <div className="bg-gradient-to-br from-blue-500 to-blue-700 px-6 py-2 rounded-lg">
                  <span className="text-2xl font-bold font-mono">
                    {currentPlate?.plate_number || '--'}
                  </span>
                </div>
                <div>
                  <p className="text-xs text-gray-400">Kamera</p>
                  <p className="text-sm font-semibold">{currentPlate?.camera_id || '-'}</p>
                </div>
                <div>
                  <p className="text-xs text-gray-400">Güven</p>
                  <p className="text-sm font-semibold text-green-400">
                    {currentPlate?.confidence ? `${(currentPlate.confidence * 100).toFixed(0)}%` : '-'}
                  </p>
                </div>
                <div>
                  <p className="text-xs text-gray-400">Motor</p>
                  <p className="text-sm font-semibold text-blue-400">
                    {currentPlate?.ocr_engine || '-'}
                  </p>
                </div>
              </div>
              <div className="text-right">
                <p className="text-xs text-gray-400">Sıra</p>
                <p className="text-sm font-bold">{currentIndex + 1} / {plates.length}</p>
              </div>
            </div>
          </motion.div>
        )}
      </div>
    </div>
  )
}