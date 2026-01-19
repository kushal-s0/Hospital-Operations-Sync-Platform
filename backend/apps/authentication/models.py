from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class Hospital(models.Model):
    hospital_id = models.IntegerField(primary_key=True)
    hospital_name = models.CharField(max_length=150, null=True)
    region = models.CharField(max_length=10, choices=[('Urban', 'Urban'), ('Rural', 'Rural')], null=True)
    facility_size_beds = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    admin_id = models.IntegerField(null=True)
    updated_timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'hospitals'
        managed = False


class Department(models.Model):
    department_id = models.IntegerField(primary_key=True)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, db_column='hospital_id', null=True)
    department_name = models.CharField(max_length=100, null=True)
    total_beds = models.IntegerField(null=True)
    available_beds = models.IntegerField(null=True)
    emergency_beds = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    admin_id = models.IntegerField(null=True)
    updated_timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'departments'
        managed = False


class StaffUser(models.Model):
    """Custom user model that maps to MySQL staff_users table."""
    
    ROLE_CHOICES = [
        ('Doctor', 'Doctor'),
        ('Nurse', 'Nurse'),
        ('Admin', 'Admin'),
        ('Receptionist', 'Receptionist'),
        ('Pharmacist', 'Pharmacist'),
    ]

    staff_id = models.IntegerField(primary_key=True)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, db_column='hospital_id', null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, db_column='department_id', null=True)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, null=True)
    phone_number = models.CharField(max_length=20, null=True)
    email = models.CharField(max_length=120, unique=True, null=True)
    password_hash = models.CharField(max_length=255, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True)
    admin_id = models.IntegerField(null=True)
    updated_timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'staff_users'
        managed = False

    def set_password(self, raw_password):
        """Hash and set the password"""
        self.password_hash = make_password(raw_password)
        
    def check_password(self, raw_password):
        """Check if the provided password matches the stored hash"""
        return check_password(raw_password, self.password_hash)

    @property
    def is_authenticated(self):
        """Always return True for authenticated users (required by DRF)."""
        return True
    
    @property
    def is_anonymous(self):
        """Always return False (required by DRF)."""
        return False

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def __str__(self):
        return f"{self.full_name} ({self.role})"


class Doctor(models.Model):
    """Model representing a doctor (extends StaffUser)."""
    doctor_id = models.IntegerField(primary_key=True)
    specialization = models.CharField(max_length=100, null=True)
    years_experience = models.IntegerField(null=True)
    admin_id = models.IntegerField(null=True)
    updated_timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'doctors'
        managed = False

    def __str__(self):
        return f"Doctor {self.doctor_id}"


