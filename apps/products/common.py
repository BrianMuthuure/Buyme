import boto3
import logging
from botocore.exceptions import ClientError
from decouple import config


def user_directory_path(instance, filename):
    return f"products/{instance.product.name}({instance.product.id})/{filename}"


class S3Handler:
    @staticmethod
    def create_presigned_url(object_name, expiration=8600):
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=config("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=config("AWS_SECRET_ACCESS_KEY"),
            region_name=config("AWS_S3_REGION_NAME"),
        )
        try:
            response = s3_client.generate_presigned_url(
                "get_object",
                Params={
                    "Bucket": config("AWS_STORAGE_BUCKET_NAME"),
                    "Key": object_name},
                ExpiresIn=expiration,
            )
        except ClientError as e:
            logging.error(e)
            return None
        return response
