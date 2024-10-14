import boto3
from botocore.client import Config
import os
import asyncio
import io
import random
import string
from datetime import datetime

class S3Handler:
    def __init__(self):
        self.aws_access_key_id = os.getenv("aws_access_key_id")
        self.aws_secret_access_key = os.getenv("aws_secret_access_key")
        self.region_name = os.getenv("region_name")
        self.bucket_name = os.getenv("bucket_name")
        self.s3_client = boto3.client('s3', 
                                      aws_access_key_id=self.aws_access_key_id, 
                                      aws_secret_access_key=self.aws_secret_access_key, 
                                      region_name=self.region_name, 
                                      config=Config(signature_version='s3v4'))

    def generate_filename(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        return f"{timestamp}_{random_string}.png"

    async def upload_to_s3(self, image, filename=None):
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        if filename is None:
            filename = self.generate_filename()
        
        await asyncio.to_thread(self.s3_client.upload_fileobj, img_byte_arr, self.bucket_name, filename)
        
        url = f"https://{self.bucket_name}.s3.amazonaws.com/{filename}"
        return url

    async def upload_images(self, images, filenames=None):
        if filenames is None:
            filenames = [self.generate_filename() for _ in images]
        elif len(filenames) < len(images):
            filenames.extend([self.generate_filename() for _ in range(len(images) - len(filenames))])
        
        tasks = [self.upload_to_s3(image, filename) for image, filename in zip(images, filenames)]
        return await asyncio.gather(*tasks)

    def get_image_url(self, filename):
        return f"https://{self.bucket_name}.s3.amazonaws.com/{filename}"