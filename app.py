from flask import Flask, render_template,jsonify,request,Response,send_from_directory,send_file,redirect,url_for
import os
import io
import tempfile
import zipfile
import json
import numpy as np
from shapefile_make import make_shp
import pandas as pd

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

app=Flask(__name__)

poly_points=[]

shape_type=''

def generate_csv_file(file_df):
      # Create an o/p buffer
    file_buffer = io.StringIO()



      # Write the dataframe to the buffer
    file_df.to_csv(file_buffer, encoding="utf-8", index=False, sep=",")


      # Seek to the beginning of the stream
    file_buffer.seek(0)
    # file_buffer.close()
    return file_buffer


def mkZipFile(row):
    zipdir = tempfile.mkdtemp(prefix='/tmp/')
    oldpath = os.getcwd()
    os.chdir(zipdir)

    jdata = json.loads(row)
    for conf in jdata:
        for f in conf:
            makeFile(zipdir, f, conf[f])

    # Create the in-memory zip image
    data = io.BytesIO()
    with zipfile.ZipFile(data, mode='w') as z:
        for fname in os.listdir("."):
            z.write(fname)
            os.unlink(fname)
    data.seek(0)

    os.chdir(oldpath)
    os.rmdir(zipdir)
    return data

@app.route("/shp_coords",methods=['POST'])
def shp_coords():
    data=request.get_json()
    poly_points=data['points']
    shape_type=data['value']
    app.config['POLY_POINT']=poly_points



    type=request.args.get('value')
    print(type(points[0][0]))
    return jsonify(results='success')


@app.route("/download")
def download():
    zipdir = tempfile.mkdtemp(prefix='/tmp/')
    print("zipdir:",zipdir)
    oldpath = os.getcwd()
    os.chdir(zipdir)
    print(os.getcwd())
    from datetime import datetime
    poly_points=app.config['POLY_POINT']
    # print("for shp file: ",poly_points)

    # vert=[(18.56536502546686,73.87096774193552),(19.142614601018643,72.94057724957558),(19.95755517826822,73.78268251273347),(19.828522920203703,75.26315789473688),(18.97962648556873,74.76061120543297),(18.56536502546686,73.87096774193552)]
    fil_name="shapefile_"+datetime.now().strftime("%d_%m_%Y__%H:%M:%S")
    test2=make_shp("./",fil_name)
    test2.create_polygon(poly_points,"poly")#format is (lat,long)
    test2.data_source=None




    data = io.BytesIO()
    # print("filenames....")
    # print(os.listdir("."))
    with zipfile.ZipFile(data, mode='w') as z:
        for fname in os.listdir("."):
            print(fname)
            z.write(fname)
            os.unlink(fname)
    data.seek(0)

    os.chdir(oldpath)
    os.rmdir(zipdir)
    return send_file(
        data,
        mimetype='application/zip',
        as_attachment=True,
        attachment_filename='shapefiles.zip')



@app.route("/shapefile")
def shapefile():
    return(render_template('shapefile.html'))




@app.route("/")
def draw():
    return(render_template('draw_shp.html'))







if __name__ =='__main__':
    app.run(debug=True)
