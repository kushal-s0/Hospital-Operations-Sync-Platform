import razorpay
import hmac
import hashlib
from decimal import Decimal
from django.conf import settings
from django.db import connection, transaction
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import PaymentTransaction
from .serializers import (
    PaymentTransactionSerializer,
    CreateOrderSerializer,
    VerifyPaymentSerializer
)


class PaymentViewSet(viewsets.ViewSet):
    """ViewSet for handling Razorpay payment operations"""
    
    permission_classes = [IsAuthenticated]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Initialize Razorpay client
        self.razorpay_client = razorpay.Client(
            auth=(settings.RAZORPAY_PUBLIC_KEY, settings.RAZORPAY_SECRET_KEY)
        )
    
    @action(detail=False, methods=['post'])
    def create_order(self, request):
        """Create a Razorpay order for a pending bill"""
        serializer = CreateOrderSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response({
                'status': 'error',
                'message': 'Invalid data',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        bill_id = serializer.validated_data['bill_id']
        
        try:
            # Get bill details from database
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT bill_id, amount, payment_status, patient_id
                    FROM billing
                    WHERE bill_id = %s
                """, [bill_id])
                
                bill = cursor.fetchone()
                
                if not bill:
                    return Response({
                        'status': 'error',
                        'message': 'Bill not found'
                    }, status=status.HTTP_404_NOT_FOUND)
                
                bill_id, amount, payment_status, patient_id = bill
                
                # Check if bill is already paid
                if payment_status and payment_status.lower() == 'paid':
                    return Response({
                        'status': 'error',
                        'message': 'Bill is already paid'
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                # Convert amount to paise (Razorpay uses smallest currency unit)
                amount_in_paise = int(float(amount) * 100)
                
                # Create Razorpay order
                razorpay_order = self.razorpay_client.order.create({
                    'amount': amount_in_paise,
                    'currency': 'INR',
                    'receipt': f'bill_{bill_id}',
                    'notes': {
                        'bill_id': str(bill_id),
                        'patient_id': str(patient_id)
                    }
                })
                
                # Save transaction to database
                payment_transaction = PaymentTransaction.objects.create(
                    bill_id=bill_id,
                    razorpay_order_id=razorpay_order['id'],
                    amount=amount,
                    currency='INR',
                    status='created'
                )
                
                return Response({
                    'status': 'success',
                    'data': {
                        'order_id': razorpay_order['id'],
                        'amount': amount_in_paise,
                        'currency': 'INR',
                        'bill_id': bill_id,
                        'key': settings.RAZORPAY_PUBLIC_KEY
                    }
                }, status=status.HTTP_201_CREATED)
                
        except Exception as e:
            return Response({
                'status': 'error',
                'message': f'Failed to create order: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['post'])
    def verify_payment(self, request):
        """Verify Razorpay payment signature and update billing status"""
        serializer = VerifyPaymentSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response({
                'status': 'error',
                'message': 'Invalid data',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        razorpay_order_id = serializer.validated_data['razorpay_order_id']
        razorpay_payment_id = serializer.validated_data['razorpay_payment_id']
        razorpay_signature = serializer.validated_data['razorpay_signature']
        
        try:
            # Verify signature
            generated_signature = hmac.new(
                settings.RAZORPAY_SECRET_KEY.encode(),
                f"{razorpay_order_id}|{razorpay_payment_id}".encode(),
                hashlib.sha256
            ).hexdigest()
            
            if generated_signature != razorpay_signature:
                return Response({
                    'status': 'error',
                    'message': 'Invalid payment signature'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Get payment transaction
            try:
                payment_transaction = PaymentTransaction.objects.get(
                    razorpay_order_id=razorpay_order_id
                )
            except PaymentTransaction.DoesNotExist:
                return Response({
                    'status': 'error',
                    'message': 'Payment transaction not found'
                }, status=status.HTTP_404_NOT_FOUND)
            
            # Fetch payment details from Razorpay
            payment_details = self.razorpay_client.payment.fetch(razorpay_payment_id)
            
            # Start database transaction
            with transaction.atomic():
                # Update payment transaction
                payment_transaction.razorpay_payment_id = razorpay_payment_id
                payment_transaction.razorpay_signature = razorpay_signature
                payment_transaction.status = 'captured'
                payment_transaction.payment_method = payment_details.get('method', 'card')
                payment_transaction.save()
                
                # Update billing status to Paid
                with connection.cursor() as cursor:
                    cursor.execute("""
                        UPDATE billing
                        SET payment_status = 'Paid',
                            payment_method = %s,
                            updated_at = NOW()
                        WHERE bill_id = %s
                    """, [payment_details.get('method', 'Card').title(), payment_transaction.bill_id])
                
                return Response({
                    'status': 'success',
                    'message': 'Payment verified successfully',
                    'data': {
                        'bill_id': payment_transaction.bill_id,
                        'payment_id': razorpay_payment_id,
                        'status': 'paid'
                    }
                }, status=status.HTTP_200_OK)
                
        except Exception as e:
            # Update payment transaction as failed
            try:
                payment_transaction = PaymentTransaction.objects.get(
                    razorpay_order_id=razorpay_order_id
                )
                payment_transaction.status = 'failed'
                payment_transaction.error_description = str(e)
                payment_transaction.save()
            except:
                pass
            
            return Response({
                'status': 'error',
                'message': f'Payment verification failed: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['post'])
    def handle_webhook(self, request):
        """Handle Razorpay webhook events"""
        # Get webhook signature from headers
        webhook_signature = request.META.get('HTTP_X_RAZORPAY_SIGNATURE')
        webhook_secret = settings.RAZORPAY_WEBHOOK_SECRET if hasattr(settings, 'RAZORPAY_WEBHOOK_SECRET') else ''
        
        try:
            # Verify webhook signature
            self.razorpay_client.utility.verify_webhook_signature(
                request.body.decode('utf-8'),
                webhook_signature,
                webhook_secret
            )
            
            # Process webhook event
            event = request.data.get('event')
            payload = request.data.get('payload', {})
            payment_entity = payload.get('payment', {}).get('entity', {})
            
            if event == 'payment.captured':
                # Payment captured successfully
                order_id = payment_entity.get('order_id')
                payment_id = payment_entity.get('id')
                
                try:
                    payment_transaction = PaymentTransaction.objects.get(
                        razorpay_order_id=order_id
                    )
                    payment_transaction.razorpay_payment_id = payment_id
                    payment_transaction.status = 'captured'
                    payment_transaction.save()
                except PaymentTransaction.DoesNotExist:
                    pass
            
            elif event == 'payment.failed':
                # Payment failed
                order_id = payment_entity.get('order_id')
                error_code = payment_entity.get('error_code')
                error_description = payment_entity.get('error_description')
                
                try:
                    payment_transaction = PaymentTransaction.objects.get(
                        razorpay_order_id=order_id
                    )
                    payment_transaction.status = 'failed'
                    payment_transaction.error_code = error_code
                    payment_transaction.error_description = error_description
                    payment_transaction.save()
                except PaymentTransaction.DoesNotExist:
                    pass
            
            return Response({'status': 'success'}, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def transaction_history(self, request):
        """Get payment transaction history"""
        bill_id = request.query_params.get('bill_id')
        
        try:
            if bill_id:
                transactions = PaymentTransaction.objects.filter(bill_id=bill_id)
            else:
                transactions = PaymentTransaction.objects.all()[:50]
            
            serializer = PaymentTransactionSerializer(transactions, many=True)
            
            return Response({
                'status': 'success',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
