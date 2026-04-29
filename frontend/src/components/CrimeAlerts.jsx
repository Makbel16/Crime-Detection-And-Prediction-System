import React, { useState, useEffect } from 'react';
import { Bell, BellOff, MapPin, Clock, AlertTriangle } from 'lucide-react';
import axios from 'axios';

const CrimeAlerts = () => {
  const [alertsEnabled, setAlertsEnabled] = useState(false);
  const [alerts, setAlerts] = useState([]);
  const [notificationPermission, setNotificationPermission] = useState('default');

  // Check notification permission on mount
  useEffect(() => {
    if ('Notification' in window) {
      setNotificationPermission(Notification.permission);
    }
  }, []);

  // Request notification permission
  const requestPermission = async () => {
    if (!('Notification' in window)) {
      alert('This browser does not support notifications');
      return;
    }

    const permission = await Notification.requestPermission();
    setNotificationPermission(permission);
    
    if (permission === 'granted') {
      setAlertsEnabled(true);
      new Notification('Crime Alerts Enabled', {
        body: 'You will receive alerts for new crimes in your area',
        icon: '/vite.svg'
      });
    }
  };

  // Toggle alerts
  const toggleAlerts = () => {
    if (!alertsEnabled) {
      requestPermission();
    } else {
      setAlertsEnabled(false);
    }
  };

  // Fetch recent crimes and create alerts
  const fetchRecentCrimes = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/crimes/', {
        params: { limit: 10 }
      });
      
      const recentCrimes = response.data.crimes.slice(0, 5);
      const newAlerts = recentCrimes.map(crime => ({
        id: crime.id,
        type: crime.crime_type,
        location: `${crime.latitude.toFixed(4)}, ${crime.longitude.toFixed(4)}`,
        time: new Date(crime.date).toLocaleString(),
        message: `${crime.crime_type} reported in area`
      }));
      
      setAlerts(newAlerts);
    } catch (error) {
      console.error('Error fetching crimes:', error);
    }
  };

  // Send browser notification
  const sendNotification = (alert) => {
    if (alertsEnabled && notificationPermission === 'granted') {
      new Notification('🚨 Crime Alert', {
        body: alert.message,
        icon: '/vite.svg',
        tag: alert.id.toString()
      });
    }
  };

  // Auto-refresh alerts every 30 seconds
  useEffect(() => {
    if (alertsEnabled) {
      fetchRecentCrimes();
      const interval = setInterval(fetchRecentCrimes, 30000);
      return () => clearInterval(interval);
    }
  }, [alertsEnabled]);

  // Send notification when new alert appears
  useEffect(() => {
    if (alerts.length > 0 && alertsEnabled) {
      sendNotification(alerts[0]);
    }
  }, [alerts, alertsEnabled]);

  return (
    <div className="bg-white rounded-lg shadow-md p-6 mb-6">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-3">
          {alertsEnabled ? (
            <Bell className="w-6 h-6 text-blue-600 animate-pulse" />
          ) : (
            <BellOff className="w-6 h-6 text-gray-400" />
          )}
          <h2 className="text-xl font-bold text-gray-900">Crime Alerts</h2>
        </div>
        <button
          onClick={toggleAlerts}
          className={`px-4 py-2 rounded-lg font-medium transition-colors ${
            alertsEnabled
              ? 'bg-red-500 text-white hover:bg-red-600'
              : 'bg-blue-600 text-white hover:bg-blue-700'
          }`}
        >
          {alertsEnabled ? 'Disable Alerts' : 'Enable Alerts'}
        </button>
      </div>

      {alertsEnabled && (
        <div className="space-y-3">
          <p className="text-sm text-gray-600 mb-4">
            Monitoring for new crime reports... (updates every 30 seconds)
          </p>
          
          {alerts.length > 0 ? (
            <div className="space-y-2 max-h-96 overflow-y-auto">
              {alerts.map((alert) => (
                <div
                  key={alert.id}
                  className="p-4 bg-red-50 border-l-4 border-red-500 rounded-lg hover:bg-red-100 transition-colors"
                >
                  <div className="flex items-start space-x-3">
                    <AlertTriangle className="w-5 h-5 text-red-600 mt-1 flex-shrink-0" />
                    <div className="flex-1">
                      <p className="font-semibold text-gray-900">{alert.message}</p>
                      <div className="flex items-center space-x-4 mt-2 text-sm text-gray-600">
                        <span className="flex items-center space-x-1">
                          <MapPin className="w-4 h-4" />
                          <span>{alert.location}</span>
                        </span>
                        <span className="flex items-center space-x-1">
                          <Clock className="w-4 h-4" />
                          <span>{alert.time}</span>
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-8 text-gray-500">
              <Bell className="w-12 h-12 mx-auto mb-3 text-gray-300" />
              <p>No recent crime alerts</p>
              <p className="text-sm mt-1">New alerts will appear here</p>
            </div>
          )}
        </div>
      )}

      {!alertsEnabled && (
        <div className="text-center py-8 text-gray-500">
          <BellOff className="w-12 h-12 mx-auto mb-3 text-gray-300" />
          <p>Crime alerts are disabled</p>
          <p className="text-sm mt-1">Click "Enable Alerts" to receive notifications</p>
        </div>
      )}
    </div>
  );
};

export default CrimeAlerts;
