import axios from 'axios';
import { 
  SensorReading, 
  PollutionZone, 
  Vehicle, 
  VehicleLocation, 
  PollutionPrediction, 
  VehicleMission,
  ApiResponse 
} from '../types';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for authentication (if needed later)
api.interceptors.request.use(
  (config) => {
    // Add auth token if available
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// Monitoring API
export const monitoringAPI = {
  getSensorReadings: () => api.get<ApiResponse<SensorReading>>('/monitoring/readings/'),
  
  getSensorReading: (id: number) => api.get<SensorReading>(`/monitoring/readings/${id}/`),
  
  createSensorReading: (data: Partial<SensorReading>) => 
    api.post<SensorReading>('/monitoring/readings/', data),
  
  getPollutionZones: () => api.get<ApiResponse<PollutionZone>>('/monitoring/zones/'),
  
  getPollutionZone: (id: number) => api.get<PollutionZone>(`/monitoring/zones/${id}/`),
  
  getLatestReadings: () => api.get<SensorReading[]>('/monitoring/readings/latest/'),
  
  generateMockData: () => api.post('/monitoring/readings/generate-mock/'),
};

// Vehicles API
export const vehiclesAPI = {
  getVehicles: () => api.get<ApiResponse<Vehicle>>('/vehicles/vehicles/'),
  
  getVehicle: (id: number) => api.get<Vehicle>(`/vehicles/vehicles/${id}/`),
  
  updateVehicle: (id: number, data: Partial<Vehicle>) => 
    api.patch<Vehicle>(`/vehicles/vehicles/${id}/`, data),
  
  getVehicleLocations: (vehicleId?: number) => 
    api.get<ApiResponse<VehicleLocation>>('/vehicles/locations/', {
      params: vehicleId ? { vehicle: vehicleId } : {}
    }),
  
  getVehicleMissions: (vehicleId?: number) => 
    api.get<ApiResponse<VehicleMission>>('/vehicles/missions/', {
      params: vehicleId ? { vehicle: vehicleId } : {}
    }),
  
  createVehicleMission: (data: Partial<VehicleMission>) => 
    api.post<VehicleMission>('/vehicles/missions/', data),
  
  updateVehicleMission: (id: number, data: Partial<VehicleMission>) => 
    api.patch<VehicleMission>(`/vehicles/missions/${id}/`, data),
};

// ML Predictions API
export const predictionsAPI = {
  getPredictions: () => api.get<ApiResponse<PollutionPrediction>>('/ml/predictions/'),
  
  getPrediction: (id: number) => api.get<PollutionPrediction>(`/ml/predictions/${id}/`),
  
  getLatestPredictions: () => api.get<PollutionPrediction[]>('/ml/predictions/latest/'),
  
  generatePredictions: () => api.post('/ml/predictions/generate/'),
  
  trainModel: () => api.post('/ml/train-model/'),
};

// Dashboard API
export const dashboardAPI = {
  getDashboardData: async () => {
    const [sensorReadings, pollutionZones, vehicles, predictions] = await Promise.all([
      monitoringAPI.getLatestReadings(),
      monitoringAPI.getPollutionZones(),
      vehiclesAPI.getVehicles(),
      predictionsAPI.getLatestPredictions(),
    ]);
    
    return {
      sensorReadings: sensorReadings.data,
      pollutionZones: pollutionZones.data.results,
      vehicles: vehicles.data.results,
      predictions: predictions.data,
    };
  },
};

export default api;
