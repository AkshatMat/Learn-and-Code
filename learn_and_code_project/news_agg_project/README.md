# News Aggregator Project

A comprehensive news aggregation platform with a FastAPI backend and CLI frontend, featuring intelligent content extraction, AI-powered keyword analysis, and personalized user notifications.

##  Features

### Core Functionality
- **Multi-source News Aggregation**: Fetches news from multiple APIs with fallback support
- **Intelligent Content Extraction**: Uses multiple scraping strategies (BeautifulSoup4, Newspaper3k, Selenium)
- **AI-Powered Keyword Extraction**: Leverages AWS Bedrock (Claude) for intelligent keyword analysis
- **Personalized Notifications**: User preference-based news alerts
- **User Management**: Secure authentication with JWT tokens and bcrypt password hashing

### User Features
- **News Browsing**: Today's headlines, date range filtering, category-based browsing
- **Article Management**: Save/unsave articles, like/dislike feedback
- **Advanced Search**: Keyword-based article search
- **Personalized Dashboard**: User-specific saved articles and preferences

### Admin Features
- **API Management**: View, add, update, and delete news API configurations
- **System Monitoring**: Track API status and usage
- **Database Management**: Manage news sources and configurations

##  Architecture

### Project Structure
```
news_agg_project/
├── client/                          # FastAPI + CLI Application
│   ├── api_client/                  # HTTP API clients
│   ├── cli/                         # Command-line interface
│   ├── config/                      # Configuration settings
│   ├── db/                          # Database layer
│   │   ├── modules/                 # Database managers
│   │   └── connection.py            # Database connection pool
│   ├── server/                      # FastAPI server
│   │   ├── fast_api/
│   │   │   ├── routers/             # API endpoints
│   │   │   └── schemas/             # Pydantic models
│   │   ├── services/                # Core services
│   │   ├── scrapers/                # Web scraping modules
│   │   ├── repositories/            # Data access layer
│   │   └── models/                  # Data models
│   └── utils/                       # Utilities and helpers
├── start_cli.py                     # CLI entry point
├── start_fastapi.py                 # FastAPI server entry point
└── README.md
```

### Technology Stack
- **Backend**: Python, FastAPI, PostgreSQL, psycopg2
- **News Sources**: NewsAPI, multiple scraping strategies
- **AI/ML**: AWS Bedrock (Claude)
- **Authentication**: JWT tokens, bcrypt password hashing
- **Scraping**: BeautifulSoup4, Newspaper3k, Selenium
- **CLI**: Custom console interface

##  Prerequisites

- Python 3.8+
- PostgreSQL database
- AWS account (for Bedrock keyword extraction)
- News API key (optional, for fallback)

##  Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd news_agg_project
```

### 2. Create Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup
Create a PostgreSQL database and update the configuration in `client/config/settings.py`:
```python
DB_NAME = "news_agg"
DB_USER = "your_username"
DB_PASSWORD = "your_password"
DB_HOST = "localhost"
DB_PORT = "5432"
```

### 5. Environment Variables
Create a `.env` file in the root directory:
```env
# Database Configuration
DB_NAME=news_agg
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

# JWT Configuration
JWT_SECRET=your_jwt_secret_key
JWT_ALGORITHM=HS256

# AWS Configuration (for keyword extraction)
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=us-east-1
BEDROCK_MODEL_ID=anthropic.claude-3-5-sonnet-20240620-v1:0

# News API (optional)
NEWS_API_KEY=your_news_api_key
```

##  Usage

### Starting the Application

#### 1. Start the FastAPI Server
```bash
python start_fastapi.py
```
The server will be available at `http://127.0.0.1:8000`

#### 2. Start the CLI Client
```bash
python start_cli.py
```

### User Workflow

#### 1. User Registration/Login
- Choose "Sign Up" to create a new account
- Choose "Login" to access existing account
- Support for both regular users and admin users

#### 2. News Browsing
- **Today's Headlines**: View latest news by category
- **Date Range**: Browse news from specific date ranges
- **Search**: Find articles by keywords
- **Saved Articles**: Access your bookmarked articles

#### 3. Article Actions
- Save articles for later reading
- Like/dislike articles for feedback
- View detailed article information

#### 4. Notifications
- Configure notification preferences by category
- Set keyword-based alerts
- View unread notifications

### Admin Workflow

#### 1. Admin Login
- Use admin credentials to access admin panel
- Available options: View All API Details, Add/Update API, Delete API, Update API Status

#### 2. API Management
- **View All APIs**: See all configured news APIs with status
- **View Specific API**: Get detailed information about a specific API
- **Add/Update API**: Configure new APIs or modify existing ones
- **Delete API**: Remove APIs from the system
- **Update Status**: Change API status (Active/Inactive/Maintenance)

##  Database Schema

### Core Tables
- `news_table`: Stored articles with metadata
- `user_table`: User accounts and authentication
- `saved_article_table`: User's saved articles
- `user_notification_table`: User notifications
- `user_notification_config_table`: Notification preferences
- `user_keyword_table`: User's keyword preferences
- `api_table`: API configuration and status

##  API Endpoints

### Authentication
- `POST /signup_user/` - User registration
- `POST /login_user/` - User login
- `POST /login_admin/` - Admin login

### News
- `GET /headlines/today` - Today's headlines
- `POST /headlines/range` - Headlines by date range
- `GET /headlines/search` - Search articles by keyword

### Articles
- `POST /articles/save_article` - Save article
- `GET /articles/saved_articles/{user_id}` - Get saved articles
- `DELETE /articles/delete_article` - Delete saved article
- `POST /articles/feedback` - Submit article feedback

### Notifications
- `GET /notifications/unviewed/{user_id}` - Get unviewed notifications
- `PUT /notifications/mark_viewed/{user_id}` - Mark notifications as viewed
- `PUT /notifications/preferences` - Update notification preferences
- `PUT /notifications/keywords` - Update keyword preferences

### Admin APIs
- `GET /admin/apis/` - Get all API details
- `GET /admin/apis/{api_name}` - Get specific API details
- `POST /admin/apis/` - Add/Update API
- `DELETE /admin/apis/` - Delete API
- `PUT /admin/apis/status` - Update API status

##  Configuration

### Settings Files
- `client/config/settings.py`: Client-side configuration
- `server/src/config/settings.py`: Server-side configuration

### Key Configuration Options
- Database connection settings
- API endpoints and timeouts
- AWS Bedrock configuration
- News categories and limits
- Content validation rules
