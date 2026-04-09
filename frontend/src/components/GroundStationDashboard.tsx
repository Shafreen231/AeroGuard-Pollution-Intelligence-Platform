import React, { useState, useEffect, useRef } from 'react';
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
  LinearProgress,
  Fade,
  Zoom,
  useTheme,
  alpha,
} from '@mui/material';
import {
  Refresh as RefreshIcon,
  Satellite as SatelliteIcon,
  Speed as SpeedIcon,
  Visibility as RadarIcon,
  SignalCellularAlt as SignalIcon,
  FlightTakeoff as DroneIcon,
  DirectionsCar as VehicleIcon,
  Waves as BoatIcon,
} from '@mui/icons-material';
import { MapContainer, TileLayer, Circle, Popup, Marker } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import { dashboardAPI } from '../services/api';
import { SensorReading, PollutionZone, Vehicle, PollutionPrediction } from '../types';

// Ground Station Theme Colors
const GROUND_STATION_COLORS = {
  primary: '#00ff41', // Matrix green
  secondary: '#0099ff', // Electric blue
  warning: '#ff9800', // Orange
  danger: '#ff1744', // Red
  background: '#0a0a0a', // Dark background
  surface: '#1a1a1a', // Card background
  radar: '#00ff4140', // Transparent green
};

interface DashboardData {
  sensorReadings: SensorReading[];
  pollutionZones: PollutionZone[];
  vehicles: Vehicle[];
  predictions: PollutionPrediction[];
}

