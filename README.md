# Hospital Operations Sync Platform

## Software Syncing Hospital Operations for a Healthier City

An intelligent hospital operations platform that improves patient flow and resource utilization using real-time operational data.

## Features

- **Dynamic OPD Queue Management**: Real-time patient check-in data and historical averages to prioritize OPD queues
- **Live Bed Availability Dashboard**: Current bed occupancy by department with admission/discharge updates
- **Rule-Based Admission Workflow**: Guided intake process matching patient requirements to available beds
- **Inter-Hospital Capacity Sharing**: APIs for sharing anonymized bed availability with city health dashboard
- **Inventory Usage Tracking**: Medicine and consumable usage monitoring with low-stock alerts
- **Operational Command View**: Real-time dashboard with key metrics for administrative action

## Tech Stack

- **Frontend**: React.js
- **Backend**: Django REST Framework
- **Database**: MySQL (to be configured)

## Project Structure

```
rubix/
├── frontend/          # React application
├── backend/           # Django application
└── docs/              # Documentation
```

## Getting Started

### Backend Setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Frontend Setup
```bash
cd frontend
npm install
npm start
```

## License

MIT License
