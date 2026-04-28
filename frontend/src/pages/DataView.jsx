import React, { useState, useEffect } from 'react';
import { crimeAPI } from '../services/api';
import Loading from '../components/Loading';
import { Upload, RefreshCw, FileText } from 'lucide-react';

const DataView = () => {
  const [crimes, setCrimes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [total, setTotal] = useState(0);
  const [skip, setSkip] = useState(0);
  const [limit] = useState(50);
  const [uploading, setUploading] = useState(false);

  useEffect(() => {
    fetchCrimes();
  }, [skip]);

  const fetchCrimes = async () => {
    try {
      setLoading(true);
      const response = await crimeAPI.getCrimes(skip, limit);
      setCrimes(response.data.data);
      setTotal(response.data.total);
    } catch (error) {
      console.error('Error fetching crimes:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    try {
      setUploading(true);
      await crimeAPI.uploadCSV(file);
      alert('Data uploaded successfully!');
      fetchCrimes();
    } catch (error) {
      console.error('Error uploading file:', error);
      alert('Upload failed. Please check your file format.');
    } finally {
      setUploading(false);
    }
  };

  const handleGenerateSample = async () => {
    try {
      setLoading(true);
      await crimeAPI.generateSample();
      alert('Sample data generated!');
      fetchCrimes();
    } catch (error) {
      console.error('Error generating sample:', error);
      alert('Failed to generate sample data.');
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleString();
  };

  const getCrimeTypeColor = (type) => {
    const colors = {
      'Theft': 'bg-red-100 text-red-800',
      'Assault': 'bg-orange-100 text-orange-800',
      'Burglary': 'bg-yellow-100 text-yellow-800',
      'Vandalism': 'bg-blue-100 text-blue-800',
      'Robbery': 'bg-purple-100 text-purple-800',
      'Fraud': 'bg-green-100 text-green-800',
    };
    return colors[type] || 'bg-gray-100 text-gray-800';
  };

  if (loading && crimes.length === 0) {
    return <Loading message="Loading crime data..." />;
  }

  return (
    <div className="p-6">
      {/* Header */}
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Crime Data</h1>
        <p className="text-gray-600 mt-1">Browse and manage crime records</p>
      </div>

      {/* Actions */}
      <div className="bg-white rounded-lg shadow-md p-4 mb-6 flex flex-wrap gap-4 items-center justify-between">
        <div className="flex gap-4">
          <label className="cursor-pointer">
            <input
              type="file"
              accept=".csv"
              onChange={handleFileUpload}
              className="hidden"
            />
            <div className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
              <Upload size={18} />
              <span>{uploading ? 'Uploading...' : 'Upload CSV'}</span>
            </div>
          </label>

          <button
            onClick={handleGenerateSample}
            disabled={loading}
            className="flex items-center gap-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50 transition-colors"
          >
            <FileText size={18} />
            <span>Generate Sample Data</span>
          </button>
        </div>

        <div className="flex items-center gap-2">
          <RefreshCw
            size={18}
            className={`cursor-pointer text-gray-600 hover:text-blue-600 ${loading ? 'animate-spin' : ''}`}
            onClick={fetchCrimes}
          />
          <span className="text-sm text-gray-600">
            Showing {skip + 1}-{Math.min(skip + limit, total)} of {total}
          </span>
        </div>
      </div>

      {/* Table */}
      <div className="bg-white rounded-lg shadow-md overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50 border-b">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  ID
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Crime Type
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Location
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Date & Time
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Hour
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Day
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Hotspot
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {crimes.map((crime) => (
                <tr key={crime.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {crime.id}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full ${getCrimeTypeColor(crime.crime_type)}`}>
                      {crime.crime_type}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                    {crime.latitude.toFixed(4)}, {crime.longitude.toFixed(4)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                    {formatDate(crime.date)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                    {crime.hour !== null ? `${crime.hour}:00` : 'N/A'}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                    {crime.day !== null ? crime.day : 'N/A'}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                    {crime.hotspot_cluster !== -1 && crime.hotspot_cluster !== null ? (
                      <span className="px-2 py-1 bg-blue-100 text-blue-800 rounded-full text-xs">
                        Cluster {crime.hotspot_cluster}
                      </span>
                    ) : (
                      'N/A'
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Pagination */}
        <div className="bg-gray-50 px-6 py-4 flex items-center justify-between border-t">
          <button
            onClick={() => setSkip(Math.max(0, skip - limit))}
            disabled={skip === 0}
            className="px-4 py-2 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Previous
          </button>

          <span className="text-sm text-gray-600">
            Page {Math.floor(skip / limit) + 1} of {Math.ceil(total / limit)}
          </span>

          <button
            onClick={() => setSkip(skip + limit)}
            disabled={skip + limit >= total}
            className="px-4 py-2 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Next
          </button>
        </div>
      </div>
    </div>
  );
};

export default DataView;
