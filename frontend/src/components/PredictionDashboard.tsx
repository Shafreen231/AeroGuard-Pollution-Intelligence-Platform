import React, { useState, useEffect } from 'react';
import {
  Box,
  Grid,
  Paper,
  Typography,
  Card,
  CardContent,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Alert,
  CircularProgress,
  Chip,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  IconButton,
  Tooltip,
} from '@mui/material';
import {
  Refresh as RefreshIcon,
  TrendingUp as TrendingUpIcon,
  TrendingDown as TrendingDownIcon,
  Analytics as AnalyticsIcon,
} from '@mui/icons-material';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip as RechartsTooltip,
  Legend,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from 'recharts';
import { predictionsAPI, monitoringAPI } from '../services/api';
import { PollutionPrediction, SensorReading } from '../types';

const PredictionDashboard: React.FC = () => {
  const [predictions, setPredictions] = useState<PollutionPrediction[]>([]);
  const [sensorData, setSensorData] = useState<SensorReading[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [timeRange, setTimeRange] = useState<'24h' | '7d' | '30d'>('7d');
  const [lastUpdated, setLastUpdated] = useState<Date | null>(null);

  const fetchData = async () => {
    try {
      setLoading(true);
      setError(null);
      const [predictionsRes, sensorRes] = await Promise.all([
        predictionsAPI.getLatestPredictions(),
        monitoringAPI.getLatestReadings(),
      ]);
      
      setPredictions(predictionsRes.data);
      setSensorData(sensorRes.data);
      setLastUpdated(new Date());
    } catch (err) {
      setError('Failed to fetch prediction data. Please try again.');
      console.error('Prediction data fetch error:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 60000); // Refresh every minute
    return () => clearInterval(interval);
  }, []);

  const getAQIColor = (aqi: number): string => {
    if (aqi <= 50) return '#4CAF50';
    if (aqi <= 100) return '#FFEB3B';
    if (aqi <= 150) return '#FF9800';
    if (aqi <= 200) return '#F44336';
    if (aqi <= 300) return '#9C27B0';
    return '#8D6E63';
  };

  const getAQILevel = (aqi: number): string => {
    if (aqi <= 50) return 'Good';
    if (aqi <= 100) return 'Moderate';
    if (aqi <= 150) return 'Unhealthy for Sensitive';
    if (aqi <= 200) return 'Unhealthy';
    if (aqi <= 300) return 'Very Unhealthy';
    return 'Hazardous';
  };

  const getTrendIcon = (current: number, predicted: number) => {
    if (predicted > current * 1.1) return <TrendingUpIcon color="error" />;
    if (predicted < current * 0.9) return <TrendingDownIcon color="success" />;
    return <AnalyticsIcon color="primary" />;
  };

  // Prepare chart data
  const chartData = predictions.map((pred, index) => ({
    name: `Point ${index + 1}`,
    predicted: pred.predicted_aqi,
    confidence: pred.confidence_score * 100,
    date: new Date(pred.prediction_date).toLocaleDateString(),
  }));

  const currentAvg = sensorData.length > 0 
    ? sensorData.reduce((sum, reading) => sum + reading.aqi, 0) / sensorData.length 
    : 0;
  
  const predictedAvg = predictions.length > 0 
    ? predictions.reduce((sum, pred) => sum + pred.predicted_aqi, 0) / predictions.length 
    : 0;

  // Model distribution data
  const modelDistribution = predictions.reduce((acc, pred) => {
    acc[pred.model_used] = (acc[pred.model_used] || 0) + 1;
    return acc;
  }, {} as Record<string, number>);

  const modelPieData = Object.entries(modelDistribution).map(([model, count]) => ({
    name: model,
    value: count,
  }));

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8'];

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress size={50} />
        <Typography variant="h6" sx={{ ml: 2 }}>Loading predictions...</Typography>
      </Box>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      {/* Header */}
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4" component="h1">
          Pollution Prediction Dashboard
        </Typography>
        <Box display="flex" alignItems="center" gap={2}>
          <FormControl size="small" sx={{ minWidth: 120 }}>
            <InputLabel>Time Range</InputLabel>
            <Select
              value={timeRange}
              label="Time Range"
              onChange={(e) => setTimeRange(e.target.value as any)}
            >
              <MenuItem value="24h">24 Hours</MenuItem>
              <MenuItem value="7d">7 Days</MenuItem>
              <MenuItem value="30d">30 Days</MenuItem>
            </Select>
          </FormControl>
          {lastUpdated && (
            <Typography variant="body2" color="text.secondary">
              Last updated: {lastUpdated.toLocaleTimeString()}
            </Typography>
          )}
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

      {/* Summary Cards */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid size={{ xs: 12, sm: 6, md: 3 }}>
          <Card>
            <CardContent>
              <Typography color="text.secondary" gutterBottom>
                Current Avg AQI
              </Typography>
              <Typography variant="h4" sx={{ color: getAQIColor(currentAvg) }}>
                {Math.round(currentAvg)}
              </Typography>
              <Chip 
                label={getAQILevel(currentAvg)} 
                size="small"
                sx={{ 
                  mt: 1,
                  backgroundColor: getAQIColor(currentAvg),
                  color: 'white'
                }}
              />
            </CardContent>
          </Card>
        </Grid>

        <Grid size={{ xs: 12, sm: 6, md: 3 }}>
          <Card>
            <CardContent>
              <Box display="flex" justifyContent="space-between" alignItems="center">
                <Box>
                  <Typography color="text.secondary" gutterBottom>
                    Predicted Avg AQI
                  </Typography>
                  <Typography variant="h4" sx={{ color: getAQIColor(predictedAvg) }}>
                    {Math.round(predictedAvg)}
                  </Typography>
                </Box>
                {getTrendIcon(currentAvg, predictedAvg)}
              </Box>
              <Chip 
                label={getAQILevel(predictedAvg)} 
                size="small"
                sx={{ 
                  mt: 1,
                  backgroundColor: getAQIColor(predictedAvg),
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
                Predictions Generated
              </Typography>
              <Typography variant="h4">
                {predictions.length}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Total forecasts
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid size={{ xs: 12, sm: 6, md: 3 }}>
          <Card>
            <CardContent>
              <Typography color="text.secondary" gutterBottom>
                Avg Confidence
              </Typography>
              <Typography variant="h4">
                {predictions.length > 0 
                  ? Math.round(predictions.reduce((sum, p) => sum + p.confidence_score, 0) / predictions.length * 100)
                  : 0}%
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Model reliability
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Charts */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid size={{ xs: 12, lg: 8 }}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              AQI Predictions Over Time
            </Typography>
            <ResponsiveContainer width="100%" height={400}>
              <LineChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <RechartsTooltip />
                <Legend />
                <Line 
                  type="monotone" 
                  dataKey="predicted" 
                  stroke="#8884d8" 
                  strokeWidth={2}
                  name="Predicted AQI"
                />
                <Line 
                  type="monotone" 
                  dataKey="confidence" 
                  stroke="#82ca9d" 
                  strokeWidth={2}
                  name="Confidence %"
                />
              </LineChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        <Grid size={{ xs: 12, lg: 4 }}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Model Usage Distribution
            </Typography>
            <ResponsiveContainer width="100%" height={400}>
              <PieChart>
                <Pie
                  data={modelPieData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={(entry: any) => `${entry.name} ${(entry.percent * 100).toFixed(0)}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {modelPieData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <RechartsTooltip />
              </PieChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>
      </Grid>

      {/* Detailed Predictions Table */}
      <Paper sx={{ p: 2 }}>
        <Typography variant="h6" gutterBottom>
          Detailed Predictions
        </Typography>
        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Location</TableCell>
                <TableCell>Predicted AQI</TableCell>
                <TableCell>Level</TableCell>
                <TableCell>Confidence</TableCell>
                <TableCell>Model</TableCell>
                <TableCell>Prediction Date</TableCell>
                <TableCell>Created</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {predictions.map((prediction) => (
                <TableRow key={prediction.id}>
                  <TableCell>
                    {prediction.latitude ? Number(prediction.latitude).toFixed(4) : 'N/A'}, {prediction.longitude ? Number(prediction.longitude).toFixed(4) : 'N/A'}
                  </TableCell>
                  <TableCell>
                    <Typography sx={{ color: getAQIColor(prediction.predicted_aqi) }}>
                      {Math.round(prediction.predicted_aqi)}
                    </Typography>
                  </TableCell>
                  <TableCell>
                    <Chip 
                      label={getAQILevel(prediction.predicted_aqi)} 
                      size="small"
                      sx={{ 
                        backgroundColor: getAQIColor(prediction.predicted_aqi),
                        color: 'white'
                      }}
                    />
                  </TableCell>
                  <TableCell>
                    <Tooltip title={`${prediction.confidence_score ? (Number(prediction.confidence_score) * 100).toFixed(1) : '0'}%`}>
                      <Box display="flex" alignItems="center">
                        <Typography variant="body2">
                          {prediction.confidence_score ? Math.round(Number(prediction.confidence_score) * 100) : 0}%
                        </Typography>
                      </Box>
                    </Tooltip>
                  </TableCell>
                  <TableCell>
                    <Chip label={prediction.model_used} size="small" variant="outlined" />
                  </TableCell>
                  <TableCell>
                    {new Date(prediction.prediction_date).toLocaleDateString()}
                  </TableCell>
                  <TableCell>
                    {new Date(prediction.created_at).toLocaleString()}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Paper>
    </Box>
  );
};

export default PredictionDashboard;
