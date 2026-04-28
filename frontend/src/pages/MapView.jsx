import React, { useState, useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Circle } from 'react-leaflet';
import { hotspotAPI } from '../services/api';
import Loading from '../components/Loading';
import L from 'leaflet';
import { RefreshCw } from 'lucide-react';

// Fix for default marker icons in React-Leaflet
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
});

// Custom colors for clusters
const clusterColors = [
  '#ef4444', // red
  '#3b82f6', // blue
  '#10b981', // green
  '#f59e0b', // yellow
  '#8b5cf6', // purple
  '#ec4899', // pink
];

const MapView = () => {
  const [hotspots, setHotspots] = useState([]);
  const [clusterCenters, setClusterCenters] = useState([]);
  const [statistics, setStatistics] = useState({});
  const [loading, setLoading] = useState(true);
  const [selectedCluster, setSelectedCluster] = useState(null);

  useEffect(() => {
    fetchHotspots();
  }, []);

  const fetchHotspots = async () => {
    try {
      setLoading(true);
      const response = await hotspotAPI.getHotspots();
      setHotspots(response.data.hotspots);
      setClusterCenters(response.data.cluster_centers);
      setStatistics(response.data.statistics);
    } catch (error) {
      console.error('Error fetching hotspots:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleRetrain = async () => {
    try {
      setLoading(true);
      await hotspotAPI.retrain(5);
      await fetchHotspots();
    } catch (error) {
      console.error('Error retraining model:', error);
      setLoading(false);
    }
  };

  const filteredHotspots = selectedCluster !== null
    ? hotspots.filter(h => h.cluster === selectedCluster)
    : hotspots;

  // Calculate map center
  const mapCenter = clusterCenters.length > 0
    ? [clusterCenters[0].latitude, clusterCenters[0].longitude]
    : [37.7749, -122.4194]; // San Francisco default

  if (loading && hotspots.length === 0) {
    return <Loading message="Loading map data..." />;
  }

  return (
    <div className="h-screen flex flex-col">
      {/* Header */}
      <div className="bg-white shadow-sm p-4 flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Crime Hotspot Map</h1>
          <p className="text-sm text-gray-600">
            {filteredHotspots.length} crimes detected • {clusterCenters.length} hotspots
          </p>
        </div>
        <button
          onClick={handleRetrain}
          disabled={loading}
          className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
        >
          <RefreshCw size={18} className={loading ? 'animate-spin' : ''} />
          {loading ? 'Processing...' : 'Retrain Model'}
        </button>
      </div>

      <div className="flex-1 flex">
        {/* Sidebar */}
        <div className="w-80 bg-white shadow-lg overflow-y-auto">
          <div className="p-4 border-b">
            <h2 className="text-lg font-bold text-gray-900 mb-3">Hotspot Clusters</h2>
            <button
              onClick={() => setSelectedCluster(null)}
              className={`w-full text-left px-3 py-2 rounded-lg mb-2 ${
                selectedCluster === null
                  ? 'bg-blue-100 text-blue-700'
                  : 'bg-gray-100 hover:bg-gray-200'
              }`}
            >
              <span className="font-medium">All Clusters</span>
              <span className="float-right text-sm">({hotspots.length})</span>
            </button>
            {clusterCenters.map((center) => (
              <button
                key={center.cluster_id}
                onClick={() => setSelectedCluster(center.cluster_id)}
                className={`w-full text-left px-3 py-2 rounded-lg mb-2 ${
                  selectedCluster === center.cluster_id
                    ? 'bg-blue-100 text-blue-700'
                    : 'bg-gray-100 hover:bg-gray-200'
                }`}
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <div
                      className="w-3 h-3 rounded-full"
                      style={{ backgroundColor: clusterColors[center.cluster_id % clusterColors.length] }}
                    />
                    <span className="font-medium">Cluster {center.cluster_id}</span>
                  </div>
                  <span className="text-sm text-gray-600">({center.crime_count})</span>
                </div>
              </button>
            ))}
          </div>

          {/* Statistics */}
          <div className="p-4">
            <h2 className="text-lg font-bold text-gray-900 mb-3">Statistics</h2>
            {Object.entries(statistics).map(([clusterId, stat]) => (
              <div key={clusterId} className="mb-2 p-2 bg-gray-50 rounded">
                <p className="text-sm font-medium">Cluster {clusterId}</p>
                <p className="text-xs text-gray-600">
                  {stat.count} crimes ({stat.percentage}%)
                </p>
              </div>
            ))}
          </div>
        </div>

        {/* Map */}
        <div className="flex-1">
          <MapContainer
            center={mapCenter}
            zoom={12}
            style={{ height: '100%', width: '100%' }}
          >
            <TileLayer
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            />

            {/* Cluster centers */}
            {clusterCenters.map((center) => (
              <Circle
                key={`center-${center.cluster_id}`}
                center={[center.latitude, center.longitude]}
                radius={500}
                pathOptions={{
                  color: clusterColors[center.cluster_id % clusterColors.length],
                  fillColor: clusterColors[center.cluster_id % clusterColors.length],
                  fillOpacity: 0.3,
                }}
              >
                <Popup>
                  <div>
                    <h3 className="font-bold">Cluster {center.cluster_id}</h3>
                    <p className="text-sm">{center.crime_count} crimes</p>
                  </div>
                </Popup>
              </Circle>
            ))}

            {/* Crime markers */}
            {filteredHotspots.map((hotspot) => (
              <Marker
                key={hotspot.id}
                position={[hotspot.latitude, hotspot.longitude]}
              >
                <Popup>
                  <div>
                    <h3 className="font-bold">{hotspot.crime_type}</h3>
                    <p className="text-sm">Cluster: {hotspot.cluster}</p>
                    <p className="text-xs text-gray-600 mt-1">
                      Lat: {hotspot.latitude.toFixed(4)}<br />
                      Lon: {hotspot.longitude.toFixed(4)}
                    </p>
                  </div>
                </Popup>
              </Marker>
            ))}
          </MapContainer>
        </div>
      </div>
    </div>
  );
};

export default MapView;
