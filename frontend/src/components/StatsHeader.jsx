import React from 'react'
import { motion } from 'framer-motion'
import { 
  VideoCameraIcon, 
  RectangleStackIcon, 
  CheckCircleIcon,
  ExclamationTriangleIcon
} from '@heroicons/react/24/outline'

export default function StatsHeader({ stats }) {
  const statCards = [
    {
      label: 'Aktif Kameralar',
      value: stats?.activeCameras || 0,
      icon: VideoCameraIcon,
      color: 'blue',
      bgGradient: 'from-blue-500 to-blue-700'
    },
    {
      label: 'Bugün Tespit',
      value: stats?.todayPlates || 0,
      icon: RectangleStackIcon,
      color: 'green',
      bgGradient: 'from-green-500 to-green-700'
    },
    {
      label: 'Toplam Plaka',
      value: stats?.totalPlates || 0,
      icon: CheckCircleIcon,
      color: 'purple',
      bgGradient: 'from-purple-500 to-purple-700'
    },
    {
      label: 'Kara Liste Alarm',
      value: stats?.blacklistAlerts || 0,
      icon: ExclamationTriangleIcon,
      color: 'red',
      bgGradient: 'from-red-500 to-red-700'
    },
  ]

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      {statCards.map((stat, index) => {
        const Icon = stat.icon
        return (
          <motion.div
            key={stat.label}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            className="bg-dark-800 border border-dark-600 rounded-xl p-5 hover:border-primary-500 transition-all cursor-pointer"
          >
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm mb-1">{stat.label}</p>
                <h3 className="text-3xl font-bold">{stat.value}</h3>
              </div>
              <div className={`w-14 h-14 bg-gradient-to-br ${stat.bgGradient} rounded-xl flex items-center justify-center`}>
                <Icon className="w-8 h-8 text-white" />
              </div>
            </div>
          </motion.div>
        )
      })}
    </div>
  )
}