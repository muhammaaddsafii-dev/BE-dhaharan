"""               
API Views for S3 file upload
"""
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import uuid
from datetime import datetime
import traceback

try:
    import boto3
    from botocore.exceptions import ClientError
    BOTO3_AVAILABLE = True
except ImportError:
    BOTO3_AVAILABLE = False


@api_view(['POST'])
def upload_to_s3(request):
    """
    Upload file to S3 bucket
    Expects: multipart/form-data with 'file' field
    Returns: URL of uploaded file
    """
    # Check if boto3 is available
    if not BOTO3_AVAILABLE:
        return Response(
            {'error': 'boto3 library not installed. Please run: pip install boto3'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    # Check if AWS credentials are configured
    if not settings.AWS_ACCESS_KEY_ID or not settings.AWS_SECRET_ACCESS_KEY:
        return Response(
            {'error': 'AWS credentials not configured. Please set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY in .env'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    if 'file' not in request.FILES:
        return Response(
            {'error': 'No file provided'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    file = request.FILES['file']
    
    # Validate file type
    allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp']
    if file.content_type not in allowed_types:
        return Response(
            {'error': 'Invalid file type. Only JPEG, PNG, and WEBP allowed.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Validate file size (5MB max)
    max_size = 5 * 1024 * 1024  # 5MB
    if file.size > max_size:
        return Response(
            {'error': 'File too large. Maximum size is 5MB.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        # Generate unique filename
        ext = file.name.split('.')[-1]
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_id = str(uuid.uuid4())[:8]
        filename = f"kegiatan/{timestamp}_{unique_id}.{ext}"
        
        # S3 configuration
        bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        prefix = settings.AWS_S3_PREFIX
        s3_key = f"{prefix}/{filename}"
        
        # Upload to S3
        s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME
        )
        
        s3_client.upload_fileobj(
            file,
            bucket_name,
            s3_key,
            ExtraArgs={
                'ContentType': file.content_type,
                # Removed ACL - bucket uses Bucket Owner Enforced
            }
        )
        
        # Generate URL - gunakan format S3 yang benar
        file_url = f"https://s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com/{bucket_name}/{s3_key}"
        
        return Response({
            'url': file_url,
            'filename': file.name,
            'size': file.size,
            'content_type': file.content_type
        }, status=status.HTTP_201_CREATED)
        
    except ClientError as e:
        error_code = e.response.get('Error', {}).get('Code', 'Unknown')
        error_message = e.response.get('Error', {}).get('Message', str(e))
        
        print(f"S3 ClientError: {error_code} - {error_message}")
        print(f"Full traceback: {traceback.format_exc()}")
        
        return Response(
            {
                'error': f'S3 upload failed: {error_code}',
                'details': error_message,
                'help': 'Please check your AWS credentials and bucket permissions'
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    except Exception as e:
        print(f"Upload error: {str(e)}")
        print(f"Full traceback: {traceback.format_exc()}")
        
        return Response(
            {
                'error': f'Upload failed: {str(e)}',
                'error_type': type(e).__name__,
                'help': 'Please check server logs for more details'
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
