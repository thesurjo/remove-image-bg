import os
from django.shortcuts import render
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from rembg import remove
from PIL import Image
from io import BytesIO

def remove_background(request):
    if request.method == 'POST' and request.FILES.get('image'):
        input_image = request.FILES['image']
        
        # Save the uploaded image
        input_path = default_storage.save('uploads/' + input_image.name, ContentFile(input_image.read()))
        input_path = default_storage.path(input_path)
        
        # Process image and remove background
        output_path = input_path.replace('uploads/', 'processed/')
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Remove background
        input_img = Image.open(input_path)
        output_img = remove(input_img)
        output_img.save(output_path, 'PNG')
        
        # Get relative paths for template
        input_url = default_storage.url(input_path.split('media/')[-1])
        output_url = default_storage.url(output_path.split('media/')[-1])
        
        return render(request, 'bgremover/index.html', {
            'input_image': input_url,
            'output_image': output_url
        })
    
    return render(request, 'bgremover/index.html')
