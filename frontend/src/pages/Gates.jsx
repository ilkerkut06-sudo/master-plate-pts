import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { PlusIcon, PencilIcon, TrashIcon, LockOpenIcon } from '@heroicons/react/24/outline'
import { gateAPI } from '../utils/api'
import toast from 'react-hot-toast'

export default function Gates() {
  const [gates, setGates] = useState([])
  const [loading, setLoading] = useState(true)
  const [showModal, setShowModal] = useState(false)
  const [editingGate, setEditingGate] = useState(null)
  const [formData, setFormData] = useState({
    name: '',
    gate_type: 'entry',
    site_id: '',
    nodemcu_id: '',
    relay_pin: 2,
    auto_open: false,
    open_duration: 5,
  })

  useEffect(() => {
    fetchGates()
  }, [])

  const fetchGates = async () => {
    try {
      const response = await gateAPI.getAll()
      setGates(response.data)
      setLoading(false)
    } catch (error) {
      console.error('Error fetching gates:', error)
      toast.error('Kapılar yüklenemedi')
      setLoading(false)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      if (editingGate) {
        await gateAPI.update(editingGate.id, formData)
        toast.success('Kapı güncellendi')
      } else {
        await gateAPI.create(formData)
        toast.success('Kapı eklendi')
      }
      setShowModal(false)
      fetchGates()
      resetForm()
    } catch (error) {
      console.error('Error saving gate:', error)
      toast.error('Kapı kaydedilemedi')
    }
  }

  const handleDelete = async (id) => {
    if (!confirm('Kapı silinecek. Emin misiniz?')) return
    try {
      await gateAPI.delete(id)
      toast.success('Kapı silindi')
      fetchGates()
    } catch (error) {
      console.error('Error deleting gate:', error)
      toast.error('Kapı silinemedi')
    }
  }

  const handleOpen = async (id) => {
    try {
      await gateAPI.open(id)
      toast.success('Kapı açıldı')
    } catch (error) {
      toast.error('Kapı açılamadı')
    }
  }

  const handleTest = async (id) => {
    try {
      await gateAPI.test(id)
      toast.success('Test başarılı')
    } catch (error) {
      toast.error('Test başarısız')
    }
  }

  const resetForm = () => {
    setFormData({
      name: '',
      gate_type: 'entry',
      site_id: '',
      nodemcu_id: '',
      relay_pin: 2,
      auto_open: false,
      open_duration: 5,
    })
    setEditingGate(null)
  }

  return (
    <div className="flex-1 overflow-y-auto p-6">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-3xl font-bold mb-2">Kapılar</h1>
          <p className="text-gray-400">Giriş kapısı yönetimi</p>
        </div>
        <button
          onClick={() => {
            resetForm()
            setShowModal(true)
          }}
          className="flex items-center space-x-2 px-4 py-2 bg-primary-600 hover:bg-primary-700 rounded-lg transition-colors"
        >
          <PlusIcon className="w-5 h-5" />
          <span>Yeni Kapı</span>
        </button>
      </div>

      {loading ? (
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin w-12 h-12 border-4 border-primary-500 border-t-transparent rounded-full"></div>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {gates.map((gate) => (
            <motion.div
              key={gate.id}
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              className="bg-dark-800 border border-dark-600 rounded-xl p-4 hover:border-primary-500 transition-all"
            >
              <div className="flex items-start justify-between mb-3">
                <div>
                  <h3 className="font-bold text-lg">{gate.name}</h3>
                  <p className="text-sm text-gray-400">
                    {gate.gate_type === 'entry' ? 'Giriş' : gate.gate_type === 'exit' ? 'Çıkış' : 'İki Yönlü'}
                  </p>
                </div>
                <div className={`w-3 h-3 rounded-full ${
                  gate.is_active ? 'bg-green-500 pulse-glow' : 'bg-gray-500'
                }`}></div>
              </div>

              <div className="space-y-2 mb-4 text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-400">NodeMCU:</span>
                  <span className="font-mono">{gate.nodemcu_id || '-'}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-400">Röle Pin:</span>
                  <span>{gate.relay_pin || '-'}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-400">Otomatik Aç:</span>
                  <span className={gate.auto_open ? 'text-green-400' : 'text-red-400'}>
                    {gate.auto_open ? 'Evet' : 'Hayır'}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-400">Açık Kalma:</span>
                  <span>{gate.open_duration}s</span>
                </div>
              </div>

              <div className="flex space-x-2">
                <button
                  onClick={() => handleOpen(gate.id)}
                  className="flex-1 flex items-center justify-center space-x-1 px-3 py-2 bg-green-600 hover:bg-green-700 rounded-lg text-sm transition-colors"
                >
                  <LockOpenIcon className="w-4 h-4" />
                  <span>Aç</span>
                </button>
                <button
                  onClick={() => handleTest(gate.id)}
                  className="px-3 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg text-sm transition-colors"
                >
                  Test
                </button>
                <button
                  onClick={() => {
                    setEditingGate(gate)
                    setFormData(gate)
                    setShowModal(true)
                  }}
                  className="px-3 py-2 bg-gray-600 hover:bg-gray-700 rounded-lg text-sm transition-colors"
                >
                  <PencilIcon className="w-4 h-4" />
                </button>
                <button
                  onClick={() => handleDelete(gate.id)}
                  className="px-3 py-2 bg-red-600 hover:bg-red-700 rounded-lg text-sm transition-colors"
                >
                  <TrashIcon className="w-4 h-4" />
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
              {editingGate ? 'Kapı Düzenle' : 'Yeni Kapı'}
            </h2>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-1">Kapı Adı</label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  className="w-full px-3 py-2 bg-dark-700 border border-dark-600 rounded-lg focus:border-primary-500 outline-none"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Kapı Tipi</label>
                <select
                  value={formData.gate_type}
                  onChange={(e) => setFormData({ ...formData, gate_type: e.target.value })}
                  className="w-full px-3 py-2 bg-dark-700 border border-dark-600 rounded-lg focus:border-primary-500 outline-none"
                >
                  <option value="entry">Giriş</option>
                  <option value="exit">Çıkış</option>
                  <option value="both">İki Yönlü</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">NodeMCU ID</label>
                <input
                  type="text"
                  value={formData.nodemcu_id}
                  onChange={(e) => setFormData({ ...formData, nodemcu_id: e.target.value })}
                  className="w-full px-3 py-2 bg-dark-700 border border-dark-600 rounded-lg focus:border-primary-500 outline-none"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Röle Pin</label>
                <input
                  type="number"
                  value={formData.relay_pin}
                  onChange={(e) => setFormData({ ...formData, relay_pin: parseInt(e.target.value) })}
                  className="w-full px-3 py-2 bg-dark-700 border border-dark-600 rounded-lg focus:border-primary-500 outline-none"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Açık Kalma Süresi (saniye)</label>
                <input
                  type="number"
                  value={formData.open_duration}
                  onChange={(e) => setFormData({ ...formData, open_duration: parseInt(e.target.value) })}
                  className="w-full px-3 py-2 bg-dark-700 border border-dark-600 rounded-lg focus:border-primary-500 outline-none"
                />
              </div>
              <div className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  checked={formData.auto_open}
                  onChange={(e) => setFormData({ ...formData, auto_open: e.target.checked })}
                  className="w-4 h-4"
                />
                <label className="text-sm">Otomatik Aç</label>
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