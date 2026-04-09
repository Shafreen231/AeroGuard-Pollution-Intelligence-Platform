# Copilot Instructions for Pollution Monitoring System

<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

## Project Overview
This is a Pollution Monitoring and Forecasting system using unmanned vehicles with React frontend and Django backend.

## Technology Stack
- **Frontend**: React.js with TypeScript, Leaflet for maps, Chart.js for visualizations
- **Backend**: Django with Django REST Framework
- **Database**: SQLite (development), PostgreSQL (production)
- **ML**: scikit-learn, pandas, numpy for pollution forecasting
- **APIs**: OpenWeatherMap Air Pollution API for external data

## Code Style Guidelines
- Use TypeScript for React components
- Follow Django REST framework conventions
- Use functional components with hooks in React
- Implement proper error handling and validation
- Use environment variables for API keys and sensitive data
- Follow PEP 8 for Python code
- Use meaningful variable and function names

## Key Features
- Interactive dashboard with map visualization (green/orange/red zones)
- Real-time vehicle tracking and sensor data management
- ML-based pollution forecasting for next day predictions
- External pollution API integration
- Vehicle fleet management
- Responsive design for mobile and desktop

## Security Considerations
- Validate all user inputs
- Use CORS properly between frontend and backend
- Secure API endpoints with authentication where needed
- Handle sensitive vehicle and sensor data appropriately
