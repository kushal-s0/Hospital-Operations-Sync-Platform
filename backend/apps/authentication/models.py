from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class Hospital(models.Model):
    hospital_id = models.IntegerField(primary_key=True)
    hospital_name = models.CharField(max_length=150, null=True)
    region = models.CharField(max_length=10, choices=[('Urban', 'Urban'), ('Rural', 'Rural')], null=True)
    facility_size_beds = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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

    class Meta:
        db_table = 'departments'
        managed = False


class StaffUser(models.Model):
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
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def __str__(self):
        return f"{self.full_name} ({self.role})"
