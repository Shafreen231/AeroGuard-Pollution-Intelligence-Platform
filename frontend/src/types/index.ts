export interface SensorReading {
  id: number;
  longitude: number;
  latitude: number;
  pm25: number;
  pm10: number;
  no2: number;
  so2: number;
  co: number;
  o3: number;
  aqi: number;
  timestamp: string;
  vehicle?: number;
  source: 'vehicle' | 'external_api' | 'manual';
}

export interface PollutionZone {
  id: number;
  name: string;
  center_longitude: number;
  center_latitude: number;
  radius: number;
  pollution_level: 'safe' | 'moderate' | 'danger';
  description: string;
  last_updated: string;
}

export interface Vehicle {
  id: number;
  name: string;
  vehicle_type: 'drone' | 'ground_robot' | 'boat';
  current_longitude: number;
  current_latitude: number;
  battery_level: number;
  status: 'active' | 'inactive' | 'maintenance' | 'charging';
  last_active: string;
}

export interface VehicleLocation {
  id: number;
  vehicle: number;
  longitude: number;
  latitude: number;
  altitude?: number;
  speed?: number;
  timestamp: string;
}

export interface PollutionPrediction {
  id: number;
  longitude: number;
  latitude: number;
  predicted_aqi: number;
  prediction_date: string;
  confidence_score: number;
  model_used: string;
  created_at: string;
}

export interface VehicleMission {
  id: number;
  vehicle: number;
  mission_type: 'monitoring' | 'emergency_response' | 'routine_patrol';
  start_location_longitude: number;
  start_location_latitude: number;
  end_location_longitude?: number;
  end_location_latitude?: number;
  status: 'planned' | 'in_progress' | 'completed' | 'aborted';
  start_time: string;
  end_time?: string;
  description: string;
}

export interface ApiResponse<T> {
  results: T[];
  count: number;
  next?: string;
  previous?: string;
}
