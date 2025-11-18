import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import StatsHeader from '../components/StatsHeader'
import CameraBox from '../components/CameraBox'
import LastLogsPanel from '../components/LastLogsPanel'
import LiveTicker from '../components/LiveTicker'
import { cameraAPI, plateAPI } from '../utils/api'
import toast from 'react-hot-toast'

export default function Dashboard() {
  const [cameras, setCameras] = useState([])
  const [stats, setStats] = useState({
    activeCameras: 0,
    todayPlates: 0,
    totalPlates: 0,
    blacklistAlerts: 0,
  })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    try {
      const [camerasRes, platesStatsRes] = await Promise.all([
        cameraAPI.getAll(),
        plateAPI.getStats(),
      ])

      setCameras(camerasRes.data.slice(0, 4)) // Show only first 4 cameras
      setStats({
        activeCameras: camerasRes.data.filter(c => c.is_active).length,
        todayPlates: platesStatsRes.data.today_plates || 0,
        totalPlates: platesStatsRes.data.total_plates || 0,
        blacklistAlerts: 0, // TODO: Implement blacklist
      })
      setLoading(false)
    } catch (error) {
      console.error('Error fetching data:', error)
      toast.error('Veri yüklenirken hata oluştu')
      setLoading(false)
    }
  }

  const handleStartCamera = async (cameraId) => {
    try {
      await cameraAPI.start(cameraId)
      toast.success('Kamera başlatıldı')
    } catch (error) {
      console.error('Error starting camera:', error)
      toast.error('Kamera başlatılamadı')
    }
  }

  const handleStopCamera = async (cameraId) => {
    try {
      await cameraAPI.stop(cameraId)
      toast.success('Kamera durduruldu')
    } catch (error) {
      console.error('Error stopping camera:', error)
      toast.error('Kamera durdurulamadı')
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="animate-spin w-16 h-16 border-4 border-primary-500 border-t-transparent rounded-full"></div>
      </div>
    )
  }

  return (
    <div className="flex-1 overflow-y-auto p-6">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="space-y-6"
      >
        {/* Header */}
        <div>
          <h1 className="text-3xl font-bold mb-2">Dashboard</h1>
          <p className="text-gray-400">EvoPlate Enterprise - Plaka Tanıma Sistemi</p>
        </div>

        {/* Stats */}
        <StatsHeader stats={stats} />

        {/* Live Ticker */}
        <LiveTicker />

        {/* Main Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Camera Grid (2/3) */}
          <div className="lg:col-span-2">
            <div className="bg-dark-800 border border-dark-600 rounded-xl p-4">
              <h2 className="text-xl font-bold mb-4">Canlı Kameralar (2x2)</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {cameras.length > 0 ? (
                  cameras.map((camera) => (
                    <CameraBox
                      key={camera.id}
                      camera={camera}
                      onStart={handleStartCamera}
                      onStop={handleStopCamera}
                    />
                  ))
                ) : (
                  <div className="col-span-2 text-center py-12 text-gray-500">
                    Henüz kamera eklenmemiş
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Logs Panel (1/3) */}
          <div className="lg:col-span-1">
            <LastLogsPanel />
          </div>
        </div>
      </motion.div>
    </div>
  )
}