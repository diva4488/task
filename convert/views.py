from django.http import HttpResponse
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

    return render(request, 'upload.html')


'''from django.shortcuts import render
from .script import create_gpx_from_csv, getGPXData, conv_json_model, create_gpx_from_csv
import os
import json
from django.http import HttpResponse
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

             

            # Prepare the file for download
            with open(gpx_file_path, 'rb') as f:
                response = HttpResponse(f.read(), content_type='application/gpx+xml')
                response['Content-Disposition'] = f'attachment; filename={smart_str(output_file)}'
                return response

            # Ensure the gpx-json folder exists
            gpx_json_folder = 'gpx-json'
            if not os.path.exists(gpx_json_folder):
                os.makedirs(gpx_json_folder)

            # Create the JSON file from GPX data
            #json_file_path = os.path.join(gpx_json_folder, f'gpx-json-utc-{os.path.basename(csv_file_path).split(".")[0]}.json')
            #with open(json_file_path, 'w') as json_file:
                #json.dump(gpx_data, json_file, indent=2)

            # Convert JSON to IST
            #Sconv_json_model(json_file_path)

            # Optionally delete the temporary GPX file
            # os.remove(gpx_file_path)
            return render(request, 'success.html', {'gpx_file_path': gpx_file_path})
        else:
            # Handle conversion failure
            return render(request, 'error.html')

    return render(request, 'upload.html')'''
