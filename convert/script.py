import csv
import gpxpy.gpx
from datetime import datetime, timedelta
import gpxpy
from geopy import distance
import os
import json
import math
import argparse



def convert_to_utc(time_str):
    time_obj = datetime.strptime(time_str, "%m/%d/%Y %H:%M:%S")
    fixed_offset = timedelta(hours=5, minutes=30)
    time_utc = time_obj - fixed_offset
    return time_utc

def create_gpx_from_csv(csv_file, output_file , output_folder):

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)


    gpx = gpxpy.gpx.GPX()
    gpx_track = gpxpy.gpx.GPXTrack()
    gpx_segment = gpxpy.gpx.GPXTrackSegment()
    gpx_track.segments.append(gpx_segment)
    gpx.tracks.append(gpx_track)

    with open(csv_file, 'r') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            latitude, longitude = float(row['Lat']), float(row['Lon'])
            time_str = row['Time']
            speed = float(row['Speed'])
            
            time_str = time_str[:-14]

            time_utc_str = convert_to_utc(time_str)

            trkpt = gpxpy.gpx.GPXTrackPoint(latitude, longitude)
            trkpt.time = time_utc_str
            trkpt.speed = speed


            gpx_segment.points.append(trkpt)
    gpx_xml = gpx.to_xml()
    gpx_xml = gpx_xml.replace('xmlns="http://www.topografix.com/GPX/1/1"', 'xmlns="http://www.topografix.com/GPX/1/0"')
    gpx_xml = gpx_xml.replace('version="1.1" creator="gpx.py', 'version="1.0" creator="BasicAirData GPS Logger 3.2.1')

    with open(f'{output_folder}/{output_file}', 'w') as gpxfile:
        gpxfile.write(gpx_xml)

def getGPXData(gpxFileName=None,all_gpx={}):

    #gpx = gpxpy.parse(open(os.path.join(f"{folderName}",gpxFileName), 'r'))
    gpx = gpxpy.parse( open(gpxFileName) , 'r')
    gpxData={
        "chk_pnts":{}
    }
    dis=0
    disInMeters=0
    startPoint=[0,0]
    dis_3d=0

    for track in gpx.tracks:
        for segment in track.segments:
            for i,point in enumerate(segment.points):
                
                if i==0:
                    startPoint[0],startPoint[1] =  (point.latitude, point.longitude)


                try:
                    nxt=segment.points[i+1]
                    newport_ri = (point.latitude, point.longitude)
                    cleveland_oh = (nxt.latitude, nxt.longitude)
                    dis+=distance.distance(newport_ri, cleveland_oh).km

                    dis_bt_points=distance.distance(newport_ri, cleveland_oh).m

                    disInMeters+=dis_bt_points

                    h=abs(nxt.elevation-point.elevation)
                    dis_3d+=math.sqrt((h*h)+(dis_bt_points*dis_bt_points))
                    print("testing")
                except IndexError:
                    print('file ended..')
                except:
                    print(i,len(segment.points))
                    print('Error in gpxParser.py > getGPXData() > line:28')
                    pass

                gpxData['chk_pnts'][str(point.time.replace(microsecond=0))]={
                    "lat":point.latitude,
                    "lng":point.longitude,
                    "distanceInMeters":disInMeters
                }
                all_gpx[str(point.time.replace(microsecond=0))]={
                    "lat":point.latitude,
                    "lng":point.longitude,
                    "distanceInMeters":disInMeters
                }

    gpxData['dist_covered']= disInMeters

    print("extraction ended.")
    return gpxData,all_gpx

def convert_to_ist( time_str):

    # opening json file 

    time_str = time_str.split('+')[0]
    #print(time_str)
    #time_obj = datetime.strptime(time_str, "%Y/%m/%d %H:%M:%S")
    # "2024-01-22 07:46:57"
    time_obj = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
    #time_obj = datetime.strptime(time_str, "%m/%d/%Y %H:%M:%S")
    fixed_offset = timedelta(hours=5, minutes=30)
    time_utc = time_obj + fixed_offset
    return time_utc

def conv_json_model(json_file ):
    base = json_file.split("/")[0]
    file = json_file.split("/")[-1].split(".")[0]

    # utc data after conversion 
    utc_data = {}

    with open(json_file, "r") as f : 
        data = json.load(f)

    for k , d  in data.items():
        key_data = k
        ist = convert_to_ist(key_data)
        utc_data[f'{ist}'] = d

    with open(f'{base}/ist-{file}.json', "w") as f : 
       json.dump(utc_data , f , indent=2 )
       f.close()
    




if __name__ == "__main__":

    # add the csv file path 
    csv_file = "Montgomery_TRACKPOINTS.csv" 

    ### ARGUEMENT PARSER
    parser = argparse.ArgumentParser(description='Process an image and find extreme points on the mask.')
    #parser.add_argument('image_path', type=str, help='Path to the input image file')
    parser.add_argument('--csv_file', type=str, default = csv_file ,  help='Path to the CSV file')
   

    # Parse command-line arguments
    args = parser.parse_args()

    # data extracted from the json file 
    gpx_data = {}
    gpx_path = "gpx"

    # gpx name of the csv file 
    gpx_output_file = f"csv2gpx_{csv_file[:-4]}.gpx"  
    # creating gpx file 
    create_gpx_from_csv(csv_file, gpx_output_file , gpx_path )

    # loading the gpx file to convert to json 
    data, gpx_data = getGPXData( f'{gpx_path}/{gpx_output_file}' , gpx_data)
    

    # gpx-json  folder path 
    gpx2json_path = "gpx-json"
    
    if not os.path.exists(gpx2json_path):
        os.makedirs(gpx2json_path)

    # dumping the gpx data into the json file 
    with open(f'{gpx2json_path}/gpx-json-utc-{csv_file[:-4]}.json','w') as f:
        json.dump(gpx_data ,f)

    # covert to ist back again for tracking 
    conv_json_model(f'{gpx2json_path}/gpx-json-utc-{csv_file[:-4]}.json')
        
    
    


