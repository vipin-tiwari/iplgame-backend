# IPL Game Auction Simulator API

An educational backend API that simulates the Indian Premier League (IPL) cricket player auctions, designed to help students understand the dynamics of betting, auction strategies, and financial decision-making in a fun and engaging way.

## 🎯 Project Purpose

This project aims to:
1. Create an interactive platform for students to learn about auction mechanics and financial literacy
2. Demonstrate real-world applications of strategic bidding and resource management
3. Provide hands-on experience with cricket-themed financial decision-making
4. Enable educators to teach complex economic concepts through gamification

## Requirements
* Python 3.6.1+
* `virtualenv` and `pip`
* A free Heroku account
* [Heroku Toolbelt](https://devcenter.heroku.com/articles/heroku-cli)

## Optional Tools
- [Postman](https://www.getpostman.com/) -- Cool tool for testing REST API's and auction endpoints
- [DBeaver](http://dbeaver.jkiss.org/) -- Cross-platform database client for managing auction data

## Included Features
The code comes with these features built in:

### General
* Pre-configured to be deployed to a Heroku app with a PostgreSQL database
* Pre-defined sample endpoints and account management endpoints
* Application logic for handling user account creation and sessions
* IPL auction game state management

### Utilities
* `RequestParser`: Class that makes it easy to define, enforce, and parse endpoint parameters
* `ResponseJson`: Class that standardizes the JSON format of endpoint responses
* `Logger`: Class for writing application logs and auction event logs

### Database
* `Alembic` pre-configured to initialize and upgrade database schemas
* Pre-defined `SQLAlchemy` model classes for user accounts, user sessions, and auction logging
* `SQLAlchemy` database session management
* Light wrapper around `psycopg2` for handling custom queries and connection management

### Authentication and Security
* Function decorators for endpoint authentication and JSON validation
* AES encrypt / decrypt
* Hash generation / verification using `pbkdf2_sha256` (storing password)
* JWT generation / verification for secure auction sessions

## Setup Instructions

### Heroku Setup
Execute these commands to create your Heroku app and configure the IPL Game environment:
```bash
heroku login
heroku apps:create your-ipl-game-app
heroku config:set JWT_SECRET="your_secret_key" --app your-ipl-game-app
heroku config:set JWT_ISS="IPL Game Auction" --app your-ipl-game-app
heroku addons:create heroku-postgresql --app your-ipl-game-app
```

### Local Environment
Set up your local development environment:
```bash
git clone https://github.com/yourusername/ipl-game-api.git
cd ipl-game-api
git remote add heroku git@heroku.com:your-ipl-game-app.git

virtualenv venv -p /usr/bin/python3.6
source venv/bin/activate
pip install -r requirements.txt
```

Configure local environment variables:
```bash
heroku config --app your-ipl-game-app --shell > .env
cp .env .bash_env
# Add 'export ' to each line in .bash_env
```

### Initializing the Database
Initialize the database with auction tables and required schemas:
```bash
source .bash_env
alembic upgrade head
```

### Testing Locally
Start the local server:
```bash
# Option 1: Using Heroku
heroku local web

# Option 2: Using Python directly
python rundebug.py
```

### Deploying your Code
Deploy to Heroku:
```bash
git push heroku master
```
Your IPL Game API will be live at: `https://your-ipl-game-app.herokuapp.com`

## 🎮 API Endpoints

### Core System Endpoints
- `GET /api/hello`: Test endpoint
- `GET /api/echo`: Parameter parsing example
- `GET /api/protectedhello`: Protected endpoint example
- `POST /api/account`: Create user account
- `GET /api/session`: Login
- `DELETE /api/session`: Logout

### Game Management Endpoints
```bash
# Get game state
GET /gamestate?id=9713880169

# Update bid
POST /gamestate/9713880169
Content-Type: application/json
{
    "bidvalue": 50,
    "bidwinningteam": "Team-3",
    "playerId": 1664,
    "role": "bowler"
}

# Reset game
GET /gamestate/reset
```

## 🛠 Core Libraries
* [Flask](http://flask.pocoo.org/) - Web framework
* [Flask-Restful](https://flask-restful.readthedocs.io/en/0.3.5/) - REST API framework
* [Waitress](http://docs.pylonsproject.org/projects/waitress/en/latest/) - Production WSGI server
* [SQLAlchemy](https://www.sqlalchemy.org/) - Database ORM
* [Alembic](http://alembic.zzzcomputing.com/en/latest/) - Database migrations
* [psycopg2](http://initd.org/psycopg/) - PostgreSQL adapter

## 📚 Educational Resources

The API is designed to help teach:
- Auction dynamics and bidding strategies
- Budget management and resource allocation
- Risk assessment and decision-making
- Market value estimation
- Team building and resource optimization

## Advanced Usage

### Updating the Schema
When you need to modify the auction database schema:
```bash
alembic revision --autogenerate -m "update details"
alembic upgrade head
```

### API Examples

#### Place a Bid
```bash
curl -X POST \
  http://localhost:8000/gamestate/9713880169 \
  -H 'cache-control: no-cache' \
  -H 'content-type: application/json' \
  -d '{
    "bidvalue": 50,
    "bidwinningteam": "Team-3",
    "playerId": 1664,
    "role": "bowler"
}'
```

#### Get Game State
```bash
curl http://ipl-game-lb-790669502.us-east-2.elb.amazonaws.com:8000/gamestate?id=9713880169
```

#### Reset Game
```bash
curl http://ipl-game-lb-790669502.us-east-2.elb.amazonaws.com:8000/gamestate/reset
```

## 🔒 Security Notes

- This is an educational project and should not be used with real money
- Implement appropriate access controls before deploying in a production environment
- Student data protection measures should be considered when deploying in educational settings

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Development Guidelines
- Follow PEP 8 style guide for Python code
- Write unit tests for new features
- Update documentation when adding new endpoints
- Follow REST API best practices
- Keep educational context in mind when adding features

## 🙏 Acknowledgments

- IPL for inspiration
- Educational institutions using this tool
- Contributors and maintainers

## 📞 Support

For support:
- Create an issue in the GitHub repository
- Contact the maintainers
- Check the documentation in the `/docs` folder

---

**Note:** This is an educational project. No real money or betting is involved. The purpose is purely to teach financial concepts through gamification.
