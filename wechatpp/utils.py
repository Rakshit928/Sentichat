from django.core.files.storage import FileSystemStorage
from django.conf import settings

def save_file(file):
    # Initialize file storage with the MEDIA_ROOT directory
    fs = FileSystemStorage(location=settings.MEDIA_ROOT, base_url=settings.MEDIA_URL)
    filename = fs.save(file.name, file)  # Save the file and return its name
    return fs.url(filename)  # Generate a URL to access the file
