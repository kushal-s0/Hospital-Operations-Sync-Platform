# Database Schema

## Patient Management

### Patient
| Field | Type | Description |
|-------|------|-------------|
| id | AutoField | Primary key |
| first_name | CharField(100) | Patient first name |
| last_name | CharField(100) | Patient last name |
| date_of_birth | DateField | Date of birth |
| gender | CharField(1) | M/F/O |
| phone_number | CharField(15) | Contact number |
| email | EmailField | Email address |
| address | TextField | Residential address |
| emergency_contact_name | CharField(200) | Emergency contact |
| emergency_contact_phone | CharField(15) | Emergency phone |
| medical_history | TextField | Medical history notes |
| created_at | DateTimeField | Record creation time |
| updated_at | DateTimeField | Last update time |

## Bed Management

### Department
| Field | Type | Description |
|-------|------|-------------|
| id | AutoField | Primary key |
| name | CharField(100) | Department name |
| description | TextField | Description |
| floor | IntegerField | Floor number |
| created_at | DateTimeField | Record creation time |

### Bed
| Field | Type | Description |
|-------|------|-------------|
| id | AutoField | Primary key |
| bed_number | CharField(20) | Unique bed identifier |
| department | ForeignKey | Link to Department |
| bed_type | CharField(20) | general/icu/private/etc |
| status | CharField(20) | available/occupied/maintenance/reserved |
| floor | IntegerField | Floor number |
| room_number | CharField(20) | Room identifier |
| created_at | DateTimeField | Record creation time |
| updated_at | DateTimeField | Last update time |

## OPD Management

### OPDQueue
| Field | Type | Description |
|-------|------|-------------|
| id | AutoField | Primary key |
| patient | ForeignKey | Link to Patient |
| token_number | IntegerField | Queue token |
| department | CharField(100) | Department name |
| doctor_name | CharField(200) | Treating doctor |
| status | CharField(20) | waiting/in_consultation/completed/cancelled |
| priority | CharField(20) | normal/urgent/emergency |
| check_in_time | DateTimeField | Patient check-in time |
| consultation_start_time | DateTimeField | Consultation start |
| consultation_end_time | DateTimeField | Consultation end |
| estimated_wait_time | IntegerField | Estimated wait in minutes |
| notes | TextField | Additional notes |

### OPDStatistics
| Field | Type | Description |
|-------|------|-------------|
| id | AutoField | Primary key |
| date | DateField | Statistics date |
| department | CharField(100) | Department |
| total_patients | IntegerField | Total patients |
| average_wait_time | FloatField | Avg wait time |
| average_consultation_time | FloatField | Avg consultation time |
| peak_hour | IntegerField | Peak hour (0-23) |

## Admission Management

### Admission
| Field | Type | Description |
|-------|------|-------------|
| id | AutoField | Primary key |
| patient | ForeignKey | Link to Patient |
| bed | ForeignKey | Link to Bed |
| admission_type | CharField(20) | emergency/planned/transfer |
| status | CharField(20) | admitted/discharged/transferred |
| admission_date | DateTimeField | Admission timestamp |
| discharge_date | DateTimeField | Discharge timestamp |
| diagnosis | TextField | Diagnosis details |
| treating_doctor | CharField(200) | Doctor name |
| notes | TextField | Additional notes |

### AdmissionRule
| Field | Type | Description |
|-------|------|-------------|
| id | AutoField | Primary key |
| name | CharField(200) | Rule name |
| description | TextField | Rule description |
| condition | TextField | JSON condition |
| recommended_bed_type | CharField(50) | Suggested bed type |
| recommended_department | CharField(100) | Suggested department |
| priority | IntegerField | Rule priority |
| is_active | BooleanField | Active status |

## Inventory Management

### InventoryCategory
| Field | Type | Description |
|-------|------|-------------|
| id | AutoField | Primary key |
| name | CharField(100) | Category name |
| description | TextField | Description |

### InventoryItem
| Field | Type | Description |
|-------|------|-------------|
| id | AutoField | Primary key |
| name | CharField(200) | Item name |
| category | ForeignKey | Link to Category |
| item_type | CharField(20) | medicine/consumable/equipment/surgical |
| sku | CharField(50) | Stock keeping unit |
| unit | CharField(50) | Unit of measurement |
| current_stock | IntegerField | Current quantity |
| minimum_stock | IntegerField | Low stock threshold |
| maximum_stock | IntegerField | Maximum capacity |
| unit_price | DecimalField | Price per unit |
| expiry_date | DateField | Expiry date |
| supplier | CharField(200) | Supplier name |
| location | CharField(100) | Storage location |

### InventoryTransaction
| Field | Type | Description |
|-------|------|-------------|
| id | AutoField | Primary key |
| item | ForeignKey | Link to Item |
| transaction_type | CharField(20) | in/out/adjustment |
| quantity | IntegerField | Quantity changed |
| reference | CharField(100) | Reference number |
| notes | TextField | Transaction notes |
| performed_by | CharField(200) | Staff member |
| created_at | DateTimeField | Transaction time |

## Inter-Hospital

### Hospital
| Field | Type | Description |
|-------|------|-------------|
| id | AutoField | Primary key |
| name | CharField(200) | Hospital name |
| code | CharField(20) | Unique code |
| address | TextField | Address |
| city | CharField(100) | City |
| phone | CharField(20) | Contact number |
| email | EmailField | Email |
| api_endpoint | URLField | API endpoint |
| is_active | BooleanField | Active status |

### CapacitySnapshot
| Field | Type | Description |
|-------|------|-------------|
| id | AutoField | Primary key |
| hospital | ForeignKey | Link to Hospital |
| total_beds | IntegerField | Total beds |
| available_beds | IntegerField | Available beds |
| icu_beds_total | IntegerField | Total ICU beds |
| icu_beds_available | IntegerField | Available ICU beds |
| emergency_load | IntegerField | Emergency patients |
| opd_load | IntegerField | OPD queue length |
| timestamp | DateTimeField | Snapshot time |
