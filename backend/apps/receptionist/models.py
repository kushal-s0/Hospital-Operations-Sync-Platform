"""
Receptionist models - Uses existing database tables without creating new models
The receptionist views will read from: billing, financial_transactions, treatments, patients
"""
from django.db import models


class ReceptionistDashboardView(models.Model):
    """
    View-only model for receptionist dashboard.
    Doesn't store data, just provides a marker for the app.
    """
    class Meta:
        managed = False
        db_table = 'receptionist_dashboard_view'
