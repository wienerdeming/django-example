# Python
import os
import io
import uuid
from PIL import Image, ImageDraw
from urllib.parse import urlencode

# Django
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.urls import reverse as rev


def reverse(url, params=None, **kwargs):
    """
    :param url:
    :param params: dict
    :return: full_url: full_url
    """
    return rev(url, **kwargs) + '?' + urlencode(params or {})


def timezone_fix(str_date):
    date = parse_datetime(str_date)
    date_timezone = timezone.localtime(date)
    return str(date_timezone).replace(' ', 'T')


def get_files_for_checking(start_path):
    source_files = []
    for root, dirs, files in os.walk(start_path, topdown=True):
        for file in files:
            if file.endswith('.py') and not root.endswith('migrations'):
                source_files.append('%s/%s' % (root, file))
    return source_files


def generate_image():
    file = io.BytesIO()
    image = Image.new('RGBA', size=(255, 255), color='white')
    draw = ImageDraw.Draw(image)
    draw.text((100, 100), 'Test image', fill='black')
    image.save(file, 'png')
    file.name = 'test.png'
    file.seek(0)
    return file


def get_file_path(instance, filename):
    ext = filename.rsplit('.', 1)
    date_dir = timezone.now().strftime('%Y/%m/%d')
    upload_path = 'upload_storage/{date_dir}/{name}.{ext}' \
        .format(date_dir=date_dir, name=uuid.uuid4(), ext=ext[1])
    return upload_path
