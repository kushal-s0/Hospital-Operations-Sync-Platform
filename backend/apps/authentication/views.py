from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from django.db.models import Q
from .models import StaffUser, Department


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    Login endpoint that returns JWT tokens
    Supports login with email, phone number, or staff ID
    """
    identifier = request.data.get('username')  # Can be email, phone, or ID
    password = request.data.get('password')
    
    if not identifier or not password:
        return Response(
            {'error': 'Please provide both username and password'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Try to find user by email, phone_number, or staff_id
    try:
        # Check if identifier is a number (could be staff_id or phone)
        if identifier.isdigit():
            user = StaffUser.objects.filter(
                Q(phone_number=identifier) | Q(staff_id=identifier)
            ).first()
        else:
            # Assume it's an email
            user = StaffUser.objects.filter(email=identifier).first()
        
        if user is None:
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Check if user is active
        if not user.is_active:
            return Response(
                {'error': 'This account has been disabled'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Check if password is set
        if not user.password_hash:
            return Response(
                {'error': 'Account not activated. Please contact administrator to set password.'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Verify password
        if not user.check_password(password):
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Update last login
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])
        
        # Generate JWT tokens
        # We'll use staff_id as the user identifier for JWT
        refresh = RefreshToken()
        refresh['staff_id'] = user.staff_id
        refresh['email'] = user.email
        refresh['role'] = user.role
        
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'id': user.staff_id,
                'email': user.email,
                'phone_number': user.phone_number,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'full_name': user.full_name,
                'role': user.role,
                'hospital_id': user.hospital_id,
                'department_id': user.department_id,
                'is_active': user.is_active,
            }
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': f'Login failed: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([AllowAny])  # Changed to AllowAny since we don't need authentication to logout
def logout_view(request):
    """
    Logout endpoint that blacklists the refresh token
    """
    try:
        refresh_token = request.data.get('refresh')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        return Response({'message': 'Successfully logged out'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    """
    Get current user profile from JWT token
    """
    try:
        # The user is already authenticated and available as request.user
        user = request.user
        
        return Response({
            'id': user.staff_id,
            'email': user.email,
            'phone_number': user.phone_number,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'full_name': user.full_name,
            'role': user.role,
            'hospital_id': user.hospital_id,
            'department_id': user.department_id,
            'is_active': user.is_active,
        })
    except AttributeError:
        return Response(
            {'error': 'User not found'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def token_refresh_view(request):
    """
    Refresh access token using refresh token
    """
    from rest_framework_simplejwt.views import TokenRefreshView
    return TokenRefreshView.as_view()(request._request)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def staff_list(request):
    """
    Get list of all staff users (optionally filter by role)
    """
    try:
        role = request.query_params.get('role', None)
        
        if role:
            staff = StaffUser.objects.filter(role=role, is_active=True)
        else:
            staff = StaffUser.objects.filter(is_active=True)
        
        staff_data = [{
            'staff_id': s.staff_id,
            'first_name': s.first_name,
            'last_name': s.last_name,
            'full_name': s.full_name,
            'role': s.role,
            'email': s.email,
            'phone_number': s.phone_number,
            'department_id': s.department_id,
            'hospital_id': s.hospital_id,
        } for s in staff]
        
        return Response(staff_data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {'error': f'Failed to fetch staff: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def department_list(request):
    """
    Get list of all departments
    """
    try:
        departments = Department.objects.all()
        
        dept_data = [{
            'department_id': d.department_id,
            'department_name': d.department_name,
            'hospital_id': d.hospital_id,
            'total_beds': d.total_beds,
            'available_beds': d.available_beds,
            'emergency_beds': d.emergency_beds,
        } for d in departments]
        
        return Response(dept_data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {'error': f'Failed to fetch departments: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
