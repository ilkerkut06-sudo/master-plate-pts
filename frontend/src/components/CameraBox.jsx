import React, { useState, useEffect, useRef } from 'react'
import { motion } from 'framer-motion'
import { 
  PlayIcon, 
  PauseIcon, 
  Cog6ToothIcon,
  SignalIcon
} from '@heroicons/react/24/solid'

export default function CameraBox({ camera, onStart, onStop }) {
  const [isRunning, setIsRunning] = useState(false)
  const [fps, setFps] = useState(0)
  const [lastPlate, setLastPlate] = useState(null)
  const canvasRef = useRef(null)
  const wsRef = useRef(null)

  useEffect(() => {
    if (isRunning && camera) {
      connectWebSocket()
    }
    
    return () => {
      if (wsRef.current) {
        wsRef.current.close()
      }
    }
  }, [isRunning, camera])

  const connectWebSocket = () => {
    const wsUrl = `ws://localhost:8000/api/cameras/ws/${camera.id}`
    wsRef.current = new WebSocket(wsUrl)
    
    wsRef.current.onmessage = (event) => {
      if (event.data instanceof Blob) {
        // Frame data
        const url = URL.createObjectURL(event.data)
        const img = new Image()
        img.onload = () => {
          const canvas = canvasRef.current
          if (canvas) {
            const ctx = canvas.getContext('2d')
            ctx.drawImage(img, 0, 0, canvas.width, canvas.height)
          }
          URL.revokeObjectURL(url)
        }
        img.src = url
      } else {
        // Text data (stats, events)
        try {
          const data = JSON.parse(event.data)
          if (data.fps) setFps(data.fps)
          if (data.plate) setLastPlate(data.plate)
        } catch (e) {}
      }
    }
    
    wsRef.current.onerror = (error) => {
      console.error('WebSocket error:', error)
    }
    
    wsRef.current.onclose = () => {
      console.log('WebSocket closed')
    }
  }

  const handleToggle = async () => {
    if (isRunning) {
      if (wsRef.current) {
        wsRef.current.close()
      }
      if (onStop) await onStop(camera.id)
      setIsRunning(false)
    } else {
      if (onStart) await onStart(camera.id)
      setIsRunning(true)
    }
  }

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      className="bg-dark-800 border border-dark-600 rounded-xl overflow-hidden hover:border-primary-500 transition-all"
    >
      {/* Camera Header */}
      <div className="p-3 bg-dark-700 border-b border-dark-600 flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <div className={`w-2 h-2 rounded-full ${
            isRunning ? 'bg-green-500 pulse-glow' : 'bg-gray-500'
          }`}></div>
          <h3 className="font-semibold text-sm">{camera?.name || 'Kamera'}</h3>
        </div>
        <div className="flex items-center space-x-2">
          <div className="flex items-center space-x-1 text-xs text-gray-400">
            <SignalIcon className="w-3 h-3" />
            <span>{fps} FPS</span>
          </div>
          <button
            onClick={handleToggle}
            className={`p-1.5 rounded-lg transition-colors ${
              isRunning 
                ? 'bg-red-500 hover:bg-red-600' 
                : 'bg-green-500 hover:bg-green-600'
            }`}
          >
            {isRunning ? (
              <PauseIcon className="w-4 h-4 text-white" />
            ) : (
              <PlayIcon className="w-4 h-4 text-white" />
            )}
          </button>
        </div>
      </div>

      {/* Video Canvas */}
      <div className="relative bg-black aspect-video">
        <canvas
          ref={canvasRef}
          width={480}
          height={360}
          className="w-full h-full object-cover"
        />
        {!isRunning && (
          <div className="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50">
            <button
              onClick={handleToggle}
              className="px-6 py-3 bg-primary-600 hover:bg-primary-700 rounded-lg font-semibold transition-colors"
            >
              Başlat
            </button>
          </div>
        )}
      </div>

      {/* Last Plate */}
      <div className="p-3 bg-dark-700 border-t border-dark-600">
        {lastPlate ? (
          <div className="flex items-center justify-between">
            <span className="text-xs text-gray-400">Son Plaka:</span>
            <span className="text-sm font-mono font-bold text-green-400">{lastPlate}</span>
          </div>
        ) : (
          <div className="text-center text-xs text-gray-500">
            Plaka bekleniyor...
          </div>
        )}
      </div>
    </motion.div>
  )
}