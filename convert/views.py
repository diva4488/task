'''from django.http import HttpResponse
from django.shortcuts import render
from .script import create_gpx_from_csv, getGPXData
import os
from django.utils.encoding import smart_str

def upload_file(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        print(csv_file)

        # Save the uploaded CSV file to a local path
        csv_file_path = 'uploaded_file.csv'
        with open(csv_file_path, 'wb+') as destination:
            for chunk in csv_file.chunks():
                destination.write(chunk)

        # Define output paths
        output_folder = 'output_folder'
        output_file = 'output_file.gpx'

        # Ensure the output folder exists
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Convert CSV to GPX
        create_gpx_from_csv(csv_file_path, output_file, output_folder)
        gpx_file_path = os.path.join(output_folder, output_file)

        if os.path.exists(gpx_file_path):
            # Get GPX data
            data, gpx_data = getGPXData(gpx_file_path)

            # Optionally delete the temporary CSV file
            os.remove(csv_file_path)

            # Prepare the file for download
            with open(gpx_file_path, 'rb') as f:
                response = HttpResponse(f.read(), content_type='application/gpx+xml')
                response['Content-Disposition'] = f'attachment; filename={smart_str(output_file)}'
                return response

        else:
            # Handle conversion failure
            return render(request, 'error.html')

    return render(request, 'upload.html')'''

from django.http import HttpResponse
from django.shortcuts import render
from .script import create_gpx_from_csv, getGPXData
import os
import json

import datetime

def upload_file(request):
  
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        print(csv_file)

        # Generate a timestamped file name
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        original_file_name = os.path.splitext(csv_file.name)[0]
        output_file = f'{original_file_name}_{timestamp}.gpx'
        

        # Define output paths
        output_folder = 'output_folder'
        gpx_file_path = os.path.join(output_folder, output_file)

        # Save the uploaded CSV file to a local path
        csv_file_path = 'uploaded_file.csv'
        with open(csv_file_path, 'wb+') as destination:
            for chunk in csv_file.chunks():
                destination.write(chunk)

        # Ensure the output folder exists
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Convert CSV to GPX
        create_gpx_from_csv(csv_file_path, output_file, output_folder)

        if os.path.exists(gpx_file_path):
            # Get GPX data
            data, gpx_data = getGPXData(gpx_file_path)

            # Optionally delete the temporary CSV file
            os.remove(csv_file_path)
            # Prepare the file for download with the correct file name
            print(output_file)
            response = HttpResponse(open(gpx_file_path, 'rb').read(), content_type='application/gpx+xml')
            response['Content-Disposition'] = f'attachment; filename={output_file}'
            return response

        else:
            # Handle conversion failure
            return render(request, 'error.html')

    return render(request, 'upload.html' )


'''from django.http import HttpResponse
from django.shortcuts import render
from .script import create_gpx_from_csv, getGPXData
import os
import json
from django.utils.encoding import smart_str
import datetime

def upload_file(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        print(csv_file)

        # Generate a timestamped file name
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        original_file_name = os.path.splitext(csv_file.name)[0]
        output_file = f'{original_file_name}_{timestamp}.gpx'

        # Define output paths
        output_folder = 'output_folder'
        gpx_file_path = os.path.join(output_folder, output_file)

        # Save the uploaded CSV file to a local path
        csv_file_path = 'uploaded_file.csv'
        with open(csv_file_path, 'wb+') as destination:
            for chunk in csv_file.chunks():
                destination.write(chunk)

        # Ensure the output folder exists
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Convert CSV to GPX
        create_gpx_from_csv(csv_file_path, output_file, output_folder)

        if os.path.exists(gpx_file_path):
            # Get GPX data
            data, gpx_data = getGPXData(gpx_file_path)

            # Optionally delete the temporary CSV file
            os.remove(csv_file_path)

            # Prepare the file for download with the correct file name
            output_filename = os.path.basename(gpx_file_path)

            response = HttpResponse(open(gpx_file_path, 'rb').read(), content_type='application/gpx+xml')
            response['Content-Disposition'] = f'attachment; filename="{smart_str(output_filename)}"'
            return response
          
        else:
            # Handle conversion failure
            return render(request, 'error.html')

    return render(request, 'upload.html')'''
