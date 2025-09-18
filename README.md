# TailoRent - Tailor at your doorstep

A comprehensive platform connecting customers with skilled tailors, fashion designers, and fabric vendors. Built with Django REST Framework backend and React TypeScript frontend.

## 🚀 Features

### Core Functionality
- **User Management**: Multi-role authentication (Customer, Tailor, Fashion Designer, Vendor, Admin)
- **OTP Authentication**: Email and SMS-based verification
- **Service Booking**: Book tailoring and fashion design services
- **Marketplace**: Browse and purchase fabrics and materials
- **Professional Profiles**: Discover and connect with skilled professionals
- **Real-time Notifications**: Email and SMS notifications via Celery

### Technical Features
- **Backend**: Django 5.2 with REST Framework
- **Frontend**: React 18 with TypeScript and Tailwind CSS
- **Database**: MySQL with optimized queries
- **Image Storage**: Cloudinary integration
- **Background Tasks**: Celery with Redis
- **Authentication**: JWT tokens with refresh mechanism
- **API Documentation**: Auto-generated with DRF Spectacular

## 🛠️ Tech Stack

### Backend
- **Framework**: Django 5.2
- **API**: Django REST Framework
- **Database**: MySQL
- **Authentication**: JWT (Simple JWT)
- **Background Tasks**: Celery
- **Message Broker**: Redis
- **Image Storage**: Cloudinary
- **Email**: SendGrid
- **SMS**: Twilio
- **OTP**: django-otp

### Frontend
- **Framework**: React 18
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **State Management**: React Context
- **HTTP Client**: Axios
- **Forms**: React Hook Form
- **Notifications**: React Hot Toast
- **Icons**: Heroicons

## 📁 Project Structure

```
TailoRent/
├── backend/
│   ├── config/                 # Django configuration
│   │   ├── settings/          # Environment-specific settings
│   │   ├── urls.py            # Main URL configuration
│   │   └── celery.py          # Celery configuration
│   ├── apps/                  # Django applications
│   │   ├── profiles/          # User management & authentication
│   │   ├── bookings/          # Service booking system
│   │   └── marketplace/       # Products & services marketplace
│   ├── requirements/          # Python dependencies
│   ├── tests/                 # Test suite
│   ├── scripts/               # Utility scripts
│   └── manage.py
├── frontend/                  # React application
│   ├── src/
│   │   ├── components/        # Reusable UI components
│   │   ├── pages/            # Page components
│   │   ├── contexts/         # React contexts
│   │   ├── services/         # API services
│   │   └── App.tsx
│   ├── public/
│   └── package.json
└── README.md
```

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- Node.js 18+
- MySQL 8.0+
- Redis 6.0+

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd TailoRent/backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment configuration**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Database setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. **Start development server**
   ```bash
   python manage.py runserver
   ```

7. **Start Celery worker** (in a separate terminal)
   ```bash
   celery -A config worker --loglevel=info
   ```

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd ../frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Environment configuration**
   ```bash
   cp .env.example .env
   # Edit .env with your API URL
   ```

4. **Start development server**
   ```bash
   npm start
   ```

## 🔧 Configuration

### Environment Variables

#### Backend (.env)
```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Settings (MySQL)
DB_NAME=tailorent_db
DB_USER=root
DB_PASSWORD=your-mysql-password
DB_HOST=localhost
DB_PORT=3306

# Redis Settings
REDIS_URL=redis://localhost:6379/0

# Cloudinary Settings
CLOUDINARY_CLOUD_NAME=your-cloudinary-cloud-name
CLOUDINARY_API_KEY=your-cloudinary-api-key
CLOUDINARY_API_SECRET=your-cloudinary-api-secret

# Email Settings (SendGrid)
SENDGRID_API_KEY=your-sendgrid-api-key
DEFAULT_FROM_EMAIL=noreply@tailorent.com

# Twilio Settings (for SMS OTP)
TWILIO_ACCOUNT_SID=your-twilio-account-sid
TWILIO_AUTH_TOKEN=your-twilio-auth-token
TWILIO_PHONE_NUMBER=your-twilio-phone-number
```

#### Frontend (.env)
```env
REACT_APP_API_URL=http://localhost:8000/api
```

## 📚 API Documentation

### Authentication Endpoints
- `POST /api/profiles/register/` - User registration
- `POST /api/profiles/login/` - Email/password login
- `POST /api/profiles/otp-login/` - Send OTP to phone
- `POST /api/profiles/otp-verify/` - Verify OTP
- `POST /api/profiles/email-verify/` - Verify email
- `POST /api/profiles/logout/` - Logout user

### User Management
- `GET /api/profiles/dashboard/` - User dashboard data
- `PATCH /api/profiles/profile-update/` - Update profile
- `POST /api/profiles/change-password/` - Change password
- `GET /api/profiles/professionals/` - List professionals

### Bookings
- `GET /api/bookings/` - List bookings
- `POST /api/bookings/` - Create booking
- `GET /api/bookings/{id}/` - Get booking details
- `PATCH /api/bookings/{id}/` - Update booking

### Marketplace
- `GET /api/marketplace/products/` - List products
- `POST /api/marketplace/products/` - Create product
- `GET /api/marketplace/services/` - List services
- `POST /api/marketplace/services/` - Create service

## 🧪 Testing

### Backend Tests
```bash
cd backend
python manage.py test
# or with pytest
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 🚀 Deployment

### Production Settings
1. Update `config/settings/production.py` with production values
2. Set environment variables
3. Run migrations
4. Collect static files
5. Configure web server (Nginx)
6. Set up process manager (PM2 or systemd)

### Docker Deployment
```bash
# Build and run with docker-compose
docker-compose up --build
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support, email support@tailorent.com or create an issue in the repository.

## 🔮 Roadmap

- [ ] Mobile app (React Native)
- [ ] Real-time chat
- [ ] Video consultations
- [ ] Payment integration
- [ ] Advanced analytics
- [ ] Multi-language support
- [ ] AI-powered recommendations

---

Built with ❤️ by the TailoRent team