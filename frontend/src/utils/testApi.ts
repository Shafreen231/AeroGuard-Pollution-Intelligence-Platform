import { dashboardAPI } from '../services/api';

const testDashboardAPI = async () => {
  try {
    console.log('Testing dashboard API...');
    const data = await dashboardAPI.getDashboardData();
    console.log('Dashboard data:', data);
    console.log('Sensor readings:', data.sensorReadings?.length || 0);
    console.log('Pollution zones:', data.pollutionZones?.length || 0);
    console.log('Vehicles:', data.vehicles?.length || 0);
    console.log('Predictions:', data.predictions?.length || 0);
    
    if (data.pollutionZones?.length > 0) {
      console.log('Sample pollution zone:', data.pollutionZones[0]);
    }
    
    return data;
  } catch (error) {
    console.error('Dashboard API error:', error);
    throw error;
  }
};

// Add to window for testing in browser console
(window as any).testDashboardAPI = testDashboardAPI;

export { testDashboardAPI };
