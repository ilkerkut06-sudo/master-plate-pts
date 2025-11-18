import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { PlusIcon, PencilIcon, TrashIcon, PlayIcon, StopIcon } from '@heroicons/react/24/outline'
import { cameraAPI } from '../utils/api'
import toast from 'react-hot-toast'

export default function Cameras() {
  const [cameras, setCameras] = useState([])
  const [loading, setLoading] = useState(true)
  const [showModal, setShowModal] = useState(false)
  const [editingCamera, setEditingCamera] = useState(null)
  const [formData, setFormData] = useState({
    name: '',
    camera_type: 'rtsp',
    stream_url: '',
    webcam_index: 0,
    fps: 25,
    enable_ocr: true,
    enable_motion_detection: true,
    roi_enabled: false,
  })

  useEffect(() => {
    fetchCameras()
  }, [])

  const fetchCameras = async () => {
    try {
      const response = await cameraAPI.getAll()
      setCameras(response.data)
      setLoading(false)
    } catch (error) {
      console.error('Error fetching cameras:', error)
      toast.error('Kameralar yüklenemedi')
      setLoading(false)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      if (editingCamera) {
        await cameraAPI.update(editingCamera.id, formData)
        toast.success('Kamera güncellendi')
      } else {
        await cameraAPI.create(formData)
        toast.success('Kamera eklendi')
      }
      setShowModal(false)
      fetchCameras()
      resetForm()
    } catch (error) {
      console.error('Error saving camera:', error)
      toast.error('Kamera kaydedilemedi')
    }
  }

  const handleDelete = async (id) => {
    if (!confirm('Kamara silinecek. Emin misiniz?')) return
    try {
      await cameraAPI.delete(id)
      toast.success('Kamera silindi')
      fetchCameras()
    } catch (error) {
      console.error('Error deleting camera:', error)
      toast.error('Kamera silinemedi')
    }
  }

  const handleStart = async (id) => {
    try {
      await cameraAPI.start(id)
      toast.success('Kamera başlatıldı')
    } catch (error) {
      toast.error('Kamera başlatılamadı')
    }
  }

  const handleStop = async (id) => {
    try {
      await cameraAPI.stop(id)
      toast.success('Kamera durduruldu')
    } catch (error) {
      toast.error('Kamera durdurulamadı')
    }
  }

  const resetForm = () => {
    setFormData({
      name: '',
      camera_type: 'rtsp',
      stream_url: '',
      webcam_index: 0,
      fps: 25,
      enable_ocr: true,
      enable_motion_detection: true,
      roi_enabled: false,
    })
    setEditingCamera(null)
  }

  return (
    <div className="flex-1 overflow-y-auto p-6">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-3xl font-bold mb-2">Kameralar</h1>
          <p className="text-gray-400">Kamera yönetimi ve ayarları</p>
        </div>
        <button
          onClick={() => {
            resetForm()
            setShowModal(true)
          }}
          className="flex items-center space-x-2 px-4 py-2 bg-primary-600 hover:bg-primary-700 rounded-lg transition-colors"
        >
          <PlusIcon className="w-5 h-5" />
          <span>Yeni Kamera</span>
        </button>
      </div>

      {loading ? (
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin w-12 h-12 border-4 border-primary-500 border-t-transparent rounded-full"></div>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {cameras.map((camera) => (
            <motion.div
              key={camera.id}
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              className="bg-dark-800 border border-dark-600 rounded-xl p-4 hover:border-primary-500 transition-all"
            >
              <div className="flex items-start justify-between mb-3">
                <div>
                  <h3 className="font-bold text-lg">{camera.name}</h3>
                  <p className="text-sm text-gray-400">{camera.camera_type.toUpperCase()}</p>
                </div>
                <div className={`w-3 h-3 rounded-full ${
                  camera.is_active ? 'bg-green-500 pulse-glow' : 'bg-gray-500'
                }`}></div>
              </div>

              <div className="space-y-2 mb-4 text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-400">FPS:</span>
                  <span>{camera.fps}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-400">OCR:</span>
                  <span className={camera.enable_ocr ? 'text-green-400' : 'text-red-400'}>
                    {camera.enable_ocr ? 'Aktif' : 'Pasif'}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-400">Hareket Algı:</span>
                  <span className={camera.enable_motion_detection ? 'text-green-400' : 'text-red-400'}>
                    {camera.enable_motion_detection ? 'Aktif' : 'Pasif'}
                  </span>
                </div>
              </div>

              <div className="flex space-x-2">
                <button
                  onClick={() => handleStart(camera.id)}
                  className="flex-1 px-3 py-2 bg-green-600 hover:bg-green-700 rounded-lg text-sm transition-colors"
                >
                  <PlayIcon className="w-4 h-4 mx-auto" />
                </button>
                <button
                  onClick={() => handleStop(camera.id)}
                  className="flex-1 px-3 py-2 bg-red-600 hover:bg-red-700 rounded-lg text-sm transition-colors"
                >
                  <StopIcon className="w-4 h-4 mx-auto" />
                </button>
                <button
                  onClick={() => {
                    setEditingCamera(camera)
                    setFormData(camera)
                    setShowModal(true)
                  }}
                  className="flex-1 px-3 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg text-sm transition-colors"
                >
                  <PencilIcon className="w-4 h-4 mx-auto" />
                </button>
                <button
                  onClick={() => handleDelete(camera.id)}
                  className="flex-1 px-3 py-2 bg-gray-600 hover:bg-gray-700 rounded-lg text-sm transition-colors"
                >
                  <TrashIcon className="w-4 h-4 mx-auto" />
                </button>
              </div>
            </motion.div>
          ))}
        </div>
      )}

      {/* Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            className="bg-dark-800 rounded-xl p-6 max-w-md w-full border border-dark-600"
          >
            <h2 className="text-2xl font-bold mb-4">
              {editingCamera ? 'Kamera Düzenle' : 'Yeni Kamera'}
            </h2>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-1">Kamera Adı</label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  className="w-full px-3 py-2 bg-dark-700 border border-dark-600 rounded-lg focus:border-primary-500 outline-none"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Kamera Tipi</label>
                <select
                  value={formData.camera_type}
                  onChange={(e) => setFormData({ ...formData, camera_type: e.target.value })}
                  className="w-full px-3 py-2 bg-dark-700 border border-dark-600 rounded-lg focus:border-primary-500 outline-none"
                >
                  <option value="rtsp">RTSP</option>
                  <option value="onvif">ONVIF</option>
                  <option value="webcam">Webcam</option>
                </select>
              </div>
              {formData.camera_type === 'webcam' ? (
                <div>
                  <label className="block text-sm font-medium mb-1">Webcam Index</label>
                  <input
                    type="number"
                    value={formData.webcam_index}
                    onChange={(e) => setFormData({ ...formData, webcam_index: parseInt(e.target.value) })}
                    className="w-full px-3 py-2 bg-dark-700 border border-dark-600 rounded-lg focus:border-primary-500 outline-none"
                  />
                </div>
              ) : (
                <div>
                  <label className="block text-sm font-medium mb-1">Stream URL</label>
                  <input
                    type="text"
                    value={formData.stream_url}
                    onChange={(e) => setFormData({ ...formData, stream_url: e.target.value })}
                    placeholder="rtsp://username:password@ip:port/stream"
                    className="w-full px-3 py-2 bg-dark-700 border border-dark-600 rounded-lg focus:border-primary-500 outline-none"
                    required
                  />
                </div>
              )}
              <div>
                <label className="block text-sm font-medium mb-1">FPS</label>
                <input
                  type="number"
                  value={formData.fps}
                  onChange={(e) => setFormData({ ...formData, fps: parseInt(e.target.value) })}
                  className="w-full px-3 py-2 bg-dark-700 border border-dark-600 rounded-lg focus:border-primary-500 outline-none"
                />
              </div>
              <div className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  checked={formData.enable_ocr}
                  onChange={(e) => setFormData({ ...formData, enable_ocr: e.target.checked })}
                  className="w-4 h-4"
                />
                <label className="text-sm">OCR Aktif</label>
              </div>
              <div className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  checked={formData.enable_motion_detection}
                  onChange={(e) => setFormData({ ...formData, enable_motion_detection: e.target.checked })}
                  className="w-4 h-4"
                />
                <label className="text-sm">Hareket Algılama</label>
              </div>
              <div className="flex space-x-2 pt-4">
                <button
                  type="button"
                  onClick={() => {
                    setShowModal(false)
                    resetForm()
                  }}
                  className="flex-1 px-4 py-2 bg-gray-600 hover:bg-gray-700 rounded-lg transition-colors"
                >
                  İptal
                </button>
                <button
                  type="submit"
                  className="flex-1 px-4 py-2 bg-primary-600 hover:bg-primary-700 rounded-lg transition-colors"
                >
                  Kaydet
                </button>
              </div>
            </form>
          </motion.div>
        </div>
      )}
    </div>
  )
}