class Patient(models.Model):
    """Model representing a patient (mapped to MySQL patients table)."""
    patient_id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    gender = models.CharField(max_length=1, null=True)
    date_of_birth = models.DateField(null=True)
    contact_number = models.CharField(max_length=20, null=True)
    address = models.TextField(null=True)
    registration_date = models.DateField(null=True)
    insurance_provider = models.CharField(max_length=100, null=True)
    insurance_number = models.CharField(max_length=50, null=True)
    email = models.CharField(max_length=120, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    admin_id = models.IntegerField(null=True)
    updated_timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'patients'
        managed = False

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def __str__(self):
        return self.full_name


class Bed(models.Model):
    """Model representing a hospital bed (mapped to MySQL beds table)."""
    BED_TYPE_CHOICES = [
        ('Normal', 'Normal'),
        ('ICU', 'ICU'),
        ('Ventilator', 'Ventilator'),
        ('Emergency', 'Emergency'),
    ]
    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('Occupied', 'Occupied'),
        ('Maintenance', 'Maintenance'),
    ]

    bed_id = models.IntegerField(primary_key=True)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, db_column='hospital_id', null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, db_column='department_id', null=True)
    bed_type = models.CharField(max_length=20, choices=BED_TYPE_CHOICES, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    admin_id = models.IntegerField(null=True)
    updated_timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'beds'
        managed = False

    def __str__(self):
        return f"Bed {self.bed_id}"


class Admission(models.Model):
    """Model representing a patient admission (mapped to MySQL admissions table)."""
    CONDITION_CHOICES = [
        ('Critical', 'Critical'),
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
    ]
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Discharged', 'Discharged'),
    ]

    admission_id = models.IntegerField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, db_column='patient_id', null=True)
    bed = models.ForeignKey(Bed, on_delete=models.CASCADE, db_column='bed_id', null=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, db_column='doctor_id', null=True)
    admission_time = models.DateTimeField(null=True)
    discharge_time = models.DateTimeField(null=True)
    condition_level = models.CharField(max_length=20, choices=CONDITION_CHOICES, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    admin_id = models.IntegerField(null=True)
    updated_timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'admissions'
        managed = False

    def __str__(self):
        return f"Admission {self.admission_id}"


class Visit(models.Model):
    """Model representing a patient visit (mapped to MySQL visits table)."""
    URGENCY_CHOICES = [
        ('Critical', 'Critical'),
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
    ]
    OUTCOME_CHOICES = [
        ('Admitted', 'Admitted'),
        ('Discharged', 'Discharged'),
        ('Left Without Being Seen', 'Left Without Being Seen'),
    ]

    visit_id = models.IntegerField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, db_column='patient_id', null=True)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, db_column='hospital_id', null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, db_column='department_id', null=True)
    visit_datetime = models.DateTimeField(null=True)
    day_of_week = models.CharField(max_length=20, null=True)
    season = models.CharField(max_length=20, null=True)
    time_of_day = models.CharField(max_length=20, null=True)
    urgency_level = models.CharField(max_length=20, choices=URGENCY_CHOICES, null=True)
    nurse_patient_ratio = models.DecimalField(max_digits=4, decimal_places=2, null=True)
    specialist_availability = models.IntegerField(null=True)
    time_to_registration_min = models.IntegerField(null=True)
    time_to_triage_min = models.IntegerField(null=True)
    time_to_medical_professional_min = models.IntegerField(null=True)
    total_wait_time_min = models.IntegerField(null=True)
    patient_outcome = models.CharField(max_length=30, choices=OUTCOME_CHOICES, null=True)
    patient_satisfaction = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    admin_id = models.IntegerField(null=True)
    updated_timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'visits'
        managed = False

    def __str__(self):
        return f"Visit {self.visit_id}"


