# Weather API Project

This is a Django REST framework project that provides weather information through an API.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
- Windows:
```bash
venv\Scripts\activate
```
- Unix/MacOS:
```bash
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Start the development server:
```bash
python manage.py runserver
```

## API Endpoints

- `GET /api/weather/` - Get weather information
- `POST /api/weather/` - Create weather record
- `GET /api/weather/{id}/` - Get specific weather record
- `PUT /api/weather/{id}/` - Update weather record
- `DELETE /api/weather/{id}/` - Delete weather record 