"""
S3 Storage Backend for Django
Upload files to S3: s3://cdn.ruangbumi.com/dhaharan.id.ruangbumi.com/
"""
import boto3
from botocore.exceptions import ClientError
from django.conf import settings
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible
import os


@deconstructible
class S3Storage(Storage):
    """
    Custom storage backend for AWS S3
    """
    
    def __init__(self):
        self.bucket_name = getattr(settings, 'AWS_STORAGE_BUCKET_NAME', 'cdn.ruangbumi.com')
        self.prefix = getattr(settings, 'AWS_S3_PREFIX', 'dhaharan.id.ruangbumi.com')
        self.region = getattr(settings, 'AWS_S3_REGION_NAME', 'ap-southeast-1')
        
        # Initialize S3 client
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=getattr(settings, 'AWS_ACCESS_KEY_ID', None),
            aws_secret_access_key=getattr(settings, 'AWS_SECRET_ACCESS_KEY', None),
            region_name=self.region
        )
    
    def _get_s3_key(self, name):
        """Generate S3 key with prefix"""
        # Clean the name
        name = name.replace('\\', '/')
        if name.startswith('/'):
            name = name[1:]
        
        # Add prefix
        return f"{self.prefix}/{name}"
    
    def _save(self, name, content):
        """
        Save file to S3
        """
        s3_key = self._get_s3_key(name)
        
        try:
            # Upload file to S3
            self.s3_client.upload_fileobj(
                content,
                self.bucket_name,
                s3_key,
                ExtraArgs={
                    'ContentType': content.content_type if hasattr(content, 'content_type') else 'application/octet-stream'
                    # ACL removed - bucket uses Bucket Owner Enforced setting
                }
            )
            return name
        except ClientError as e:
            raise IOError(f"Error uploading to S3: {str(e)}")
    
    def exists(self, name):
        """
        Check if file exists in S3
        """
        s3_key = self._get_s3_key(name)
        
        try:
            self.s3_client.head_object(Bucket=self.bucket_name, Key=s3_key)
            return True
        except ClientError:
            return False
    
    def url(self, name):
        """
        Return the URL to access the file
        """
        s3_key = self._get_s3_key(name)
        # Return S3 URL dengan format yang benar
        return f"https://s3.{self.region}.amazonaws.com/{self.bucket_name}/{s3_key}"
    
    def delete(self, name):
        """
        Delete file from S3
        """
        s3_key = self._get_s3_key(name)
        
        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=s3_key)
        except ClientError as e:
            raise IOError(f"Error deleting from S3: {str(e)}")
    
    def size(self, name):
        """
        Return the size of the file
        """
        s3_key = self._get_s3_key(name)
        
        try:
            response = self.s3_client.head_object(Bucket=self.bucket_name, Key=s3_key)
            return response['ContentLength']
        except ClientError:
            return 0
