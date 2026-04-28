import React, { useState, useEffect } from 'react';
import { crimeAPI } from '../services/api';
import Loading from '../components/Loading';
import { Bar, Pie } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
} from 'chart.js';
import { AlertTriangle, TrendingUp, MapPin, Clock } from 'lucide-react';

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
);

const Dashboard = () => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const response = await crimeAPI.getStats();
      setStats(response.data);
    } catch (error) {
      console.error('Error fetching stats:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <Loading message="Loading dashboard..." />;
  }

  if (!stats) {
    return (
      <div className="p-6">
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <p className="text-red-600">Failed to load statistics</p>
        </div>
      </div>
    );
  }

  // Chart data
  const crimesByTypeData = {
    labels: Object.keys(stats.crimes_by_type),
    datasets: [
      {
        label: 'Crimes by Type',
        data: Object.values(stats.crimes_by_type),
        backgroundColor: [
          'rgba(255, 99, 132, 0.7)',
          'rgba(54, 162, 235, 0.7)',
          'rgba(255, 206, 86, 0.7)',
          'rgba(75, 192, 192, 0.7)',
          'rgba(153, 102, 255, 0.7)',
          'rgba(255, 159, 64, 0.7)',
        ],
        borderColor: [
          'rgba(255, 99, 132, 1)',
          'rgba(54, 162, 235, 1)',
          'rgba(255, 206, 86, 1)',
          'rgba(75, 192, 192, 1)',
          'rgba(153, 102, 255, 1)',
          'rgba(255, 159, 64, 1)',
        ],
        borderWidth: 2,
      },
    ],
  };

  const crimesByHourData = {
    labels: Array.from({ length: 24 }, (_, i) => `${i}:00`),
    datasets: [
      {
        label: 'Crimes by Hour',
        data: Object.values(stats.crimes_by_hour),
        backgroundColor: 'rgba(59, 130, 246, 0.5)',
        borderColor: 'rgba(59, 130, 246, 1)',
        borderWidth: 1,
      },
    ],
  };

  const crimesByDayData = {
    labels: Object.keys(stats.crimes_by_day),
    datasets: [
      {
        label: 'Crimes by Day',
        data: Object.values(stats.crimes_by_day),
        backgroundColor: 'rgba(16, 185, 129, 0.5)',
        borderColor: 'rgba(16, 185, 129, 1)',
        borderWidth: 1,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
      },
    },
  };

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-600 mt-1">Crime Analytics Overview</p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white rounded-lg shadow-md p-6 border-l-4 border-blue-500">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600 text-sm">Total Crimes</p>
              <p className="text-3xl font-bold text-gray-900 mt-2">
                {stats.total_crimes}
              </p>
            </div>
            <AlertTriangle className="w-12 h-12 text-blue-500" />
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6 border-l-4 border-red-500">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600 text-sm">Most Common</p>
              <p className="text-xl font-bold text-gray-900 mt-2">
                {Object.entries(stats.crimes_by_type).sort((a, b) => b[1] - a[1])[0]?.[0]}
              </p>
            </div>
            <TrendingUp className="w-12 h-12 text-red-500" />
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6 border-l-4 border-green-500">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600 text-sm">Crime Types</p>
              <p className="text-3xl font-bold text-gray-900 mt-2">
                {Object.keys(stats.crimes_by_type).length}
              </p>
            </div>
            <MapPin className="w-12 h-12 text-green-500" />
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6 border-l-4 border-purple-500">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600 text-sm">Peak Hour</p>
              <p className="text-xl font-bold text-gray-900 mt-2">
                {Object.entries(stats.crimes_by_hour).sort((a, b) => b[1] - a[1])[0]?.[0]}:00
              </p>
            </div>
            <Clock className="w-12 h-12 text-purple-500" />
          </div>
        </div>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Crimes by Type - Pie Chart */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Crimes by Type</h2>
          <div className="h-80">
            <Pie data={crimesByTypeData} options={chartOptions} />
          </div>
        </div>

        {/* Crimes by Hour - Bar Chart */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Crimes by Hour</h2>
          <div className="h-80">
            <Bar data={crimesByHourData} options={chartOptions} />
          </div>
        </div>

        {/* Crimes by Day - Bar Chart */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Crimes by Day of Week</h2>
          <div className="h-80">
            <Bar data={crimesByDayData} options={chartOptions} />
          </div>
        </div>

        {/* Crimes by Type - Bar Chart */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Crime Distribution</h2>
          <div className="h-80">
            <Bar data={crimesByTypeData} options={chartOptions} />
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
