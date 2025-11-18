import React from 'react'
import { Link, useLocation } from 'react-router-dom'
import { 
  HomeIcon, 
  VideoCameraIcon, 
  RectangleStackIcon,
  LockClosedIcon,
  BuildingOfficeIcon,
  Cog6ToothIcon,
  ChevronLeftIcon,
  ChevronRightIcon
} from '@heroicons/react/24/outline'

const menuItems = [
  { name: 'Dashboard', path: '/', icon: HomeIcon },
  { name: 'Kameralar', path: '/cameras', icon: VideoCameraIcon },
  { name: 'Plakalar', path: '/plates', icon: RectangleStackIcon },
  { name: 'Kapılar', path: '/gates', icon: LockClosedIcon },
  { name: 'Lokasyonlar', path: '/sites', icon: BuildingOfficeIcon },
  { name: 'Ayarlar', path: '/settings', icon: Cog6ToothIcon },
]

export default function SideMenu({ isOpen, setIsOpen }) {
  const location = useLocation()

  return (
    <div className={`bg-dark-800 border-r border-dark-600 transition-all duration-300 ${
      isOpen ? 'w-64' : 'w-20'
    }`}>
      <div className="flex flex-col h-full">
        {/* Logo */}
        <div className="flex items-center justify-between p-4 border-b border-dark-600">
          {isOpen && (
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-blue-700 rounded-lg flex items-center justify-center">
                <span className="text-xl font-bold">EP</span>
              </div>
              <div>
                <h1 className="text-lg font-bold">EvoPlate</h1>
                <p className="text-xs text-gray-400">Enterprise</p>
              </div>
            </div>
          )}
          <button
            onClick={() => setIsOpen(!isOpen)}
            className="p-2 hover:bg-dark-700 rounded-lg transition-colors"
          >
            {isOpen ? (
              <ChevronLeftIcon className="w-5 h-5" />
            ) : (
              <ChevronRightIcon className="w-5 h-5" />
            )}
          </button>
        </div>

        {/* Menu Items */}
        <nav className="flex-1 p-3 space-y-1">
          {menuItems.map((item) => {
            const Icon = item.icon
            const isActive = location.pathname === item.path

            return (
              <Link
                key={item.path}
                to={item.path}
                className={`flex items-center space-x-3 px-3 py-3 rounded-lg transition-all ${
                  isActive
                    ? 'bg-primary-600 text-white'
                    : 'text-gray-400 hover:bg-dark-700 hover:text-white'
                }`}
                title={!isOpen ? item.name : ''}
              >
                <Icon className="w-6 h-6 flex-shrink-0" />
                {isOpen && <span className="font-medium">{item.name}</span>}
              </Link>
            )
          })}
        </nav>

        {/* System Status */}
        <div className={`p-4 border-t border-dark-600 ${!isOpen && 'px-3'}`}>
          <div className="flex items-center space-x-2">
            <div className="w-3 h-3 bg-green-500 rounded-full pulse-glow"></div>
            {isOpen && <span className="text-sm text-gray-400">Sistem Aktif</span>}
          </div>
        </div>
      </div>
    </div>
  )
}