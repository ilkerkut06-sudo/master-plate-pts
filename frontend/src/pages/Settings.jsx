import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { settingsAPI } from '../utils/api'
import toast from 'react-hot-toast'
import { CheckCircleIcon } from '@heroicons/react/24/solid'

export default function Settings() {
  const [ocrEngines, setOcrEngines] = useState({ available_engines: [], current_engine: '', engines: [] })
  const [systemInfo, setSystemInfo] = useState({})
  const [loading, setLoading] = useState(true)
  const [selectedEngine, setSelectedEngine] = useState('')

  useEffect(() => {
    fetchSettings()
  }, [])

  const fetchSettings = async () => {
    try {
      const [enginesRes, infoRes] = await Promise.all([
        settingsAPI.getOCREngines(),
        settingsAPI.getSystemInfo(),
      ])
      setOcrEngines(enginesRes.data)
      setSystemInfo(infoRes.data)
      setSelectedEngine(enginesRes.data.current_engine)
      setLoading(false)
    } catch (error) {
      console.error('Error fetching settings:', error)
      toast.error('Ayarlar yüklenemedi')
      setLoading(false)
    }
  }

  const handleEngineChange = async (engine) => {
    try {
      await settingsAPI.setOCREngine(engine)
      toast.success(`OCR motoru ${engine} olarak ayarlandı`)
      setSelectedEngine(engine)
      fetchSettings()
    } catch (error) {
      console.error('Error changing engine:', error)
      toast.error('OCR motoru değiştirilemedi')
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
        <div>
          <h1 className="text-3xl font-bold mb-2">Ayarlar</h1>
          <p className="text-gray-400">Sistem ayarları ve yapılandırma</p>
        </div>

        {/* System Info */}
        <div className="bg-dark-800 border border-dark-600 rounded-xl p-6">
          <h2 className="text-xl font-bold mb-4">Sistem Bilgileri</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <p className="text-sm text-gray-400">Sistem Adı</p>
              <p className="text-lg font-semibold">{systemInfo.name || 'EvoPlate Enterprise'}</p>
            </div>
            <div>
              <p className="text-sm text-gray-400">Versiyon</p>
              <p className="text-lg font-semibold">{systemInfo.version || '1.0.0'}</p>
            </div>
            <div>
              <p className="text-sm text-gray-400">Aktif Kameralar</p>
              <p className="text-lg font-semibold">{systemInfo.active_cameras || 0}</p>
            </div>
            <div>
              <p className="text-sm text-gray-400">OCR Motoru</p>
              <p className="text-lg font-semibold text-primary-400">{systemInfo.ocr_engine || '-'}</p>
            </div>
          </div>
        </div>

        {/* OCR Engine Selection */}
        <div className="bg-dark-800 border border-dark-600 rounded-xl p-6">
          <h2 className="text-xl font-bold mb-4">OCR Motor Seçimi</h2>
          <p className="text-sm text-gray-400 mb-6">
            Plaka tanıma için kullanılacak OCR motorunu seçin. Hybrid motor tüm motorları paralel çalıştırıp en iyi sonucu döndürür.
          </p>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {ocrEngines.engines.map((engine) => {
              const isAvailable = ocrEngines.available_engines.includes(engine.id)
              const isCurrent = selectedEngine === engine.id

              return (
                <motion.div
                  key={engine.id}
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  className={`relative bg-dark-700 border rounded-xl p-4 cursor-pointer transition-all ${
                    isCurrent
                      ? 'border-primary-500 ring-2 ring-primary-500'
                      : isAvailable
                      ? 'border-dark-600 hover:border-primary-400'
                      : 'border-dark-600 opacity-50 cursor-not-allowed'
                  }`}
                  onClick={() => isAvailable && handleEngineChange(engine.id)}
                >
                  {isCurrent && (
                    <div className="absolute top-2 right-2">
                      <CheckCircleIcon className="w-6 h-6 text-primary-500" />
                    </div>
                  )}
                  <h3 className="text-lg font-bold mb-2">{engine.name}</h3>
                  <p className="text-sm text-gray-400 mb-4">{engine.description}</p>
                  <div className="flex items-center justify-between">
                    <span className={`text-xs px-2 py-1 rounded ${
                      isAvailable
                        ? 'bg-green-900 text-green-300'
                        : 'bg-red-900 text-red-300'
                    }`}>
                      {isAvailable ? 'Kullanılabilir' : 'Kullanılamaz'}
                    </span>
                    {isCurrent && (
                      <span className="text-xs px-2 py-1 bg-primary-900 text-primary-300 rounded">
                        Aktif
                      </span>
                    )}
                  </div>
                </motion.div>
              )
            })}
          </div>
        </div>

        {/* Additional Settings */}
        <div className="bg-dark-800 border border-dark-600 rounded-xl p-6">
          <h2 className="text-xl font-bold mb-4">Diğer Ayarlar</h2>
          <div className="space-y-4">
            <div className="flex items-center justify-between py-3 border-b border-dark-600">
              <div>
                <p className="font-semibold">Otomatik Güncelleme</p>
                <p className="text-sm text-gray-400">Sistem güncellemelerini otomatik yükle</p>
              </div>
              <label className="relative inline-flex items-center cursor-pointer">
                <input type="checkbox" className="sr-only peer" />
                <div className="w-11 h-6 bg-gray-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary-600"></div>
              </label>
            </div>
            <div className="flex items-center justify-between py-3 border-b border-dark-600">
              <div>
                <p className="font-semibold">Sesli Uyarılar</p>
                <p className="text-sm text-gray-400">Plaka tespit edildiğinde sesli uyarı ver</p>
              </div>
              <label className="relative inline-flex items-center cursor-pointer">
                <input type="checkbox" className="sr-only peer" defaultChecked />
                <div className="w-11 h-6 bg-gray-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary-600"></div>
              </label>
            </div>
            <div className="flex items-center justify-between py-3">
              <div>
                <p className="font-semibold">Dark Mode</p>
                <p className="text-sm text-gray-400">Koyu tema kullan (varsayılan)</p>
              </div>
              <label className="relative inline-flex items-center cursor-pointer">
                <input type="checkbox" className="sr-only peer" defaultChecked disabled />
                <div className="w-11 h-6 bg-gray-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary-600"></div>
              </label>
            </div>
          </div>
        </div>
      </motion.div>
    </div>
  )
}