class Appointment(models.Model):
    """Model representing an appointment (mapped to MySQL appointments table)."""
    STATUS_CHOICES = [
        ('Scheduled', 'Scheduled'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    appointment_id = models.IntegerField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, db_column='patient_id', null=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, db_column='doctor_id', null=True)
    visit = models.ForeignKey(Visit, on_delete=models.CASCADE, db_column='visit_id', null=True)
    appointment_date = models.DateField(null=True)
    appointment_time = models.TimeField(null=True)
    reason_for_visit = models.CharField(max_length=200, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    admin_id = models.IntegerField(null=True)
    updated_timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'appointments'
        managed = False

    def __str__(self):
        return f"Appointment {self.appointment_id}"


class Treatment(models.Model):
    """Model representing a treatment (mapped to MySQL treatments table)."""
    treatment_id = models.IntegerField(primary_key=True)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, db_column='appointment_id', null=True)
    treatment_type = models.CharField(max_length=100, null=True)
    description = models.TextField(null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    treatment_date = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    admin_id = models.IntegerField(null=True)
    updated_timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'treatments'
        managed = False

    def __str__(self):
        return f"Treatment {self.treatment_id}"


class Billing(models.Model):
    """Model representing billing (mapped to MySQL billing table)."""
    PAYMENT_METHOD_CHOICES = [
        ('Cash', 'Cash'),
        ('Card', 'Card'),
        ('Insurance', 'Insurance'),
    ]
    PAYMENT_STATUS_CHOICES = [
        ('Paid', 'Paid'),
        ('Pending', 'Pending'),
        ('Failed', 'Failed'),
    ]

    bill_id = models.IntegerField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, db_column='patient_id', null=True)
    treatment = models.ForeignKey(Treatment, on_delete=models.CASCADE, db_column='treatment_id', null=True)
    bill_date = models.DateField(null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, null=True)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    admin_id = models.IntegerField(null=True)
    updated_timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'billing'
        managed = False

    def __str__(self):
        return f"Bill {self.bill_id}"


class InventoryItem(models.Model):
    """Model representing inventory items (mapped to MySQL inventory_items table)."""
    CATEGORY_CHOICES = [
        ('Medicine', 'Medicine'),
        ('Consumable', 'Consumable'),
        ('Equipment', 'Equipment'),
    ]

    item_id = models.IntegerField(primary_key=True)
    item_name = models.CharField(max_length=150, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, null=True)
    quantity_available = models.IntegerField(null=True)
    reorder_level = models.IntegerField(null=True)
    supplier = models.CharField(max_length=150, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    admin_id = models.IntegerField(null=True)
    updated_timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'inventory_items'
        managed = False

    @property
    def is_low_stock(self):
        if self.quantity_available and self.reorder_level:
            return self.quantity_available <= self.reorder_level
        return False

    def __str__(self):
        return f"{self.item_name}"


class InventoryUsage(models.Model):
    """Model representing inventory usage (mapped to MySQL inventory_usage table)."""
    usage_id = models.IntegerField(primary_key=True)
    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, db_column='item_id', null=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, db_column='patient_id', null=True)
    quantity_used = models.IntegerField(null=True)
    usage_date = models.DateTimeField(null=True)
    department = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    admin_id = models.IntegerField(null=True)
    updated_timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'inventory_usage'
        managed = False

    def __str__(self):
        return f"Usage {self.usage_id}"


class FinancialTransaction(models.Model):
    """Model representing financial transactions (mapped to MySQL financial_transactions table)."""
    REFERENCE_TYPE_CHOICES = [
        ('Billing', 'Billing'),
        ('Inventory', 'Inventory'),
        ('Salary', 'Salary'),
        ('Maintenance', 'Maintenance'),
        ('Other', 'Other'),
    ]
    TRANSACTION_TYPE_CHOICES = [
        ('INCOME', 'Income'),
        ('EXPENSE', 'Expense'),
    ]
    PAYMENT_METHOD_CHOICES = [
        ('Cash', 'Cash'),
        ('Card', 'Card'),
        ('Insurance', 'Insurance'),
        ('UPI', 'UPI'),
        ('Bank', 'Bank'),
    ]

    transaction_id = models.IntegerField(primary_key=True)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, db_column='hospital_id', null=True)
    reference_type = models.CharField(max_length=20, choices=REFERENCE_TYPE_CHOICES, null=True)
    reference_id = models.IntegerField(null=True)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, null=True)
    description = models.TextField(null=True)
    transaction_date = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    admin_id = models.IntegerField(null=True)
    updated_timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'financial_transactions'
        managed = False

    def __str__(self):
        return f"Transaction {self.transaction_id}"


class AuditLog(models.Model):
    """Model representing audit log (mapped to MySQL audit_log table)."""
    OPERATION_CHOICES = [
        ('INSERT', 'Insert'),
        ('UPDATE', 'Update'),
        ('DELETE', 'Delete'),
    ]

    audit_id = models.AutoField(primary_key=True)
    table_name = models.CharField(max_length=100)
    record_id = models.IntegerField()
    operation_type = models.CharField(max_length=10, choices=OPERATION_CHOICES)
    admin_id = models.IntegerField(null=True)
    admin_name = models.CharField(max_length=200, null=True)
    admin_role = models.CharField(max_length=50, null=True)
    old_values = models.JSONField(null=True)
    new_values = models.JSONField(null=True)
    changed_fields = models.TextField(null=True)
    ip_address = models.CharField(max_length=45, null=True)
    user_agent = models.CharField(max_length=255, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'audit_log'
        managed = False

    def __str__(self):
        return f"Audit {self.audit_id}: {self.operation_type} on {self.table_name}"