const GroundStationDashboard: React.FC = () => {
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [lastUpdated, setLastUpdated] = useState<Date | null>(null);
  const [connectionStatus, setConnectionStatus] = useState<'connected' | 'connecting' | 'disconnected'>('connecting');
  const [radarSweep, setRadarSweep] = useState(0);
  const theme = useTheme();

  // Radar sweep animation
  useEffect(() => {
    const interval = setInterval(() => {
      setRadarSweep(prev => (prev + 1) % 360);
    }, 50);
    return () => clearInterval(interval);
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      setError(null);
      setConnectionStatus('connecting');
      
      const dashboardData = await dashboardAPI.getDashboardData();
      setData(dashboardData);
      setLastUpdated(new Date());
      setConnectionStatus('connected');
    } catch (err) {
      console.error('Failed to fetch dashboard data:', err);
      setError('Failed to fetch dashboard data. Please try again.');
      setConnectionStatus('disconnected');
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

  // Get vehicle icon based on type
  const getVehicleIcon = (type: string) => {
    switch (type) {
      case 'drone': return <DroneIcon />;
      case 'ground_robot': return <VehicleIcon />;
      case 'boat': return <BoatIcon />;
      default: return <DroneIcon />;
    }
  };

  // Get connection status color
  const getConnectionColor = () => {
    switch (connectionStatus) {
      case 'connected': return GROUND_STATION_COLORS.primary;
      case 'connecting': return GROUND_STATION_COLORS.warning;
      case 'disconnected': return GROUND_STATION_COLORS.danger;
    }
  };

  const activeVehicles = data?.vehicles?.filter(v => v.status === 'active').length || 0;
  const totalVehicles = data?.vehicles?.length || 0;
  const averageAQI = data?.sensorReadings?.length 
    ? Math.round(data.sensorReadings.reduce((sum, reading) => sum + reading.aqi, 0) / data.sensorReadings.length)
    : 0;

  if (loading && !data) {
    return (
      <Box 
        display="flex" 
        justifyContent="center" 
        alignItems="center" 
        minHeight="100vh"
        bgcolor={GROUND_STATION_COLORS.background}
        color={GROUND_STATION_COLORS.primary}
      >
        <Box textAlign="center">
          <CircularProgress size={60} sx={{ color: GROUND_STATION_COLORS.primary, mb: 2 }} />
          <Typography variant="h6" sx={{ color: GROUND_STATION_COLORS.primary }}>
            INITIALIZING GROUND STATION...
          </Typography>
          <Typography variant="body2" sx={{ color: GROUND_STATION_COLORS.secondary, mt: 1 }}>
            Establishing connection to unmanned fleet
          </Typography>
        </Box>
      </Box>
    );
  }

  return (
    <Box sx={{ 
      minHeight: '100vh', 
      bgcolor: GROUND_STATION_COLORS.background,
      color: GROUND_STATION_COLORS.primary,
      p: 2,
      fontFamily: 'monospace'
    }}>
      {/* Header */}
      <Paper sx={{ 
        mb: 3, 
        p: 2, 
        bgcolor: GROUND_STATION_COLORS.surface,
        border: `1px solid ${GROUND_STATION_COLORS.primary}`,
        boxShadow: `0 0 20px ${alpha(GROUND_STATION_COLORS.primary, 0.3)}`
      }}>
        <Grid container alignItems="center" justifyContent="space-between">
          <Grid size={{ xs: 12, md: 8 }}>
            <Typography variant="h4" sx={{ 
              color: GROUND_STATION_COLORS.primary,
              fontFamily: 'monospace',
              fontWeight: 'bold',
              textShadow: `0 0 10px ${GROUND_STATION_COLORS.primary}`
            }}>
              ◉ POLLUTION MONITORING GROUND STATION
            </Typography>
            <Typography variant="body2" sx={{ color: GROUND_STATION_COLORS.secondary }}>
              Real-time Environmental Surveillance Network
            </Typography>
          </Grid>
          <Grid size={{ xs: 12, md: 4 }}>
            <Box display="flex" alignItems="center" gap={2}>
              <Box display="flex" alignItems="center" gap={1}>
                <SignalIcon sx={{ color: getConnectionColor() }} />
                <Typography variant="body2" sx={{ color: getConnectionColor() }}>
                  {connectionStatus.toUpperCase()}
                </Typography>
              </Box>
              <IconButton 
                onClick={fetchDashboardData} 
                sx={{ color: GROUND_STATION_COLORS.primary }}
              >
                <RefreshIcon />
              </IconButton>
            </Box>
          </Grid>
        </Grid>
      </Paper>

      {error && (
        <Alert 
          severity="error" 
          sx={{ mb: 3, bgcolor: alpha(GROUND_STATION_COLORS.danger, 0.1) }}
          action={
            <IconButton onClick={fetchDashboardData} size="small">
              <RefreshIcon />
            </IconButton>
          }
        >
          {error}
        </Alert>
      )}

      {/* Main Control Grid */}
      <Grid container spacing={3}>
        {/* Left Panel - Stats and Controls */}
        <Grid size={{ xs: 12, md: 4 }}>
          {/* Mission Status */}
          <Paper sx={{ 
            mb: 3, 
            p: 2, 
            bgcolor: GROUND_STATION_COLORS.surface,
            border: `1px solid ${GROUND_STATION_COLORS.secondary}`,
            boxShadow: `0 0 15px ${alpha(GROUND_STATION_COLORS.secondary, 0.2)}`
          }}>
            <Typography variant="h6" sx={{ 
              color: GROUND_STATION_COLORS.secondary, 
              mb: 2,
              display: 'flex',
              alignItems: 'center',
              gap: 1
            }}>
              <RadarIcon /> MISSION STATUS
            </Typography>
            
            <Box sx={{ mb: 2 }}>
              <Typography variant="body2" sx={{ color: GROUND_STATION_COLORS.primary }}>
                Fleet Status: {activeVehicles}/{totalVehicles} ACTIVE
              </Typography>
              <LinearProgress 
                variant="determinate" 
                value={(activeVehicles / totalVehicles) * 100} 
                sx={{ 
                  mt: 1,
                  '& .MuiLinearProgress-bar': {
                    bgcolor: GROUND_STATION_COLORS.primary
                  }
                }}
              />
            </Box>

            <Box sx={{ mb: 2 }}>
              <Typography variant="body2" sx={{ color: GROUND_STATION_COLORS.primary }}>
                Average AQI: {averageAQI}
              </Typography>
              <Chip 
                label={averageAQI > 150 ? 'HAZARDOUS' : averageAQI > 100 ? 'UNHEALTHY' : 'GOOD'}
                size="small"
                sx={{ 
                  mt: 1,
                  bgcolor: averageAQI > 150 ? GROUND_STATION_COLORS.danger : 
                           averageAQI > 100 ? GROUND_STATION_COLORS.warning : 
                           GROUND_STATION_COLORS.primary,
                  color: 'black',
                  fontWeight: 'bold'
                }}
              />
            </Box>

            <Typography variant="body2" sx={{ color: GROUND_STATION_COLORS.secondary }}>
              Data Points: {data?.sensorReadings?.length || 0}
            </Typography>
            <Typography variant="body2" sx={{ color: GROUND_STATION_COLORS.secondary }}>
              Coverage Zones: {data?.pollutionZones?.length || 0}
            </Typography>
          </Paper>

          {/* Vehicle Fleet Status */}
          <Paper sx={{ 
            mb: 3, 
            p: 2, 
            bgcolor: GROUND_STATION_COLORS.surface,
            border: `1px solid ${GROUND_STATION_COLORS.primary}`,
            boxShadow: `0 0 15px ${alpha(GROUND_STATION_COLORS.primary, 0.2)}`
          }}>
            <Typography variant="h6" sx={{ 
              color: GROUND_STATION_COLORS.primary, 
              mb: 2,
              display: 'flex',
              alignItems: 'center',
              gap: 1
            }}>
              <SatelliteIcon /> FLEET STATUS
            </Typography>
            
            {data?.vehicles?.map((vehicle, index) => (
              <Fade in={true} timeout={500 + index * 100} key={vehicle.id}>
                <Box sx={{ 
                  display: 'flex', 
                  alignItems: 'center', 
                  gap: 2, 
                  mb: 1,
                  p: 1,
                  bgcolor: alpha(GROUND_STATION_COLORS.primary, 0.05),
                  borderRadius: 1,
                  border: `1px solid ${alpha(GROUND_STATION_COLORS.primary, 0.2)}`
                }}>
                  {getVehicleIcon(vehicle.vehicle_type)}
                  <Box flex={1}>
                    <Typography variant="body2" sx={{ color: GROUND_STATION_COLORS.primary }}>
                      {vehicle.name}
                    </Typography>
                    <Typography variant="caption" sx={{ color: GROUND_STATION_COLORS.secondary }}>
                      {vehicle.status.toUpperCase()} | Battery: {vehicle.battery_level}%
                    </Typography>
                  </Box>
                  <Box 
                    sx={{
                      width: 8,
                      height: 8,
                      borderRadius: '50%',
                      bgcolor: vehicle.status === 'active' ? GROUND_STATION_COLORS.primary : 
                               vehicle.status === 'maintenance' ? GROUND_STATION_COLORS.warning :
                               GROUND_STATION_COLORS.danger,
                      boxShadow: `0 0 8px ${vehicle.status === 'active' ? GROUND_STATION_COLORS.primary : 
                                            vehicle.status === 'maintenance' ? GROUND_STATION_COLORS.warning :
                                            GROUND_STATION_COLORS.danger}`,
                      animation: vehicle.status === 'active' ? 'pulse 2s infinite' : 'none'
                    }}
                  />
                </Box>
              </Fade>
            )) || []}
          </Paper>
        </Grid>

        {/* Center - Radar Map */}
        <Grid size={{ xs: 12, md: 8 }}>
          <Paper sx={{ 
            p: 2, 
            height: '700px',
            bgcolor: GROUND_STATION_COLORS.surface,
            border: `2px solid ${GROUND_STATION_COLORS.primary}`,
            boxShadow: `0 0 30px ${alpha(GROUND_STATION_COLORS.primary, 0.4)}`,
            position: 'relative',
            overflow: 'hidden'
          }}>
            <Typography variant="h6" sx={{ 
              color: GROUND_STATION_COLORS.primary, 
              mb: 2,
              display: 'flex',
              alignItems: 'center',
              gap: 1
            }}>
              <SpeedIcon /> TACTICAL ENVIRONMENTAL MAP
            </Typography>
            
            {/* Radar Sweep Animation */}
            <Box
              sx={{
                position: 'absolute',
                top: '50%',
                left: '50%',
                width: '400px',
                height: '400px',
                transform: 'translate(-50%, -50%)',
                borderRadius: '50%',
                border: `2px solid ${alpha(GROUND_STATION_COLORS.primary, 0.3)}`,
                '&::before': {
                  content: '""',
                  position: 'absolute',
                  top: '50%',
                  left: '50%',
                  width: '2px',
                  height: '200px',
                  bgcolor: GROUND_STATION_COLORS.primary,
                  transformOrigin: 'bottom',
                  transform: `translate(-50%, -100%) rotate(${radarSweep}deg)`,
                  boxShadow: `0 0 20px ${GROUND_STATION_COLORS.primary}`,
                  opacity: 0.7
                },
                zIndex: 1000
              }}
            />
            
            <MapContainer
              center={data?.sensorReadings?.length 
                ? [data.sensorReadings[0].latitude, data.sensorReadings[0].longitude] 
                : [28.6139, 77.2090] // Default to Delhi region
              }
              zoom={10}
              style={{ 
                height: '620px', 
                width: '100%',
                filter: 'hue-rotate(180deg) saturate(0.3)',
                borderRadius: '8px'
              }}
              zoomControl={false}
            >
              <TileLayer
                url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
                attribution='&copy; <a href="https://www.carto.com/">CARTO</a>'
              />
              
              {/* Custom Heatmap using colored circles */}
              {data?.sensorReadings && data.sensorReadings.map((reading, index) => {
                const pollutionLevel = Math.max(
                  reading.pm25 || 0,
                  reading.pm10 || 0,
                  reading.no2 || 0,
                  reading.o3 || 0
                );
                
                let color = '#00ff41'; // Green for low pollution
                let radius = 50;
                
                if (pollutionLevel > 100) {
                  color = '#ff4444'; // Red for high pollution
                  radius = 100;
                } else if (pollutionLevel > 50) {
                  color = '#ff8800'; // Orange for medium pollution
                  radius = 75;
                }
                
                return (
                  <Circle
                    key={`pollution-${index}`}
                    center={[reading.latitude, reading.longitude]}
                    radius={radius}
                    pathOptions={{
                      color: color,
                      fillColor: color,
                      fillOpacity: 0.3,
                      weight: 2,
                      opacity: 0.8
                    }}
                  >
                    <Popup>
                      <div style={{ 
                        fontFamily: 'Courier New, monospace', 
                        color: '#00ff41',
                        backgroundColor: '#001100',
                        padding: '8px',
                        border: '1px solid #00ff41'
                      }}>
                        <strong>SENSOR DATA</strong><br/>
                        PM2.5: {reading.pm25 || 'N/A'} μg/m³<br/>
                        PM10: {reading.pm10 || 'N/A'} μg/m³<br/>
                        NO₂: {reading.no2 || 'N/A'} μg/m³<br/>
                        O₃: {reading.o3 || 'N/A'} μg/m³<br/>
                        Status: <span style={{ color: color }}>
                          {pollutionLevel > 100 ? 'HIGH' : pollutionLevel > 50 ? 'MEDIUM' : 'LOW'}
                        </span>
                      </div>
                    </Popup>
                  </Circle>
                );
              })}

              {/* Pollution Zones */}
              {data?.pollutionZones?.map((zone) => (
                <Circle
                  key={`zone-${zone.id}`}
                  center={[zone.center_latitude || 28.6139, zone.center_longitude || 77.2090]}
                  radius={zone.radius || 5000}
                  fillColor={
                    zone.pollution_level === 'safe' ? GROUND_STATION_COLORS.primary :
                    zone.pollution_level === 'moderate' ? GROUND_STATION_COLORS.warning :
                    GROUND_STATION_COLORS.danger
                  }
                  fillOpacity={0.2}
                  color={
                    zone.pollution_level === 'safe' ? GROUND_STATION_COLORS.primary :
                    zone.pollution_level === 'moderate' ? GROUND_STATION_COLORS.warning :
                    GROUND_STATION_COLORS.danger
                  }
                  weight={2}
                >
                  <Popup>
                    <Box sx={{ color: 'black' }}>
                      <Typography variant="subtitle2">
                        {zone.name}
                      </Typography>
                      <Typography variant="body2">
                        Status: {zone.pollution_level?.toUpperCase()}
                      </Typography>
                      <Typography variant="caption">
                        {zone.description}
                      </Typography>
                    </Box>
                  </Popup>
                </Circle>
              )) || []}
            </MapContainer>

            {/* Status Overlay */}
            <Box sx={{
              position: 'absolute',
              bottom: 16,
              right: 16,
              bgcolor: alpha(GROUND_STATION_COLORS.background, 0.8),
              p: 1,
              borderRadius: 1,
              border: `1px solid ${GROUND_STATION_COLORS.primary}`
            }}>
              <Typography variant="caption" sx={{ color: GROUND_STATION_COLORS.primary }}>
                LIVE | {lastUpdated?.toLocaleTimeString()}
              </Typography>
            </Box>
          </Paper>
        </Grid>
      </Grid>

      {/* Global Styles for Animations */}
      <style>
        {`
          @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.5; }
            100% { opacity: 1; }
          }
        `}
      </style>
    </Box>
  );
};

export default GroundStationDashboard;
