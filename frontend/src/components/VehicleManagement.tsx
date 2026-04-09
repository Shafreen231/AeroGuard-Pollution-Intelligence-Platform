import React, { useState, useEffect } from 'react';
import {
  Box,
  Grid,
  Paper,
  Typography,
  Card,
  CardContent,
  CardActions,
  Button,
  Chip,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Alert,
  CircularProgress,
  LinearProgress,
  Tabs,
  Tab,
  Tooltip,
} from '@mui/material';
import {
  Edit as EditIcon,
  Delete as DeleteIcon,
  Add as AddIcon,
  Battery90 as BatteryIcon,
  LocationOn as LocationIcon,
  Flight as FlightIcon,
  DirectionsCar as CarIcon,
  DirectionsBoat as BoatIcon,
  Refresh as RefreshIcon,
} from '@mui/icons-material';
import { vehiclesAPI } from '../services/api';
import { Vehicle, VehicleMission, VehicleLocation } from '../types';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;
  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`vehicle-tabpanel-${index}`}
      aria-labelledby={`vehicle-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
}

const VehicleManagement: React.FC = () => {
  const [vehicles, setVehicles] = useState<Vehicle[]>([]);
  const [missions, setMissions] = useState<VehicleMission[]>([]);
  const [locations, setLocations] = useState<VehicleLocation[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [tabValue, setTabValue] = useState(0);
  const [missionDialog, setMissionDialog] = useState(false);
  const [newMission, setNewMission] = useState({
    vehicle: 0,
    mission_type: 'monitoring' as 'monitoring' | 'emergency_response' | 'routine_patrol',
    start_location_longitude: 0,
    start_location_latitude: 0,
    end_location_longitude: 0,
    end_location_latitude: 0,
    description: '',
  });

  const fetchData = async () => {
    try {
      setLoading(true);
      setError(null);
      const [vehiclesRes, missionsRes, locationsRes] = await Promise.all([
        vehiclesAPI.getVehicles(),
        vehiclesAPI.getVehicleMissions(),
        vehiclesAPI.getVehicleLocations(),
      ]);
      
      setVehicles(vehiclesRes.data.results);
      setMissions(missionsRes.data.results);
      setLocations(locationsRes.data.results);
    } catch (err) {
      setError('Failed to fetch vehicle data. Please try again.');
      console.error('Vehicle data fetch error:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 15000); // Refresh every 15 seconds
    return () => clearInterval(interval);
  }, []);

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  const getVehicleIcon = (type: string) => {
    switch (type) {
      case 'drone': return <FlightIcon />;
      case 'ground_robot': return <CarIcon />;
      case 'boat': return <BoatIcon />;
      default: return <CarIcon />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'success';
      case 'maintenance': return 'warning';
      case 'charging': return 'info';
      case 'inactive': return 'default';
      default: return 'default';
    }
  };

  const getMissionStatusColor = (status: string) => {
    switch (status) {
      case 'completed': return 'success';
      case 'in_progress': return 'primary';
      case 'planned': return 'info';
      case 'aborted': return 'error';
      default: return 'default';
    }
  };

  const handleCreateMission = async () => {
    try {
      await vehiclesAPI.createVehicleMission(newMission);
      setMissionDialog(false);
      setNewMission({
        vehicle: 0,
        mission_type: 'monitoring',
        start_location_longitude: 0,
        start_location_latitude: 0,
        end_location_longitude: 0,
        end_location_latitude: 0,
        description: '',
      });
      fetchData();
    } catch (err) {
      console.error('Mission creation error:', err);
    }
  };

  const getBatteryColor = (level: number): string => {
    if (level > 60) return '#4CAF50';
    if (level > 30) return '#FF9800';
    return '#F44336';
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress size={50} />
        <Typography variant="h6" sx={{ ml: 2 }}>Loading vehicle data...</Typography>
      </Box>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      {/* Header */}
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4" component="h1">
          Vehicle Management
        </Typography>
        <Box>
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={() => setMissionDialog(true)}
            sx={{ mr: 1 }}
          >
            New Mission
          </Button>
          <IconButton onClick={fetchData}>
            <RefreshIcon />
          </IconButton>
        </Box>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {/* Tabs */}
      <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
        <Tabs value={tabValue} onChange={handleTabChange}>
          <Tab label="Fleet Overview" />
          <Tab label="Missions" />
          <Tab label="Location History" />
        </Tabs>
      </Box>

      {/* Fleet Overview Tab */}
      <TabPanel value={tabValue} index={0}>
        <Grid container spacing={3}>
          {vehicles.map((vehicle) => (
            <Grid size={{ xs: 12, md: 6, lg: 4 }} key={vehicle.id}>
              <Card>
                <CardContent>
                  <Box display="flex" justifyContent="space-between" alignItems="flex-start" mb={2}>
                    <Box display="flex" alignItems="center">
                      {getVehicleIcon(vehicle.vehicle_type)}
                      <Typography variant="h6" sx={{ ml: 1 }}>
                        {vehicle.name}
                      </Typography>
                    </Box>
                    <Chip 
                      label={vehicle.status} 
                      color={getStatusColor(vehicle.status) as any}
                      size="small"
                    />
                  </Box>

                  <Typography variant="body2" color="text.secondary" gutterBottom>
                    Type: {vehicle.vehicle_type.replace('_', ' ')}
                  </Typography>

                  <Box display="flex" alignItems="center" mb={1}>
                    <BatteryIcon sx={{ mr: 1, color: getBatteryColor(vehicle.battery_level) }} />
                    <Typography variant="body2">
                      Battery: {vehicle.battery_level}%
                    </Typography>
                  </Box>
                  <LinearProgress
                    variant="determinate"
                    value={vehicle.battery_level}
                    sx={{
                      mb: 2,
                      '& .MuiLinearProgress-bar': {
                        backgroundColor: getBatteryColor(vehicle.battery_level),
                      },
                    }}
                  />

                  <Box display="flex" alignItems="center" mb={1}>
                    <LocationIcon sx={{ mr: 1, color: 'text.secondary' }} />
                    <Typography variant="body2">
                      Lat: {vehicle.current_latitude ? Number(vehicle.current_latitude).toFixed(4) : 'N/A'}, 
                      Lng: {vehicle.current_longitude ? Number(vehicle.current_longitude).toFixed(4) : 'N/A'}
                    </Typography>
                  </Box>

                  <Typography variant="body2" color="text.secondary">
                    Last active: {new Date(vehicle.last_active).toLocaleString()}
                  </Typography>
                </CardContent>

                <CardActions>
                  <Button size="small" startIcon={<EditIcon />}>
                    Edit
                  </Button>
                  <Button 
                    size="small" 
                    startIcon={<AddIcon />}
                    onClick={() => {
                      setNewMission({ ...newMission, vehicle: vehicle.id });
                      setMissionDialog(true);
                    }}
                  >
                    Assign Mission
                  </Button>
                </CardActions>
              </Card>
            </Grid>
          ))}
        </Grid>
      </TabPanel>

      {/* Missions Tab */}
      <TabPanel value={tabValue} index={1}>
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Vehicle</TableCell>
                <TableCell>Mission Type</TableCell>
                <TableCell>Status</TableCell>
                <TableCell>Start Time</TableCell>
                <TableCell>Description</TableCell>
                <TableCell>Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {missions.map((mission) => {
                const vehicle = vehicles.find(v => v.id === mission.vehicle);
                return (
                  <TableRow key={mission.id}>
                    <TableCell>
                      <Box display="flex" alignItems="center">
                        {vehicle && getVehicleIcon(vehicle.vehicle_type)}
                        <Typography sx={{ ml: 1 }}>
                          {vehicle?.name || `Vehicle ${mission.vehicle}`}
                        </Typography>
                      </Box>
                    </TableCell>
                    <TableCell>
                      <Chip 
                        label={mission.mission_type.replace('_', ' ')} 
                        size="small"
                        variant="outlined"
                      />
                    </TableCell>
                    <TableCell>
                      <Chip 
                        label={mission.status} 
                        color={getMissionStatusColor(mission.status) as any}
                        size="small"
                      />
                    </TableCell>
                    <TableCell>
                      {new Date(mission.start_time).toLocaleString()}
                    </TableCell>
                    <TableCell>
                      <Tooltip title={mission.description}>
                        <Typography 
                          variant="body2" 
                          sx={{ 
                            maxWidth: 200, 
                            overflow: 'hidden', 
                            textOverflow: 'ellipsis',
                            whiteSpace: 'nowrap'
                          }}
                        >
                          {mission.description}
                        </Typography>
                      </Tooltip>
                    </TableCell>
                    <TableCell>
                      <IconButton size="small">
                        <EditIcon />
                      </IconButton>
                      <IconButton size="small" color="error">
                        <DeleteIcon />
                      </IconButton>
                    </TableCell>
                  </TableRow>
                );
              })}
            </TableBody>
          </Table>
        </TableContainer>
      </TabPanel>

      {/* Location History Tab */}
      <TabPanel value={tabValue} index={2}>
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Vehicle</TableCell>
                <TableCell>Latitude</TableCell>
                <TableCell>Longitude</TableCell>
                <TableCell>Altitude</TableCell>
                <TableCell>Speed</TableCell>
                <TableCell>Timestamp</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {locations.slice(0, 100).map((location) => {
                const vehicle = vehicles.find(v => v.id === location.vehicle);
                return (
                  <TableRow key={location.id}>
                    <TableCell>
                      <Box display="flex" alignItems="center">
                        {vehicle && getVehicleIcon(vehicle.vehicle_type)}
                        <Typography sx={{ ml: 1 }}>
                          {vehicle?.name || `Vehicle ${location.vehicle}`}
                        </Typography>
                      </Box>
                    </TableCell>
                    <TableCell>{location.latitude ? Number(location.latitude).toFixed(6) : 'N/A'}</TableCell>
                    <TableCell>{location.longitude ? Number(location.longitude).toFixed(6) : 'N/A'}</TableCell>
                    <TableCell>{location.altitude ? `${location.altitude}m` : 'N/A'}</TableCell>
                    <TableCell>{location.speed ? `${location.speed} km/h` : 'N/A'}</TableCell>
                    <TableCell>{new Date(location.timestamp).toLocaleString()}</TableCell>
                  </TableRow>
                );
              })}
            </TableBody>
          </Table>
        </TableContainer>
      </TabPanel>

      {/* Mission Creation Dialog */}
      <Dialog open={missionDialog} onClose={() => setMissionDialog(false)} maxWidth="md" fullWidth>
        <DialogTitle>Create New Mission</DialogTitle>
        <DialogContent>
          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid size={{ xs: 12, md: 6 }}>
              <FormControl fullWidth>
                <InputLabel>Vehicle</InputLabel>
                <Select
                  value={newMission.vehicle}
                  onChange={(e) => setNewMission({ ...newMission, vehicle: e.target.value as number })}
                >
                  {vehicles.map((vehicle) => (
                    <MenuItem key={vehicle.id} value={vehicle.id}>
                      {vehicle.name} ({vehicle.vehicle_type})
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            <Grid size={{ xs: 12, md: 6 }}>
              <FormControl fullWidth>
                <InputLabel>Mission Type</InputLabel>
                <Select
                  value={newMission.mission_type}
                  onChange={(e) => setNewMission({ ...newMission, mission_type: e.target.value as any })}
                >
                  <MenuItem value="monitoring">Monitoring</MenuItem>
                  <MenuItem value="emergency_response">Emergency Response</MenuItem>
                  <MenuItem value="routine_patrol">Routine Patrol</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid size={{ xs: 12, md: 6 }}>
              <TextField
                fullWidth
                label="Start Latitude"
                type="number"
                value={newMission.start_location_latitude}
                onChange={(e) => setNewMission({ ...newMission, start_location_latitude: parseFloat(e.target.value) })}
                inputProps={{ step: 0.000001 }}
              />
            </Grid>
            <Grid size={{ xs: 12, md: 6 }}>
              <TextField
                fullWidth
                label="Start Longitude"
                type="number"
                value={newMission.start_location_longitude}
                onChange={(e) => setNewMission({ ...newMission, start_location_longitude: parseFloat(e.target.value) })}
                inputProps={{ step: 0.000001 }}
              />
            </Grid>
            <Grid size={{ xs: 12, md: 6 }}>
              <TextField
                fullWidth
                label="End Latitude"
                type="number"
                value={newMission.end_location_latitude}
                onChange={(e) => setNewMission({ ...newMission, end_location_latitude: parseFloat(e.target.value) })}
                inputProps={{ step: 0.000001 }}
              />
            </Grid>
            <Grid size={{ xs: 12, md: 6 }}>
              <TextField
                fullWidth
                label="End Longitude"
                type="number"
                value={newMission.end_location_longitude}
                onChange={(e) => setNewMission({ ...newMission, end_location_longitude: parseFloat(e.target.value) })}
                inputProps={{ step: 0.000001 }}
              />
            </Grid>
            <Grid size={{ xs: 12 }}>
              <TextField
                fullWidth
                label="Description"
                multiline
                rows={3}
                value={newMission.description}
                onChange={(e) => setNewMission({ ...newMission, description: e.target.value })}
              />
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setMissionDialog(false)}>Cancel</Button>
          <Button onClick={handleCreateMission} variant="contained">Create Mission</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default VehicleManagement;
