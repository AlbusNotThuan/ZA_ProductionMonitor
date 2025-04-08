# Production Monitor

A web-based production monitoring system with barcode scanner integration.

## Features
- Real-time production monitoring
- Barcode scanner integration
- Automatic daily reset at 8 PM
- Admin panel for configuration
- Production target tracking

## Installation
1. Clone the repository
```bash
git clone [your-repository-url]
```

2. Install requirements
```bash
pip install -r requirements.txt
```

3. Run the application
```bash
python main.py
```

## Configuration
- Default target: 200 units
- Reset time: 8:00 PM daily
- Web interface: http://localhost:5000

## Files
- `main.py`: Main process controller
- `webapp.py`: Web server
- `test2.py`: Barcode scanner handler
- `reset_json.py`: Auto-reset scheduler
