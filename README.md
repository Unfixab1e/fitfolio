# FitFolio - Self-Hosted Fitness Tracker

FitFolio is a self-hosted fitness tracking application that integrates with Health Connect (via HCGateway) to automatically sync your health data from various sources like Samsung Health, Google Fit, and smartwatches.

## Features

- 📱 **Mobile-friendly web interface** with responsive design
- 📊 **Track multiple health metrics**:
  - Steps and activity data
  - Weight tracking
  - Sleep monitoring
- 🔄 **Automatic data sync** from Health Connect via HCGateway
- 🐳 **Docker-based deployment** with docker-compose
- 🔐 **User authentication** and data privacy
- 📈 **Data visualization** with charts and graphs
- 🛠️ **REST API** for programmatic access
- ⚡ **Background tasks** with Celery for data processing

## Quick Start

### Prerequisites

- Docker and Docker Compose
- (Optional) HCGateway instance for automatic health data sync

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Unfixab1e/fitfolio.git
   cd fitfolio
   ```

2. **Configure environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

3. **Start the services**:
   ```bash
   cd docker
   docker-compose up -d
   ```

4. **Set up the database**:
   ```bash
   docker-compose exec web python manage.py migrate
   docker-compose exec web python manage.py createsuperuser
   ```

5. **Access the application**:
   - Web interface: http://localhost:8000
   - Admin interface: http://localhost:8000/admin

## Health Connect Integration

FitFolio integrates with [HCGateway](https://github.com/shuchirj/HCGateway) to automatically sync health data from Android's Health Connect.

### Setting up HCGateway Integration

1. **Install the HCGateway Android app** on your phone
2. **Register an account** with HCGateway 
3. **Configure a user in FitFolio**:
   ```bash
   docker-compose exec web python manage.py sync_health_data --setup-user <your-username> <hc-gateway-user-id>
   ```

4. **Enable automatic sync**: The `health-sync` service will automatically sync data every 2 hours.

### Manual Sync

You can manually trigger a health data sync:

```bash
# Sync specific user
docker-compose exec web python manage.py sync_health_data --user <username>

# Sync all users
docker-compose exec web python manage.py sync_health_data --all
```

## API Usage

FitFolio provides a REST API for all data operations:

### Authentication

Use Django's session authentication or basic auth:

```bash
curl -u username:password http://localhost:8000/api/activity/
```

### Endpoints

- **Activity Data**: `/api/activity/`
- **Weight Data**: `/api/weight/`
- **Sleep Data**: `/api/sleep/`
- **Recent Data**: `/api/{activity|weight|sleep}/recent/`

### Example API Calls

```bash
# Get recent activity data
curl -u admin:password http://localhost:8000/api/activity/recent/

# Add new weight data
curl -X POST -H "Content-Type: application/json" \
  -u admin:password \
  -d '{"date": "2025-09-26", "weight": 75.5}' \
  http://localhost:8000/api/weight/

# Add sleep data
curl -X POST -H "Content-Type: application/json" \
  -u admin:password \
  -d '{"date": "2025-09-26", "total_sleep_minutes": 480}' \
  http://localhost:8000/api/sleep/
```

## Architecture

### Services

- **web**: Django application server
- **db**: PostgreSQL database (optional, SQLite by default)
- **redis**: Redis for Celery task queue
- **celery**: Background task worker
- **celery-beat**: Task scheduler
- **health-sync**: Dedicated service for HCGateway integration

### Data Models

- **User**: Extended Django user with profiles
- **ActivityData**: Steps, distance, calories
- **WeightData**: Weight measurements over time
- **SleepData**: Sleep duration, quality, and detailed metrics
- **UserProfile**: HCGateway integration settings

## Development

### Local Development Setup

1. **Install Python dependencies**:
   ```bash
   cd fitfolio
   pip install -r requirements/development.txt
   ```

2. **Run migrations**:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

3. **Start development server**:
   ```bash
   python manage.py runserver
   ```

### Running Tests

```bash
python manage.py test
```

## Configuration

### Environment Variables

- `FITFOLIO_PORT`: Web server port (default: 8000)
- `HCGATEWAY_API_URL`: HCGateway instance URL
- `POSTGRES_*`: PostgreSQL configuration (optional)
- `REDIS_PORT`: Redis port (default: 6379)

### HCGateway Setup

For self-hosting HCGateway, refer to the [HCGateway documentation](https://github.com/shuchirj/HCGateway).

## Mobile Access

The web interface is fully responsive and works well on mobile devices. For a native app experience:

1. Add the web app to your phone's home screen
2. The interface will work as a Progressive Web App (PWA)

## Security

- All data stays on your server
- User authentication required for access
- HTTPS recommended for production
- Regular backups recommended

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if needed
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Support

- GitHub Issues: [Report bugs or request features](https://github.com/Unfixab1e/fitfolio/issues)
- HCGateway Issues: [HCGateway repository](https://github.com/shuchirj/HCGateway)

## Roadmap

### Completed ✅
- Basic fitness tracking (steps, weight, sleep)
- Mobile-responsive web interface
- HCGateway integration framework
- Docker deployment setup
- REST API with authentication

### Planned 🚧
- Enhanced data visualization with charts
- Food tracking integration
- Medical data tracking
- LLM integration for data analysis
- Native mobile app wrapper
- Export/import functionality
- Multi-user households support