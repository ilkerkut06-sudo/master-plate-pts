import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { PlusIcon, PencilIcon, TrashIcon } from '@heroicons/react/24/outline'
import { siteAPI } from '../utils/api'
import toast from 'react-hot-toast'

export default function Sites() {
  const [sites, setSites] = useState([])
  const [loading, setLoading] = useState(true)
  const [showModal, setShowModal] = useState(false)
  const [editingSite, setEditingSite] = useState(null)
  const [formData, setFormData] = useState({
    name: '',
    address: '',
    city: '',
  })

  useEffect(() => {
    fetchSites()
  }, [])

  const fetchSites = async () => {
    try {
      const response = await siteAPI.getAll()
      setSites(response.data)
      setLoading(false)
    } catch (error) {
      console.error('Error fetching sites:', error)
      toast.error('Lokasyonlar yüklenemedi')
      setLoading(false)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      if (editingSite) {
        await siteAPI.update(editingSite.id, formData)
        toast.success('Lokasyon güncellendi')
      } else {
        await siteAPI.create(formData)
        toast.success('Lokasyon eklendi')
      }
      setShowModal(false)
      fetchSites()
      resetForm()
    } catch (error) {
      console.error('Error saving site:', error)
      toast.error('Lokasyon kaydedilemedi')
    }
  }

  const handleDelete = async (id) => {
    if (!confirm('Lokasyon silinecek. Emin misiniz?')) return
    try {
      await siteAPI.delete(id)
      toast.success('Lokasyon silindi')
      fetchSites()
    } catch (error) {
      console.error('Error deleting site:', error)
      toast.error('Lokasyon silinemedi')
    }
  }

  const resetForm = () => {
    setFormData({
      name: '',
      address: '',
      city: '',
    })
    setEditingSite(null)
  }

  return (
    <div className="flex-1 overflow-y-auto p-6">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-3xl font-bold mb-2">Lokasyonlar</h1>
          <p className="text-gray-400">Site ve lokasyon yönetimi</p>
        </div>
        <button
          onClick={() => {
            resetForm()
            setShowModal(true)
          }}
          className="flex items-center space-x-2 px-4 py-2 bg-primary-600 hover:bg-primary-700 rounded-lg transition-colors"
        >
          <PlusIcon className="w-5 h-5" />
          <span>Yeni Lokasyon</span>
        </button>
      </div>

      {loading ? (
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin w-12 h-12 border-4 border-primary-500 border-t-transparent rounded-full"></div>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {sites.map((site) => (
            <motion.div
              key={site.id}
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              className="bg-dark-800 border border-dark-600 rounded-xl p-4 hover:border-primary-500 transition-all"
            >
              <div className="flex items-start justify-between mb-3">
                <div>
                  <h3 className="font-bold text-lg">{site.name}</h3>
                  <p className="text-sm text-gray-400">{site.city || 'Şehir belirtilmemiş'}</p>
                </div>
                <div className={`w-3 h-3 rounded-full ${
                  site.is_active ? 'bg-green-500 pulse-glow' : 'bg-gray-500'
                }`}></div>
              </div>

              <div className="mb-4">
                <p className="text-sm text-gray-400">
                  {site.address || 'Adres belirtilmemiş'}
                </p>
              </div>

              <div className="flex space-x-2">
                <button
                  onClick={() => {
                    setEditingSite(site)
                    setFormData(site)
                    setShowModal(true)
                  }}
                  className="flex-1 px-3 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg text-sm transition-colors flex items-center justify-center"
                >
                  <PencilIcon className="w-4 h-4 mr-1" />
                  Düzenle
                </button>
                <button
                  onClick={() => handleDelete(site.id)}
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
              {editingSite ? 'Lokasyon Düzenle' : 'Yeni Lokasyon'}
            </h2>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-1">Lokasyon Adı</label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  className="w-full px-3 py-2 bg-dark-700 border border-dark-600 rounded-lg focus:border-primary-500 outline-none"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Adres</label>
                <textarea
                  value={formData.address}
                  onChange={(e) => setFormData({ ...formData, address: e.target.value })}
                  className="w-full px-3 py-2 bg-dark-700 border border-dark-600 rounded-lg focus:border-primary-500 outline-none"
                  rows="3"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Şehir</label>
                <input
                  type="text"
                  value={formData.city}
                  onChange={(e) => setFormData({ ...formData, city: e.target.value })}
                  className="w-full px-3 py-2 bg-dark-700 border border-dark-600 rounded-lg focus:border-primary-500 outline-none"
                />
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