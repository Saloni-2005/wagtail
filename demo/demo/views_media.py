from django.http import HttpResponse, Http404
from django.conf import settings
from django.views.static import serve
import os
import mimetypes


def serve_media(request, path):
    """
    Serve media files in production when DEBUG=False
    This is a simple fallback for serving uploaded images
    """
    try:
        # Construct the full file path
        document_root = settings.MEDIA_ROOT
        fullpath = os.path.join(document_root, path)
        
        # Security check - ensure the path is within MEDIA_ROOT
        if not os.path.commonpath([document_root, fullpath]) == document_root:
            raise Http404("Invalid path")
        
        # Check if file exists
        if not os.path.exists(fullpath) or not os.path.isfile(fullpath):
            raise Http404("File not found")
        
        # Determine content type
        content_type, encoding = mimetypes.guess_type(fullpath)
        if content_type is None:
            content_type = 'application/octet-stream'
        
        # Read and serve the file
        with open(fullpath, 'rb') as f:
            response = HttpResponse(f.read(), content_type=content_type)
            
        # Add cache headers for images
        if content_type.startswith('image/'):
            response['Cache-Control'] = 'public, max-age=3600'
            
        return response
        
    except Exception as e:
        raise Http404(f"Error serving media file: {e}")


def serve_protected_media(request, path):
    """
    Serve media files with basic protection
    You can add authentication checks here if needed
    """
    # Add any authentication/permission checks here
    # For now, just serve the file
    return serve_media(request, path)