# Superheroes Code Challenge

A Flask API for tracking heroes and their superpowers.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Initialize and seed the database:
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
python seed.py
```

3. Run the application:
```bash
python app.py
```

## API Endpoints

### Heroes
- `GET /heroes` - Get all heroes
- `GET /heroes/:id` - Get a specific hero with their powers

### Powers
- `GET /powers` - Get all powers
- `GET /powers/:id` - Get a specific power
- `PATCH /powers/:id` - Update a power's description

### Hero Powers
- `POST /hero_powers` - Create a new hero-power relationship

## Models

- **Hero**: Has many powers through HeroPower
- **Power**: Has many heroes through HeroPower (description must be 20+ characters)
- **HeroPower**: Belongs to Hero and Power (strength must be 'Strong', 'Weak', or 'Average')