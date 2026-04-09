# AeroGuard Pollution Intelligence Platform

🚁 **Advanced Environmental Monitoring & Forecasting System with Professional Ground Station Interface**

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.11-blue.svg)
![React](https://img.shields.io/badge/react-19.1-blue.svg)
![Django](https://img.shields.io/badge/django-5.2-green.svg)

A comprehensive pollution monitoring and forecasting platform that combines real-time environmental data collection from unmanned vehicles (drones, ground robots, boats) with machine learning-powered predictions, all presented through a sophisticated military-grade ground control station interface.

## ✨ Key Features

### 🎯 Professional Ground Station Dashboard
- Military/aerospace-inspired radar interface with Matrix green theme
- Real-time animated radar sweep and connection status indicators
- Professional dark theme optimized for mission-critical operations
- Sophisticated UI animations and tactical display elements

### 🌍 Real-Time Environmental Monitoring
- Live pollution zone visualization with color-coded risk areas (Green/Orange/Red)
- Interactive Leaflet maps with custom pollution overlays
- Real-time sensor data streaming from multiple vehicle types
- PM2.5, PM10, NO₂, O₃ monitoring with live updates

### 🚁 Advanced Fleet Management
- Multi-vehicle coordination (drones, ground robots, boats)
- Live vehicle status tracking and location monitoring
- Professional vehicle management cards with status indicators
- Real-time communication status and data streaming

### 🧠 AI-Powered Forecasting
- Machine learning pollution predictions for next-day forecasting
- Historical data analysis and trend visualization
- Confidence scoring for prediction accuracy
- Environmental pattern recognition and alerts

### 📊 Comprehensive Analytics
- Air Quality Index (AQI) monitoring and alerts
- Environmental data visualization with professional charts
- Historical trend analysis and reporting
- Export capabilities for research and compliance

## 🛠️ Technology Stack

### Frontend
- **React.js 19.1** with TypeScript for type safety
- **Material-UI v7** for professional component library
- **Leaflet** for interactive mapping and geospatial visualization
- **Chart.js** for advanced data visualization
- **Custom animations** for ground station experience

### Backend
- **Django 5.2** with Django REST Framework
- **SQLite** (development) / **PostgreSQL** (production ready)
- **Python 3.11** with modern async support
- **RESTful API** architecture with comprehensive endpoints

### Machine Learning & Analytics
- **scikit-learn** for pollution forecasting models
- **pandas & numpy** for data processing and analysis
- **Historical data analysis** with pattern recognition
- **Predictive modeling** with confidence metrics

### External Integrations
- **OpenWeatherMap Air Pollution API** for external data
- **Real-time environmental data sources**
- **Configurable API endpoints** for custom integrations

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- npm or yarn
- Git

### Backend Setup
```bash
# Clone the repository
git clone https://github.com/salmaanit26/AeroGuard-Pollution-Intelligence-Platform.git
cd AeroGuard-Pollution-Intelligence-Platform

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
cd backend
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start Django server
python manage.py runserver
```

### Frontend Setup
```bash
# Install dependencies
cd frontend
npm install

# Start React development server
npm start
```

### Access the Application
- **Ground Station Interface:** `http://localhost:3000`
- **API Documentation:** `http://localhost:8000/api`
- **Django Admin:** `http://localhost:8000/admin`

## 🎮 Live Demo Features

### Professional Interface
- Military-grade ground control station aesthetic
- Matrix green color scheme with tactical elements
- Animated radar sweep with authentic sound effects
- Real-time status indicators and alerts

### Real-time Monitoring
- Live pollution monitoring with 30-second refresh intervals
- Interactive maps with clickable pollution zones
- Vehicle tracking with live position updates
- Environmental sensor data streaming

### Predictive Analytics
- Next-day pollution forecasting with ML models
- Confidence metrics and uncertainty quantification
- Historical trend analysis and pattern recognition
- Alert system for pollution threshold breaches

## 🏆 Use Cases

- **Environmental Research Institutions:** Academic research and data analysis
- **Government Agencies:** Municipal pollution monitoring and compliance
- **Smart Cities:** Integrated environmental management systems
- **Industrial Monitoring:** Corporate pollution compliance and reporting
- **Emergency Response:** Environmental disaster assessment and response
- **Public Health:** Air quality monitoring for health advisories

## 📁 Project Structure

```
AeroGuard-Pollution-Intelligence-Platform/
├── backend/                    # Django REST API
│   ├── pollution_monitor/      # Main Django project
│   ├── monitoring/            # Monitoring app
│   ├── vehicles/              # Vehicle management app
│   ├── ml_prediction/         # ML prediction app
│   └── requirements.txt       # Python dependencies
├── frontend/                  # React application
│   ├── public/               # Static assets
│   ├── src/                  # Source code
│   │   ├── components/       # React components
│   │   ├── services/         # API services
│   │   └── types/           # TypeScript definitions
│   └── package.json         # Node dependencies
├── .github/                 # GitHub workflows
├── docs/                    # Documentation
└── README.md               # This file
```

## 🔧 Configuration

### Environment Variables
Create `.env` files in both frontend and backend directories:

**Backend (.env):**
```env
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///db.sqlite3
OPENWEATHER_API_KEY=your-api-key
```

**Frontend (.env):**
```env
REACT_APP_API_BASE_URL=http://localhost:8000/api
REACT_APP_MAP_CENTER_LAT=40.7128
REACT_APP_MAP_CENTER_LNG=-74.0060
```

### Customization
- **Pollution Thresholds:** Modify in `backend/monitoring/models.py`
- **Vehicle Types:** Configure in `backend/vehicles/models.py`
- **UI Theme:** Customize in `frontend/src/theme/`
- **Map Settings:** Update in `frontend/src/components/`

## 🧪 Testing

### Backend Tests
```bash
cd backend
python manage.py test
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 📊 API Documentation

### Main Endpoints
- `GET /api/monitoring/zones/` - Pollution zones
- `GET /api/monitoring/readings/latest/` - Latest sensor readings
- `GET /api/vehicles/vehicles/` - Vehicle fleet status
- `GET /api/ml/predictions/latest/` - ML predictions

### Authentication
Currently using session-based authentication. JWT support planned for v2.0.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenWeatherMap for environmental data API
- Material-UI team for the component library
- Leaflet community for mapping capabilities
- Django and React communities for excellent frameworks

## 📞 Support

For support, please open an issue on GitHub or contact the development team.

---

**Built for professionals who demand precision, reliability, and cutting-edge environmental intelligence.**

⭐ **Star this repository if you find it useful!**
