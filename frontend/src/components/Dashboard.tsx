import React, { useState, useEffect } from 'react';
import {
  Box,
  Grid,
  Paper,
  Typography,
  Card,
  CardContent,
  Chip,
  Alert,
  CircularProgress,
  IconButton,
  Tooltip,
} from '@mui/material';
import { Refresh as RefreshIcon, Warning as WarningIcon } from '@mui/icons-material';
import { MapContainer, TileLayer, Marker, Popup, Circle } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import { dashboardAPI } from '../services/api';
import { SensorReading, PollutionZone, Vehicle, PollutionPrediction } from '../types';

// Fix Leaflet default markers
delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
});

interface DashboardData {
  sensorReadings: SensorReading[];
  pollutionZones: PollutionZone[];
  vehicles: Vehicle[];
  predictions: PollutionPrediction[];
}

const Dashboard: React.FC = () => {
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [lastUpdated, setLastUpdated] = useState<Date | null>(null);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      setError(null);
      const dashboardData = await dashboardAPI.getDashboardData();
      setData(dashboardData);
      setLastUpdated(new Date());
    } catch (err) {
      setError('Failed to fetch dashboard data. Please try again.');
      console.error('Dashboard data fetch error:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboardData();
    // Auto-refresh every 30 seconds
    const interval = setInterval(fetchDashboardData, 30000);
    return () => clearInterval(interval);
  }, []);

  const getAQIColor = (aqi: number): string => {
    if (aqi <= 50) return '#4CAF50'; // Good - Green
    if (aqi <= 100) return '#FFEB3B'; // Moderate - Yellow
    if (aqi <= 150) return '#FF9800'; // Unhealthy for Sensitive - Orange
    if (aqi <= 200) return '#F44336'; // Unhealthy - Red
    if (aqi <= 300) return '#9C27B0'; // Very Unhealthy - Purple
    return '#8D6E63'; // Hazardous - Brown
  };

  const getAQILevel = (aqi: number): string => {
    if (aqi <= 50) return 'Good';
    if (aqi <= 100) return 'Moderate';
    if (aqi <= 150) return 'Unhealthy for Sensitive';
    if (aqi <= 200) return 'Unhealthy';
    if (aqi <= 300) return 'Very Unhealthy';
    return 'Hazardous';
  };

  const getPollutionZoneColor = (level: string): string => {
    switch (level) {
      case 'safe': return '#4CAF50';
      case 'moderate': return '#FF9800';
      case 'danger': return '#F44336';
      default: return '#9E9E9E';
    }
  };

  const getVehicleIcon = (vehicle: Vehicle) => {
    const color = vehicle.status === 'active' ? '#4CAF50' : 
                  vehicle.status === 'maintenance' ? '#FF9800' : '#9E9E9E';
    
    return new L.DivIcon({
      html: `<div style="background-color: ${color}; width: 20px; height: 20px; border-radius: 50%; border: 2px solid white;"></div>`,
      iconSize: [20, 20],
      className: 'vehicle-marker'
    });
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress size={50} />
        <Typography variant="h6" sx={{ ml: 2 }}>Loading dashboard...</Typography>
      </Box>
    );
  }

  if (error) {
    return (
      <Alert severity="error" action={
        <IconButton onClick={fetchDashboardData} size="small">
          <RefreshIcon />
        </IconButton>
      }>
        {error}
      </Alert>
    );
  }

  const averageAQI = data?.sensorReadings.length ? 
    Math.round(data.sensorReadings.reduce((sum, reading) => sum + reading.aqi, 0) / data.sensorReadings.length) : 0;

  const activeVehicles = data?.vehicles.filter(v => v.status === 'active').length || 0;
  const totalVehicles = data?.vehicles.length || 0;

  return (
    <Box sx={{ p: 3 }}>
      {/* Header */}
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4" component="h1" gutterBottom>
          Pollution Monitoring Dashboard
        </Typography>
        <Box display="flex" alignItems="center" gap={2}>
          {lastUpdated && (
            <Typography variant="body2" color="text.secondary">
              Last updated: {lastUpdated.toLocaleTimeString()}
            </Typography>
          )}
          <Tooltip title="Refresh Data">
            <IconButton onClick={fetchDashboardData}>
              <RefreshIcon />
            </IconButton>
          </Tooltip>
        </Box>
      </Box>

      {/* Statistics Cards */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid size={{ xs: 12, sm: 6, md: 3 }}>
          <Card>
            <CardContent>
              <Typography color="text.secondary" gutterBottom>
                Average AQI
              </Typography>
              <Typography variant="h4" component="div" sx={{ color: getAQIColor(averageAQI) }}>
                {averageAQI}
              </Typography>
              <Chip 
                label={getAQILevel(averageAQI)} 
                size="small" 
                sx={{ 
                  mt: 1, 
                  backgroundColor: getAQIColor(averageAQI),
                  color: 'white'
                }}
              />
            </CardContent>
          </Card>
        </Grid>

        <Grid size={{ xs: 12, sm: 6, md: 3 }}>
          <Card>
            <CardContent>
              <Typography color="text.secondary" gutterBottom>
                Active Vehicles
              </Typography>
              <Typography variant="h4" component="div">
                {activeVehicles}/{totalVehicles}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Monitoring Fleet
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid size={{ xs: 12, sm: 6, md: 3 }}>
          <Card>
            <CardContent>
              <Typography color="text.secondary" gutterBottom>
                Sensor Readings
              </Typography>
              <Typography variant="h4" component="div">
                {data?.sensorReadings.length || 0}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Recent Data Points
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid size={{ xs: 12, sm: 6, md: 3 }}>
          <Card>
            <CardContent>
              <Typography color="text.secondary" gutterBottom>
                Pollution Zones
              </Typography>
              <Typography variant="h4" component="div">
                {data?.pollutionZones.length || 0}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Monitored Areas
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Map */}
      <Paper sx={{ p: 2, height: '600px' }}>
        <Typography variant="h6" gutterBottom>
          Real-time Pollution Map
        </Typography>
        
        <MapContainer
          center={data?.sensorReadings?.length 
            ? [data.sensorReadings[0].latitude, data.sensorReadings[0].longitude] 
            : [28.6139, 77.2090] // Default to Delhi
          }
          zoom={12}
          style={{ height: '550px', width: '100%' }}
        >
          <TileLayer
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          />
          
          {/* Pollution Zones */}
          {data?.pollutionZones?.map((zone) => (
            <Circle
              key={`zone-${zone.id}`}
              center={[zone.center_latitude || 28.6139, zone.center_longitude || 77.2090]}
              radius={zone.radius || 5000}
              fillColor={getPollutionZoneColor(zone.pollution_level)}
              fillOpacity={0.3}
              color={getPollutionZoneColor(zone.pollution_level)}
              weight={2}
            >
              <Popup>
                <div>
                  <strong>{zone.name}</strong><br />
                  Level: <Chip 
                    label={zone.pollution_level?.toUpperCase() || 'UNKNOWN'} 
                    size="small"
                    sx={{ 
                      backgroundColor: getPollutionZoneColor(zone.pollution_level),
                      color: 'white'
                    }}
                  /><br />
                  {zone.description}
                </div>
              </Popup>
            </Circle>
          )) || []}

          {/* Sensor Readings */}
          {data?.sensorReadings?.map((reading) => (
            <Marker
              key={`reading-${reading.id}`}
              position={[reading.latitude, reading.longitude]}
            >
              <Popup>
                <div>
                  <strong>AQI: {reading.aqi}</strong><br />
                  <small style={{ color: getAQIColor(reading.aqi) }}>
                    {getAQILevel(reading.aqi)}
                  </small><br />
                    PM2.5: {reading.pm25} μg/m³<br />
                    PM10: {reading.pm10} μg/m³<br />
                    NO₂: {reading.no2} μg/m³<br />
                    Source: {reading.source}<br />
                    <small>{new Date(reading.timestamp).toLocaleString()}</small>
                  </div>
                </Popup>
              </Marker>
            )) || []}

            {/* Vehicles */}
            {data?.vehicles?.map((vehicle) => (
              <Marker
                key={`vehicle-${vehicle.id}`}
                position={[vehicle.current_latitude || 0, vehicle.current_longitude || 0]}
                icon={getVehicleIcon(vehicle)}
              >
                <Popup>
                  <div>
                    <strong>{vehicle.name}</strong><br />
                    Type: {vehicle.vehicle_type}<br />
                    Status: <Chip 
                      label={vehicle.status} 
                      size="small"
                      color={vehicle.status === 'active' ? 'success' : 
                             vehicle.status === 'maintenance' ? 'warning' : 'default'}
                    /><br />
                    Battery: {vehicle.battery_level}%<br />
                    <small>Last active: {new Date(vehicle.last_active).toLocaleString()}</small>
                  </div>
                </Popup>
              </Marker>
            )) || []}
          </MapContainer>
          
          {/* Status message if no data */}
          {(!data?.sensorReadings?.length && !data?.pollutionZones?.length && !data?.vehicles?.length) && (
            <Box 
              position="absolute"
              top="50%"
              left="50%"
              sx={{ transform: 'translate(-50%, -50%)' }}
              textAlign="center"
              bgcolor="rgba(255,255,255,0.9)"
              p={2}
              borderRadius={1}
            >
              <Typography variant="body2" color="text.secondary">
                Loading map data... Please wait or refresh if the issue persists.
              </Typography>
            </Box>
          )}
        </Paper>
    </Box>
  );
};

export default Dashboard;
