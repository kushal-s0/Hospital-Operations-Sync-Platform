# Frontend Integration Guide - Doctor Queue Filtering

## Quick Start

The OPD queue API now automatically filters results based on the logged-in user. Doctors will only see patients assigned to them **without ML wait time predictions** (for better performance).

## Important Notes

### ML Wait Time Predictions
- **Doctors:** Do NOT receive ML-predicted wait times (`estimated_wait_time` will be `null`)
- **Other Roles (Admin, Nurse, Receptionist):** DO receive ML-predicted wait times

This improves performance for doctors and focuses them on patient care rather than wait time analytics.

## API Endpoints

### 1. Get Queue (Auto-filtered)
```javascript
// GET /api/opd/queue/
// Returns all queue entries (filtered by doctor role)

const getQueue = async () => {
    const token = localStorage.getItem('access_token');
    
    try {
        const response = await fetch('http://localhost:8000/api/opd/queue/', {
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });
        
        if (!response.ok) throw new Error('Failed to fetch queue');
        
        const data = await response.json();
        return data; // Array of queue entries
    } catch (error) {
        console.error('Error:', error);
        throw error;
    }
};
```

### 2. Get My Queue (Doctor-Specific with Statistics)
```javascript
// GET /api/opd/queue/my_queue/
// Doctor-only endpoint with statistics

const getMyQueue = async () => {
    const token = localStorage.getItem('access_token');
    
    try {
        const response = await fetch('http://localhost:8000/api/opd/queue/my_queue/', {
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });
        
        if (!response.ok) throw new Error('Failed to fetch my queue');
        
        const data = await response.json();
        // Returns:
        // {
        //     doctor_name: "Dr. John Smith",
        //     statistics: {
        //         waiting: 2,
        //         in_consultation: 1,
        //         completed_today: 10,
        //         total_active: 3
        //     },
        //     queue: [...]
        // }
        return data;
    } catch (error) {
        console.error('Error:', error);
        throw error;
    }
};
```

### 3. Get Current Active Queue
```javascript
// GET /api/opd/queue/current_queue/
// Returns today's waiting and in-consultation patients

const getCurrentQueue = async () => {
    const token = localStorage.getItem('access_token');
    
    try {
        const response = await fetch('http://localhost:8000/api/opd/queue/current_queue/', {
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });
        
        if (!response.ok) throw new Error('Failed to fetch current queue');
        
        const data = await response.json();
        return data; // Array of active entries
    } catch (error) {
        console.error('Error:', error);
        throw error;
    }
};
```

### 4. Start Consultation
```javascript
// POST /api/opd/queue/{id}/start_consultation/

const startConsultation = async (queueId) => {
    const token = localStorage.getItem('access_token');
    
    try {
        const response = await fetch(
            `http://localhost:8000/api/opd/queue/${queueId}/start_consultation/`,
            {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            }
        );
        
        if (!response.ok) throw new Error('Failed to start consultation');
        
        const data = await response.json();
        // Returns: { status: 'consultation started' }
        return data;
    } catch (error) {
        console.error('Error:', error);
        throw error;
    }
};
```

### 5. End Consultation
```javascript
// POST /api/opd/queue/{id}/end_consultation/

const endConsultation = async (queueId) => {
    const token = localStorage.getItem('access_token');
    
    try {
        const response = await fetch(
            `http://localhost:8000/api/opd/queue/${queueId}/end_consultation/`,
            {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            }
        );
        
        if (!response.ok) throw new Error('Failed to end consultation');
        
        const data = await response.json();
        // Returns: { status: 'consultation completed' }
        return data;
    } catch (error) {
        console.error('Error:', error);
        throw error;
    }
};
```

## React Component Example

### Doctor Queue Dashboard
```jsx
import React, { useState, useEffect } from 'react';

