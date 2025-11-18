import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { MagnifyingGlassIcon } from '@heroicons/react/24/outline'
import { plateAPI } from '../utils/api'
import { format } from 'date-fns'
import { tr } from 'date-fns/locale'
import toast from 'react-hot-toast'

export default function Plates() {
  const [plates, setPlates] = useState([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')

  useEffect(() => {
    fetchPlates()
  }, [])

  const fetchPlates = async () => {
    try {
      const response = await plateAPI.getAll(100)
      setPlates(response.data)
      setLoading(false)
    } catch (error) {
      console.error('Error fetching plates:', error)
      toast.error('Plakalar yüklenemedi')
      setLoading(false)
    }
  }

  const handleSearch = async () => {
    if (!searchTerm.trim()) {
      fetchPlates()
      return
    }
    try {
      const response = await plateAPI.search(searchTerm)
      setPlates(response.data)
    } catch (error) {
      console.error('Error searching plates:', error)
      toast.error('Arama başarısız')
    }
  }

  const filteredPlates = searchTerm
    ? plates.filter(plate => plate.plate_number.toLowerCase().includes(searchTerm.toLowerCase()))
    : plates

  return (
    <div className="flex-1 overflow-y-auto p-6">
      <div className="mb-6">
        <h1 className="text-3xl font-bold mb-2">Plakalar</h1>
        <p className="text-gray-400">Tespit edilen plaka kayıtları</p>
      </div>

      {/* Search */}
      <div className="mb-6">
        <div className="flex space-x-2">
          <div className="flex-1 relative">
            <input
              type="text"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
              placeholder="Plaka ara... (örn: 34ABC123)"
              className="w-full px-4 py-3 pl-10 bg-dark-800 border border-dark-600 rounded-lg focus:border-primary-500 outline-none"
            />
            <MagnifyingGlassIcon className="w-5 h-5 absolute left-3 top-3.5 text-gray-400" />
          </div>
          <button
            onClick={handleSearch}
            className="px-6 py-3 bg-primary-600 hover:bg-primary-700 rounded-lg transition-colors"
          >
            Ara
          </button>
        </div>
      </div>

      {loading ? (
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin w-12 h-12 border-4 border-primary-500 border-t-transparent rounded-full"></div>
        </div>
      ) : (
        <div className="bg-dark-800 border border-dark-600 rounded-xl overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-dark-700 border-b border-dark-600">
                <tr>
                  <th className="px-6 py-4 text-left text-sm font-semibold">Plaka</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold">Kamera</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold">Güven</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold">Motor</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold">Yön</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold">Tarih/Saat</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-dark-600">
                {filteredPlates.length === 0 ? (
                  <tr>
                    <td colSpan="6" className="px-6 py-12 text-center text-gray-500">
                      Kayıt bulunamadı
                    </td>
                  </tr>
                ) : (
                  filteredPlates.map((plate, index) => (
                    <motion.tr
                      key={plate.id}
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      transition={{ delay: index * 0.02 }}
                      className="hover:bg-dark-700 transition-colors"
                    >
                      <td className="px-6 py-4">
                        <span className="font-mono font-bold text-lg text-primary-400">
                          {plate.plate_number}
                        </span>
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-300">{plate.camera_id}</td>
                      <td className="px-6 py-4">
                        <div className="flex items-center space-x-2">
                          <div className="w-full bg-dark-600 rounded-full h-2 max-w-[100px]">
                            <div
                              className="bg-green-500 h-2 rounded-full"
                              style={{ width: `${plate.confidence * 100}%` }}
                            ></div>
                          </div>
                          <span className="text-sm text-gray-300">
                            {(plate.confidence * 100).toFixed(0)}%
                          </span>
                        </div>
                      </td>
                      <td className="px-6 py-4">
                        <span className="px-2 py-1 bg-blue-900 text-blue-300 rounded text-xs">
                          {plate.ocr_engine}
                        </span>
                      </td>
                      <td className="px-6 py-4">
                        <span className={`px-2 py-1 rounded text-xs ${
                          plate.direction === 'in'
                            ? 'bg-green-900 text-green-300'
                            : 'bg-red-900 text-red-300'
                        }`}>
                          {plate.direction === 'in' ? 'Giriş' : 'Çıkış'}
                        </span>
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-400">
                        {format(new Date(plate.detected_at), 'dd MMM yyyy HH:mm:ss', { locale: tr })}
                      </td>
                    </motion.tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  )
}