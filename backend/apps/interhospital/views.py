from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.authentication.models import Hospital, Bed, Department


class CityDashboardAPIView(APIView):
    """
    Public API for city health dashboard.
    Returns anonymized bed availability data from actual hospitals table.
    """
    
    def get(self, request):
        """Get anonymized capacity data for all hospitals."""
        try:
            hospitals = Hospital.objects.all()
            data = []
            
            for hospital in hospitals:
                # Get bed stats for this hospital
                hospital_beds = Bed.objects.filter(hospital=hospital)
                total_beds = hospital_beds.count()
                available_beds = hospital_beds.filter(status='Available').count()
                
                # Count ICU beds (assuming ICU department or bed_type)
                icu_beds = hospital_beds.filter(bed_type='ICU')
                icu_available = icu_beds.filter(status='Available').count()
                
                occupied = total_beds - available_beds
                occupancy_rate = round((occupied / total_beds * 100), 2) if total_beds > 0 else 0
                
                data.append({
                    'hospital_code': f'HOSP-{hospital.hospital_id:03d}',
                    'hospital_name': hospital.hospital_name,
                    'city': hospital.region or 'Unknown',
                    'available_beds': available_beds,
                    'icu_beds_available': icu_available,
                    'occupancy_rate': occupancy_rate,
                    'last_updated': hospital.updated_at
                })
            
            return Response(data)
        except Exception as e:
            # Return empty data on error
            return Response([])
