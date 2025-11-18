import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { format } from 'date-fns'
import { tr } from 'date-fns/locale'
import axios from 'axios'
import {
  InformationCircleIcon,
  ExclamationTriangleIcon,
  ExclamationCircleIcon,
  CheckCircleIcon
} from '@heroicons/react/24/outline'

const severityIcons = {
  info: { icon: InformationCircleIcon, color: 'text-blue-400' },
  warning: { icon: ExclamationTriangleIcon, color: 'text-yellow-400' },
  error: { icon: ExclamationCircleIcon, color: 'text-red-400' },
  critical: { icon: ExclamationCircleIcon, color: 'text-red-600' },
}

export default function LastLogsPanel() {
  const [logs, setLogs] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchLogs()
    const interval = setInterval(fetchLogs, 5000) // Refresh every 5 seconds
    return () => clearInterval(interval)
  }, [])

  const fetchLogs = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/logs?limit=20')
      setLogs(response.data)
      setLoading(false)
    } catch (error) {
      console.error('Error fetching logs:', error)
      setLoading(false)
    }
  }

  return (
    <div className="bg-dark-800 border border-dark-600 rounded-xl p-4 h-full flex flex-col">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-bold">Son Loglar</h3>
        <span className="text-xs text-gray-400">{logs.length} kayıt</span>
      </div>

      <div className="flex-1 overflow-y-auto space-y-2 pr-2">
        {loading ? (
          <div className="flex items-center justify-center h-full">
            <div className="animate-spin w-8 h-8 border-4 border-primary-500 border-t-transparent rounded-full"></div>
          </div>
        ) : logs.length === 0 ? (
          <div className="flex items-center justify-center h-full text-gray-500">
            Henüz log kaydı yok
          </div>
        ) : (
          logs.map((log, index) => {
            const severityConfig = severityIcons[log.severity] || severityIcons.info
            const Icon = severityConfig.icon

            return (
              <motion.div
                key={log.id || index}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.03 }}
                className="p-3 bg-dark-700 rounded-lg border border-dark-600 hover:border-primary-500 transition-all"
              >
                <div className="flex items-start space-x-3">
                  <Icon className={`w-5 h-5 flex-shrink-0 ${severityConfig.color}`} />
                  <div className="flex-1 min-w-0">
                    <p className="text-sm text-gray-300 break-words">{log.message}</p>
                    <div className="flex items-center justify-between mt-1">
                      <span className="text-xs text-gray-500">
                        {format(new Date(log.created_at), 'HH:mm:ss', { locale: tr })}
                      </span>
                      <span className={`text-xs px-2 py-0.5 rounded ${
                        log.severity === 'error' || log.severity === 'critical'
                          ? 'bg-red-900 text-red-300'
                          : log.severity === 'warning'
                          ? 'bg-yellow-900 text-yellow-300'
                          : 'bg-blue-900 text-blue-300'
                      }`}>
                        {log.log_type}
                      </span>
                    </div>
                  </div>
                </div>
              </motion.div>
            )
          })
        )}
      </div>
    </div>
  )
}