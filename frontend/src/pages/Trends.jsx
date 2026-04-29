import React, { useState, useEffect } from 'react';
import { Line, Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  Filler,
} from 'chart.js';
import Loading from '../components/Loading';
import { trendsAPI } from '../services/api';
import { TrendingUp, Calendar, BarChart3, Activity } from 'lucide-react';

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

const Trends = () => {
  const [monthlyData, setMonthlyData] = useState(null);
  const [yearlyData, setYearlyData] = useState(null);
  const [seasonalData, setSeasonalData] = useState(null);
  const [predictions, setPredictions] = useState(null);
  const [monthlyError, setMonthlyError] = useState(null);
  const [yearlyError, setYearlyError] = useState(null);
  const [seasonalError, setSeasonalError] = useState(null);
  const [predictionError, setPredictionError] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('monthly');

  useEffect(() => {
    fetchAllTrends();
  }, []);

  const fetchAllTrends = async () => {
    setLoading(true);
    setMonthlyError(null);
    setYearlyError(null);
    setSeasonalError(null);
    setPredictionError(null);

    const requests = [
      trendsAPI.getMonthlyTrends(),
      trendsAPI.getYearlyTrends(),
      trendsAPI.getSeasonalAnalysis(),
      trendsAPI.getFuturePredictions()
    ];

    const results = await Promise.allSettled(requests);

    if (results[0].status === 'fulfilled') {
      setMonthlyData(results[0].value.data);
    } else {
      console.error('Monthly trends failed:', results[0].reason);
      setMonthlyError('Unable to load monthly trends.');
    }

    if (results[1].status === 'fulfilled') {
      setYearlyData(results[1].value.data);
    } else {
      console.error('Yearly trends failed:', results[1].reason);
      setYearlyError('Unable to load yearly trends.');
    }

    if (results[2].status === 'fulfilled') {
      setSeasonalData(results[2].value.data);
    } else {
      console.error('Seasonal analysis failed:', results[2].reason);
      setSeasonalError('Unable to load seasonal analysis.');
    }

    if (results[3].status === 'fulfilled') {
      setPredictions(results[3].value.data);
    } else {
      console.error('Future predictions failed:', results[3].reason);
      setPredictionError('Unable to load future predictions.');
    }

    setLoading(false);
  };

  if (loading) {
    return <Loading message="Loading trend analysis..." />;
  }

  const monthlyChartData = monthlyData ? {
    labels: monthlyData.monthly_trends.map(item => item.month),
    datasets: [{
      label: 'Monthly Crime Count',
      data: monthlyData.monthly_trends.map(item => item.count),
      borderColor: 'rgb(59, 130, 246)',
      backgroundColor: 'rgba(59, 130, 246, 0.1)',
      fill: true,
      tension: 0.4
    }]
  } : null;

  const yearlyChartData = yearlyData ? {
    labels: yearlyData.yearly_trends.map(item => item.year.toString()),
    datasets: [{
      label: 'Yearly Crime Count',
      data: yearlyData.yearly_trends.map(item => item.count),
      backgroundColor: 'rgba(16, 185, 129, 0.8)',
      borderColor: 'rgb(16, 185, 129)',
      borderWidth: 1
    }]
  } : null;

  const seasonalChartData = seasonalData && seasonalData.seasonal_analysis ? {
    labels: seasonalData.seasonal_analysis.dates,
    datasets: [
      {
        label: 'Observed',
        data: seasonalData.seasonal_analysis.observed,
        borderColor: 'rgb(59, 130, 246)',
        backgroundColor: 'rgba(59, 130, 246, 0.1)',
        fill: false,
        tension: 0.4
      },
      {
        label: 'Trend',
        data: seasonalData.seasonal_analysis.trend,
        borderColor: 'rgb(245, 101, 101)',
        backgroundColor: 'rgba(245, 101, 101, 0.1)',
        fill: false,
        tension: 0.4
      },
      {
        label: 'Seasonal',
        data: seasonalData.seasonal_analysis.seasonal,
        borderColor: 'rgb(16, 185, 129)',
        backgroundColor: 'rgba(16, 185, 129, 0.1)',
        fill: false,
        tension: 0.4
      }
    ]
  } : null;

  const predictionChartData = predictions && predictions.future_predictions ? {
    labels: predictions.future_predictions.dates,
    datasets: [
      {
        label: 'Predicted Crimes',
        data: predictions.future_predictions.predicted_crimes,
        borderColor: 'rgb(147, 51, 234)',
        backgroundColor: 'rgba(147, 51, 234, 0.1)',
        fill: true,
        tension: 0.4
      },
      {
        label: 'Upper Confidence',
        data: predictions.future_predictions.confidence_intervals.upper,
        borderColor: 'rgba(147, 51, 234, 0.3)',
        backgroundColor: 'transparent',
        fill: false,
        borderDash: [5, 5],
        pointRadius: 0
      },
      {
        label: 'Lower Confidence',
        data: predictions.future_predictions.confidence_intervals.lower,
        borderColor: 'rgba(147, 51, 234, 0.3)',
        backgroundColor: 'transparent',
        fill: false,
        borderDash: [5, 5],
        pointRadius: 0
      }
    ]
  } : null;

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Crime Trends Analysis'
      }
    },
    scales: {
      y: {
        beginAtZero: true
      }
    }
  };

  const tabs = [
    { id: 'monthly', label: 'Monthly Trends', icon: Calendar },
    { id: 'yearly', label: 'Yearly Trends', icon: BarChart3 },
    { id: 'seasonal', label: 'Seasonal Analysis', icon: Activity },
    { id: 'predictions', label: 'Future Predictions', icon: TrendingUp }
  ];

  return (
    <div className="p-6 max-w-7xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
          Time-Series Trend Analysis
        </h1>
        <p className="text-gray-600 dark:text-gray-300">
          Analyze crime patterns over time, seasonal variations, and predict future trends
        </p>
      </div>

      {/* Tab Navigation */}
      <div className="flex flex-wrap gap-2 mb-6 border-b border-gray-200 dark:border-gray-700">
        {tabs.map((tab) => {
          const Icon = tab.icon;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center gap-2 px-4 py-2 rounded-t-lg font-medium transition-colors ${
                activeTab === tab.id
                  ? 'bg-blue-500 text-white border-b-2 border-blue-500'
                  : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white hover:bg-gray-100 dark:hover:bg-gray-800'
              }`}
            >
              <Icon size={18} />
              {tab.label}
            </button>
          );
        })}
      </div>

      {/* Content */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
        {activeTab === 'monthly' && (
          <div>
            <h2 className="text-xl font-semibold mb-4 text-gray-900 dark:text-white">
              Monthly Crime Trends
            </h2>
            {monthlyError ? (
              <div className="text-center py-12">
                <p className="text-red-500 dark:text-red-400">{monthlyError}</p>
              </div>
            ) : monthlyData ? (
              <>
                <div className="mb-4">
                  <p className="text-sm text-gray-600 dark:text-gray-300">
                    Total Crimes: <span className="font-semibold">{monthlyData.total_crimes}</span> |
                    Time Periods: <span className="font-semibold">{monthlyData.periods}</span>
                  </p>
                </div>
                <div className="h-96">
                  <Line data={monthlyChartData} options={chartOptions} />
                </div>
              </>
            ) : (
              <div className="text-center py-12">
                <p className="text-gray-500 dark:text-gray-400">No monthly trend data available.</p>
              </div>
            )}
          </div>
        )}

        {activeTab === 'yearly' && (
          <div>
            <h2 className="text-xl font-semibold mb-4 text-gray-900 dark:text-white">
              Yearly Crime Trends
            </h2>
            {yearlyError ? (
              <div className="text-center py-12">
                <p className="text-red-500 dark:text-red-400">{yearlyError}</p>
              </div>
            ) : yearlyData ? (
              <>
                <div className="mb-4">
                  <p className="text-sm text-gray-600 dark:text-gray-300">
                    Total Crimes: <span className="font-semibold">{yearlyData.total_crimes}</span> |
                    Years Analyzed: <span className="font-semibold">{yearlyData.years}</span>
                  </p>
                </div>
                <div className="h-96">
                  <Bar data={yearlyChartData} options={chartOptions} />
                </div>
              </>
            ) : (
              <div className="text-center py-12">
                <p className="text-gray-500 dark:text-gray-400">No yearly trend data available.</p>
              </div>
            )}
          </div>
        )}

        {activeTab === 'seasonal' && (
          <div>
            <h2 className="text-xl font-semibold mb-4 text-gray-900 dark:text-white">
              Seasonal Analysis
            </h2>
            {seasonalError ? (
              <div className="text-center py-12">
                <p className="text-red-500 dark:text-red-400">{seasonalError}</p>
              </div>
            ) : seasonalData ? (
              <>
                {seasonalData.error ? (
                  <div className="text-center py-8">
                    <p className="text-gray-500 dark:text-gray-400">{seasonalData.error}</p>
                  </div>
                ) : (
                  <>
                    <div className="mb-4">
                      <p className="text-sm text-gray-600 dark:text-gray-300">
                        Total Periods: <span className="font-semibold">{seasonalData.total_periods}</span> |
                        Seasonal Strength: <span className="font-semibold">{(seasonalData.seasonal_strength * 100).toFixed(1)}%</span>
                      </p>
                    </div>
                    <div className="h-96">
                      <Line data={seasonalChartData} options={chartOptions} />
                    </div>
                  </>
                )}
              </>
            ) : (
              <div className="text-center py-12">
                <p className="text-gray-500 dark:text-gray-400">No seasonal analysis data available.</p>
              </div>
            )}
          </div>
        )}

        {activeTab === 'predictions' && (
          <div>
            <h2 className="text-xl font-semibold mb-4 text-gray-900 dark:text-white">
              Future Crime Predictions
            </h2>
            {predictionError ? (
              <div className="text-center py-12">
                <p className="text-red-500 dark:text-red-400">{predictionError}</p>
              </div>
            ) : predictions ? (
              <>
                {predictions.error ? (
                  <div className="text-center py-8">
                    <p className="text-gray-500 dark:text-gray-400">{predictions.error}</p>
                  </div>
                ) : (
                  <>
                    <div className="mb-4 grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div className="bg-gray-50 dark:bg-gray-700 p-4 rounded-lg">
                        <h3 className="font-semibold text-gray-900 dark:text-white mb-2">Model Metrics</h3>
                        <p className="text-sm text-gray-600 dark:text-gray-300">
                          AIC: <span className="font-mono">{predictions.aic.toFixed(2)}</span><br />
                          BIC: <span className="font-mono">{predictions.bic.toFixed(2)}</span>
                        </p>
                      </div>
                      <div className="bg-gray-50 dark:bg-gray-700 p-4 rounded-lg">
                        <h3 className="font-semibold text-gray-900 dark:text-white mb-2">Prediction Details</h3>
                        <p className="text-sm text-gray-600 dark:text-gray-300">
                          Forecasting: <span className="font-semibold">{predictions.future_predictions.dates.length} months</span><br />
                          Confidence intervals included
                        </p>
                      </div>
                    </div>
                    <div className="h-96">
                      <Line data={predictionChartData} options={chartOptions} />
                    </div>
                  </>
                )}
              </>
            ) : (
              <div className="text-center py-12">
                <p className="text-gray-500 dark:text-gray-400">No prediction data available.</p>
              </div>
            )}
          </div>
        )}

        {!monthlyData && !yearlyData && !seasonalData && !predictions && (
          <div className="text-center py-12">
            <p className="text-gray-500 dark:text-gray-400 mb-4">
              No trend data available. Please ensure you have crime data uploaded.
            </p>
            <button
              onClick={fetchAllTrends}
              className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg transition-colors"
            >
              Refresh Data
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default Trends;