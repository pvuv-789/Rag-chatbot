"""
S3 Storage Module
Handles PDF upload/download to AWS S3
"""

import boto3
import os
from botocore.exceptions import ClientError
from dotenv import load_dotenv
import tempfile

load_dotenv()


class S3Storage:
    """Manages PDF storage in AWS S3"""

    def __init__(self):
        """Initialize S3 client"""
        self.bucket_name = os.getenv("S3_BUCKET_NAME")
        self.region = os.getenv("AWS_REGION", "us-east-1")

        # Initialize S3 client
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=self.region
        )

        # Validate configuration
        if not self.bucket_name:
            raise ValueError("S3_BUCKET_NAME not found in environment variables")

    def upload_file(self, file_content: bytes, filename: str) -> str:
        """
        Upload a file to S3

        Args:
            file_content: File content as bytes
            filename: Name of the file

        Returns:
            S3 key (path) of the uploaded file
        """
        try:
            s3_key = f"documents/{filename}"

            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=s3_key,
                Body=file_content,
                ContentType="application/pdf"
            )

            print(f"Uploaded {filename} to s3://{self.bucket_name}/{s3_key}")
            return s3_key

        except ClientError as e:
            raise Exception(f"Failed to upload to S3: {str(e)}")

    def download_file(self, s3_key: str) -> str:
        """
        Download a file from S3 to a temporary location

        Args:
            s3_key: S3 key of the file

        Returns:
            Path to the temporary file
        """
        try:
            # Create temporary file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
            temp_path = temp_file.name
            temp_file.close()

            # Download from S3
            self.s3_client.download_file(
                self.bucket_name,
                s3_key,
                temp_path
            )

            print(f"Downloaded s3://{self.bucket_name}/{s3_key} to {temp_path}")
            return temp_path

        except ClientError as e:
            raise Exception(f"Failed to download from S3: {str(e)}")

    def delete_file(self, s3_key: str) -> bool:
        """
        Delete a file from S3

        Args:
            s3_key: S3 key of the file

        Returns:
            True if successful
        """
        try:
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=s3_key
            )
            print(f"Deleted s3://{self.bucket_name}/{s3_key}")
            return True

        except ClientError as e:
            raise Exception(f"Failed to delete from S3: {str(e)}")

    def list_files(self) -> list:
        """
        List all PDF files in the bucket

        Returns:
            List of file information dictionaries
        """
        try:
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix="documents/"
            )

            files = []
            if "Contents" in response:
                for obj in response["Contents"]:
                    if obj["Key"].endswith(".pdf"):
                        files.append({
                            "key": obj["Key"],
                            "filename": obj["Key"].split("/")[-1],
                            "size": obj["Size"],
                            "last_modified": obj["LastModified"].isoformat()
                        })

            return files

        except ClientError as e:
            raise Exception(f"Failed to list S3 files: {str(e)}")

    def get_file_url(self, s3_key: str, expires_in: int = 3600) -> str:
        """
        Generate a presigned URL for temporary access

        Args:
            s3_key: S3 key of the file
            expires_in: URL expiration time in seconds (default 1 hour)

        Returns:
            Presigned URL string
        """
        try:
            url = self.s3_client.generate_presigned_url(
                "get_object",
                Params={
                    "Bucket": self.bucket_name,
                    "Key": s3_key
                },
                ExpiresIn=expires_in
            )
            return url

        except ClientError as e:
            raise Exception(f"Failed to generate presigned URL: {str(e)}")
