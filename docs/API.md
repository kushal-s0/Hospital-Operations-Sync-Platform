# Hospital Operations Platform - API Documentation

## Base URL
```
http://localhost:8000/api/
```

## Endpoints

### Patients API
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/patients/` | List all patients |
| POST | `/patients/` | Create new patient |
| GET | `/patients/{id}/` | Get patient details |
| PUT | `/patients/{id}/` | Update patient |
| DELETE | `/patients/{id}/` | Delete patient |

### OPD Queue API
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/opd/queue/` | List all queue entries |
| POST | `/opd/queue/` | Add patient to queue |
| GET | `/opd/queue/current_queue/` | Get today's active queue |
| POST | `/opd/queue/{id}/start_consultation/` | Start consultation |
| POST | `/opd/queue/{id}/end_consultation/` | End consultation |
| GET | `/opd/statistics/` | Get OPD statistics |

### Beds API
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/beds/` | List all beds |
| GET | `/beds/available/` | Get available beds |
| GET | `/beds/occupancy_summary/` | Get occupancy by department |
| GET | `/beds/departments/` | List all departments |
| PUT | `/beds/{id}/` | Update bed status |

### Admissions API
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/admissions/` | List all admissions |
| POST | `/admissions/` | Create new admission |
| GET | `/admissions/current/` | Get current admissions |
| POST | `/admissions/{id}/discharge/` | Discharge patient |
| POST | `/admissions/match_bed/` | Match patient to bed |
| GET | `/admissions/rules/` | List admission rules |

### Inventory API
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/inventory/items/` | List all items |
| GET | `/inventory/items/low_stock/` | Get low stock items |
| GET | `/inventory/items/expiring_soon/` | Get expiring items |
| GET | `/inventory/categories/` | List categories |
| POST | `/inventory/transactions/` | Record transaction |

### Dashboard API
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/dashboard/summary/` | Get dashboard metrics |
| GET | `/dashboard/departments/` | Get department summary |

### Inter-Hospital API
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/interhospital/hospitals/` | List connected hospitals |
| GET | `/interhospital/capacity/latest/` | Get latest capacity |
| GET | `/interhospital/city-dashboard/` | City-wide capacity data |

## Response Format

All responses follow this format:
```json
{
  "count": 10,
  "next": "http://localhost:8000/api/patients/?page=2",
  "previous": null,
  "results": [...]
}
```

## Error Responses

```json
{
  "error": "Error message",
  "detail": "Detailed error description"
}
```

## Status Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request |
| 404 | Not Found |
| 500 | Server Error |