const DoctorQueue = () => {
    const [queueData, setQueueData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetchQueueData();
    }, []);

    const fetchQueueData = async () => {
        const token = localStorage.getItem('access_token');
        
        try {
            setLoading(true);
            const response = await fetch('http://localhost:8000/api/opd/queue/my_queue/', {
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            });

            if (!response.ok) throw new Error('Failed to fetch queue');

            const data = await response.json();
            setQueueData(data);
            setError(null);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const handleStartConsultation = async (queueId) => {
        const token = localStorage.getItem('access_token');
        
        try {
            const response = await fetch(
                `http://localhost:8000/api/opd/queue/${queueId}/start_consultation/`,
                {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json'
                    }
                }
            );

            if (!response.ok) throw new Error('Failed to start consultation');

            // Refresh queue data
            await fetchQueueData();
        } catch (err) {
            console.error('Error starting consultation:', err);
            alert('Failed to start consultation');
        }
    };

    const handleEndConsultation = async (queueId) => {
        const token = localStorage.getItem('access_token');
        
        try {
            const response = await fetch(
                `http://localhost:8000/api/opd/queue/${queueId}/end_consultation/`,
                {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json'
                    }
                }
            );

            if (!response.ok) throw new Error('Failed to end consultation');

            // Refresh queue data
            await fetchQueueData();
        } catch (err) {
            console.error('Error ending consultation:', err);
            alert('Failed to end consultation');
        }
    };

    if (loading) return <div>Loading queue...</div>;
    if (error) return <div>Error: {error}</div>;
    if (!queueData) return <div>No data available</div>;

    return (
        <div className="doctor-queue">
            <h2>My Queue - {queueData.doctor_name}</h2>
            
            {/* Statistics Section */}
            <div className="queue-stats">
                <div className="stat-card">
                    <h3>Waiting</h3>
                    <p>{queueData.statistics.waiting}</p>
                </div>
                <div className="stat-card">
                    <h3>In Consultation</h3>
                    <p>{queueData.statistics.in_consultation}</p>
                </div>
                <div className="stat-card">
                    <h3>Completed Today</h3>
                    <p>{queueData.statistics.completed_today}</p>
                </div>
                <div className="stat-card">
                    <h3>Total Active</h3>
                    <p>{queueData.statistics.total_active}</p>
                </div>
            </div>

            {/* Queue List */}
            <div className="queue-list">
                <h3>Active Patients</h3>
                {queueData.queue.length === 0 ? (
                    <p>No patients in queue</p>
                ) : (
                    <table>
                        <thead>
                            <tr>
                                <th>Token</th>
                                <th>Patient</th>
                                <th>Priority</th>
                                <th>Status</th>
                                <th>Wait Time</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {queueData.queue.map((entry) => (
                                <tr key={entry.id}>
                                    <td>#{entry.token_number}</td>
                                    <td>{entry.patient_name}</td>
                                    <td>
                                        <span className={`priority-${entry.priority}`}>
                                            {entry.priority}
                                        </span>
                                    </td>
                                    <td>
                                        <span className={`status-${entry.status}`}>
                                            {entry.status}
                                        </span>
                                    </td>
                                    <td>
                                        {entry.estimated_wait_time 
                                            ? `${entry.estimated_wait_time} min` 
                                            : '-'}
                                    </td>
                                    <td>
                                        {entry.status === 'waiting' && (
                                            <button 
                                                onClick={() => handleStartConsultation(entry.id)}
                                            >
                                                Start
                                            </button>
                                        )}
                                        {entry.status === 'in_consultation' && (
                                            <button 
                                                onClick={() => handleEndConsultation(entry.id)}
                                            >
                                                Complete
                                            </button>
                                        )}
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                )}
            </div>

            <button onClick={fetchQueueData}>Refresh Queue</button>
        </div>
    );
};

export default DoctorQueue;
```

## Important Notes

### Authentication
- All endpoints require JWT authentication
- Include the access token in the `Authorization` header: `Bearer {token}`
- If token expires, refresh it or redirect to login

### Automatic Filtering
- **Doctors:** See only their assigned patients (doctor_id matches staff_id)
- **Other roles:** See all patients (no filtering)
- No need to manually filter in frontend code

### Error Handling
- **401 Unauthorized:** Token invalid or missing → redirect to login
- **403 Forbidden:** User doesn't have access (e.g., non-doctor accessing my_queue)
- **404 Not Found:** Queue entry doesn't exist or doesn't belong to the doctor

### Response Formats

#### Queue Entry Object
```javascript
{
    id: 1,
    token_number: 7,
    patient_name: "Maria Garcia",
    doctor_name: "Dr. John Smith",
    department_name: "Cardiology",
    status: "waiting",  // waiting | in_consultation | completed | cancelled
    priority: "normal",  // normal | urgent | emergency
    estimated_wait_time: 18,  // minutes (NULL for doctors, calculated for others)
    check_in_time: "2026-01-19T10:00:00Z",
    patient: {
        patient_id: 5,
        first_name: "Maria",
        last_name: "Garcia",
        // ... other patient fields
    }
}
```

**Note:** When a doctor is logged in, `estimated_wait_time` will be `null` or `undefined`. Your UI should handle this gracefully:

```jsx
// Handle missing wait time for doctors
<td>
    {entry.estimated_wait_time 
        ? `${entry.estimated_wait_time} min` 
        : '-'}  // Show dash for doctors
</td>
```

## Testing

Before deploying to production, test with different doctor accounts:

```javascript
// Test 1: Login as Doctor A, verify only their patients appear
// Test 2: Login as Doctor B, verify different set of patients
// Test 3: Login as Admin/Nurse, verify all patients appear
// Test 4: Test start/end consultation functionality
// Test 5: Verify wait time calculations update correctly
```

## Environment Configuration

Update your API base URL based on environment:

```javascript
// config.js
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const API_ENDPOINTS = {
    OPD_QUEUE: `${API_BASE_URL}/api/opd/queue/`,
    MY_QUEUE: `${API_BASE_URL}/api/opd/queue/my_queue/`,
    CURRENT_QUEUE: `${API_BASE_URL}/api/opd/queue/current_queue/`,
    START_CONSULTATION: (id) => `${API_BASE_URL}/api/opd/queue/${id}/start_consultation/`,
    END_CONSULTATION: (id) => `${API_BASE_URL}/api/opd/queue/${id}/end_consultation/`,
};
```

## Support

For backend issues or questions, contact the backend team or refer to:
- `docs/OPD_DOCTOR_FILTERING.md` - Full implementation details
- `backend/test_doctor_api_filter.py` - API test examples
