from flask import Flask, render_template,jsonify,request,Response,send_from_directory,send_file,redirect,url_for
import os
import io
import tempfile
import zipfile
from spectral_flask1 import spectra
from pixel_latlong2_flask import transform 
import json
import numpy as np
# from shapefile_make import make_shp
# spectra_bands=[420.570, 422.915, 425.259, 427.602, 429.945, 432.288, 434.629, 436.971, 439.311, 441.651, 443.991, 446.330, 448.668, 451.006, 453.343, 455.680, 458.016, 460.352, 462.687, 465.021, 467.355, 470.000, 472.021, 474.353, 476.684, 479.015, 481.346, 483.676, 486.005, 488.333, 490.661, 492.989, 495.316, 497.642, 499.968, 502.293, 504.618, 506.942, 509.266, 511.588, 513.911, 516.233, 518.554, 520.875, 523.195, 525.514, 527.833, 530.151, 532.469, 534.786, 537.103, 539.419, 541.734, 544.049, 546.364, 548.678, 550.000, 553.303, 555.615, 557.927, 560.238, 562.548, 564.858, 567.167, 569.476, 571.784, 574.091, 576.398, 578.704, 581.010, 583.315, 585.620, 587.924, 590.228, 592.530, 594.833, 597.135, 599.436, 601.736, 604.036, 606.336, 608.635, 610.933, 613.231, 615.528, 617.824, 620.000, 622.416, 624.711, 627.005, 629.299, 631.592, 633.885, 636.177, 638.468, 640.759, 643.049, 645.339, 647.628, 649.917, 652.205, 654.492, 656.779, 659.065, 661.351, 663.636, 665.921, 668.205, 670.488, 672.771, 675.053, 677.335, 679.616, 681.897, 684.177, 686.456, 688.735, 691.013, 693.291, 695.568, 697.845, 700.121, 702.396, 704.671, 706.945, 709.219, 711.492, 713.765, 716.037, 718.308, 720.579, 722.849, 725.119, 727.388, 729.656, 731.924, 734.192, 736.459, 738.725, 740.991, 743.256, 745.520, 747.784, 750.048, 752.310, 754.573, 756.834, 759.095, 761.356, 763.616, 765.875, 768.134, 770.392, 772.650, 774.907, 777.164, 779.420, 781.675, 783.930, 786.184, 788.438, 790.691, 792.943, 795.195, 797.447, 799.697, 801.948, 804.197, 806.446, 808.695, 810.943, 813.190, 815.437, 817.683, 819.929, 822.174, 824.418, 826.662, 828.906, 831.148, 833.391, 835.632, 837.873, 840.114, 842.354, 844.593, 846.832, 849.070, 851.308, 853.545, 855.781, 858.017, 860.253, 862.487, 864.721, 866.955, 869.188, 871.421, 873.653, 875.884, 878.115, 880.345, 882.574, 884.803, 887.032, 889.260, 891.487, 893.714, 895.940, 898.166, 900.391, 902.615, 904.839, 907.062, 909.285, 911.507, 913.729, 915.950, 918.170, 920.390, 922.610, 924.828, 927.046, 929.264, 931.481, 933.698, 935.913, 938.129, 940.343, 942.558, 944.771, 946.984, 949.197, 951.409, 953.620, 955.831, 958.041, 960.250, 962.459, 964.668, 966.876, 969.083]
spectra_bands=[420.57, 443.991, 467.355, 490.661, 513.911, 537.103, 560.238, 583.315, 606.336, 629.299, 652.205, 675.053, 697.845, 720.579, 743.256, 765.875, 788.438, 810.943, 833.391, 855.781, 878.115, 900.391, 922.61, 944.771, 966.876]

from analysis import analyse
from analysis_PixData import pixData
import pandas as pd
import detect
import cv2

# lwc_img_path=url_for('static',filename='lwc_georef_final.tif')

# data_analyse=pixData('static/for_csv.tif')

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
data_analyse=pixData('static/lwc_georef_final.tif')



class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

app=Flask(__name__)

# app.config['CLIENT_IMAGES']="/Users/yani/Desktop/IAS/flaskapp2/static/client/images"
# @app.after_request
# def add_header(response):
#     """
#     Add headers to both force latest IE rendering engine or Chrome Frame,
#     and also to cache the rendered page for 10 minutes.
#     """
#     response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
#     response.headers['Cache-Control'] = 'public, max-age=0'
#     return response
#

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




@app.route('/')
def index():
    return render_template('index_v2.html')

@app.route('/background_process')
def bp():
    spectr_tifpath=APP_ROOT+url_for('static',filename='spectra/geo_hsi_data_frombsq.tif')
    spectr_hdrpath=APP_ROOT+url_for('static',filename='spectra/geo_hsi_data_frombsq.hdr')

    sp=spectra(spectr_tifpath,spectr_hdrpath)
    # sp=spectra('static/geo_ref_hsi.tif')
    # labels,values=sp.plot_spectra(1000,700)
    x=request.args.get('x', 0, type=int)
    y=request.args.get('y', 0, type=int)
    legend = 'Pixel'+str(x)+","+str(y)
    values = np.asarray(sp.plot_spectra(x,y))
    print(type(values))
    values_demo=[1,2,3,4]
    # print(json.dumps(values))
    # x=json.dumps(values)
    json_dump = json.dumps({'label': legend, 'arr': values}, cls=NumpyEncoder)
    return (json_dump)


@app.route('/coord_pixel')
def cp():
    lat=request.args.get('lat', 0, type=float)
    long=request.args.get('long', 0, type=float)
    print("lat: ",lat)
    print("long: ",long)
    hsi_path=APP_ROOT+url_for('static',filename='spectra/geo_ref_hsi.tif')
    print("hsi path :",hsi_path)
    tr=transform(hsi_path)
    # tr=transform('static/3D/spectra.tiff')#this is throwing error
    err=0
    x,y,err=tr.transfromPt(lat,long)
    print("inside coord_pixe:x={},y={},err={}".format(x,y,err))
    return (jsonify(x=x,y=y,err=err))



# @app.route('/hscube')
# def hscube():
#     return render_template('model2.html')


@app.route('/spectral')
def spectral():
    return render_template('spectral.html')


@app.route('/model')
def model():
    return render_template('model2_v3.html',labels=spectra_bands)



@app.route('/team')
def team():
    return render_template('team2.html')


@app.route('/brdf')
def brdf():
    return render_template('brdf.html')

# @app.route("/get-image/<image_name>")
# def get_image(image_name):
#     print({image_name})
#     try:
#         return send_from_directory(app.config["CLIENT_IMAGES"], filename=image_name, as_attachment=True)
#     except FileNotFoundError:
#         abort(404)

#
# vert=[(18.56536502546686,73.87096774193552),(19.142614601018643,72.94057724957558),(19.95755517826822,73.78268251273347),(19.828522920203703,75.26315789473688),(18.97962648556873,74.76061120543297),(18.56536502546686,73.87096774193552)]
#
# test2=make_shp("shape/","test_16thaug_poly")
# test2.create_polygon(vert,"poly")#format is (lat,long)
# test2.data_source=None

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


# @app.route("/download")
# def download():
#     zipdir = tempfile.mkdtemp(prefix='/tmp/')
#     print("zipdir:",zipdir)
#     oldpath = os.getcwd()
#     os.chdir(zipdir)
#     print(os.getcwd())
#     from datetime import datetime
#     poly_points=app.config['POLY_POINT']
#     print("for shp file: ",poly_points)

#     vert=[(18.56536502546686,73.87096774193552),(19.142614601018643,72.94057724957558),(19.95755517826822,73.78268251273347),(19.828522920203703,75.26315789473688),(18.97962648556873,74.76061120543297),(18.56536502546686,73.87096774193552)]
#     fil_name="shapefile_"+datetime.now().strftime("%d_%m_%Y__%H:%M:%S")
#     test2=make_shp("./",fil_name)
#     test2.create_polygon(poly_points,"poly")#format is (lat,long)
#     test2.data_source=None




    # data = io.BytesIO()
    # # print("filenames....")
    # # print(os.listdir("."))
    # with zipfile.ZipFile(data, mode='w') as z:
    #     for fname in os.listdir("."):
    #         print(fname)
    #         z.write(fname)
    #         os.unlink(fname)
    # data.seek(0)

    # os.chdir(oldpath)
    # os.rmdir(zipdir)
    # return send_file(
    #     data,
    #     mimetype='application/zip',
    #     as_attachment=True,
    #     attachment_filename='shapefiles.zip')



# @app.route("/shapefile")
# def shapefile():
#     return(render_template('shapefile.html'))




# @app.route("/draw")
# def draw():
#     return(render_template('draw_shp.html'))


# @app.route("/shp_coords",methods=['POST'])
# def shp_coords():
#     data=request.get_json()
#     poly_points=data['points']
#     shape_type=data['value']
#     app.config['POLY_POINT']=poly_points



    # type=request.args.get('value')
    # print(type(points[0][0]))
    # return jsonify(results='success')


# @app.route("/analysis")
# def analysis():
#     return render_template('pix_analysis.html')

@app.route("/LAI2")
def LAI2():
    return render_template('LAI_plot_view_RGB.html')

@app.route("/LAI1")
def LAI1():
    return render_template('LAI_vis_RGB.html')

@app.route("/LWC")
def LWC():
    return render_template('LWC.html')


@app.route("/PlotInfo")
def Plot_Info():
    return render_template('Plot_info_v2.html')

@app.route("/tassle_count")
def tassle():
    return render_template('upload.html')


@app.route("/_comp_hist",methods=['POST'])
def comp_hist():
    data_dict={}
    data=request.get_json()
    print("received at server....",data)
    data_dict['coords']=data['coords']
    data_dict['no_of_box']=data['no_of_box']
    data_dict['choice']=data['choice']


    an=analyse('static/lwc_georef_final.tif',data_dict)
    error,hist,bins,mean,median,mode=an.aoi()
    json_dump = json.dumps({"error":error,"hist":hist,"bins":bins,"mean":mean,"median":median,"mode":mode}, cls=NumpyEncoder)
    print("json dumping....",json_dump)
    return(json_dump)


@app.route("/analysis2")
def analysis2():
    return render_template('pix_analysis_v4.html')

#
#
#
# @app.route("/_comp_sep_hist",methods=['POST'])
# def comp_hist2():
#     data_dict={}
#     data=request.get_json()
#     print("received at server....",data)
#     data_dict['coords']=data['coords']
#     data_dict['no_of_box']=data['no_of_box']
#     data_dict['choice']=data['choice']
#
#
#     an=analyse('static/lwc_georef_final.tif',data_dict)
#     error,hist,bins,mean,median,mode,cov=an.aoi()
#     json_dump = json.dumps({"error":error,"hist":hist,"bins":bins,"mean":mean,"median":median,"mode":mode,"cov":cov}, cls=NumpyEncoder)
#     print("json dumping....",json_dump)
#     return(json_dump)
#
# @app.route("/_comp_box",methods=['POST'])
# def comp_box():
#     data_dict={}
#     data=request.get_json()
#     print("received at server....",data)
#     data_dict['coords']=data['coords']
#     data_dict['no_of_box']=data['no_of_box']
#     data_dict['choice']=data['choice']
#
#
#     pd=pixData('static/lwc_georef_final.tif',data_dict)
#     error,box_data=pd.box()
#     json_dump = json.dumps({"error":error,"data":box_data}, cls=NumpyEncoder)
#     print("json dumping....",json_dump)
#     return(json_dump)
#


@app.route("/_bar_plot",methods=['POST'])
def bar_plot():
    data_dict={}
    data=request.get_json()
    print("received at server....",data)
    data_dict['coords']=data['coords']
    data_dict['no_of_box']=data['no_of_box']
    data_dict['choice']=data['choice']



    error,hist,bins,mean,median,mode,cov=data_analyse.aoi(data_dict)
    json_dump = json.dumps({"error":error,"hist":hist,"bins":bins,"mean":mean,"median":median,"mode":mode,"cov":cov}, cls=NumpyEncoder)
    print("json dumping....",json_dump)
    return(json_dump)

@app.route("/_box_plot",methods=['POST'])
def box_plot():
    data_dict={}
    data=request.get_json()
    print("received at server....",data)
    data_dict['coords']=data['coords']
    data_dict['no_of_box']=data['no_of_box']
    data_dict['choice']=data['choice']

    error,box_data=data_analyse.pix_data(data_dict)
    json_dump = json.dumps({"error":error,"data":box_data}, cls=NumpyEncoder)
    print("json dumping....",json_dump)
    return(json_dump)

@app.route("/_plot",methods=['POST'])#only using this in v4
def plot_data():
    data_dict={}
    data=request.get_json()
    print("received at server....",data)
    data_dict['coords']=data['coords']
    data_dict['no_of_box']=data['no_of_box']
    data_dict['choice']=data['choice']

    error,box_data,norm_dist,normx,freq_arr,top25,top50,bot25,bot50=data_analyse.pix_data(data_dict)
    error2,hist,bins,mean,median,mode,cov=data_analyse.aoi(data_dict)
    uniq_vals=[]
    counts=[]
    for uniq,count in freq_arr:
        uniq_vals.append(uniq)
        counts.append(count)

    json_dump = json.dumps({"error":error*error2,"bot25":bot25,"bot50":bot50,"normdist":norm_dist,"normx":normx,"top25":top25,"top50":top50,"unique":uniq_vals,"counts":counts,"data":box_data,"hist":hist,"bins":bins,"mean":mean,"median":median,"mode":mode,"cov":cov}, cls=NumpyEncoder)
    print("json dumping....",json_dump)
    return(json_dump)



@app.route("/get_csv",methods=['POST'])
def get_csv():
    #   fake_df = generate_fake_data()
    data_dict={}
    data=request.get_json()
    print("received at server....",data)
    data_dict['coords']=data['coords']
    data_dict['no_of_box']=data['no_of_box']

    app.config['DATA_CSV']=data_analyse.get_df(data_dict)

    print(url_for('demo'))
    return jsonify(status=0)




@app.route("/download_csv")
def demo():

    df=app.config['DATA_CSV']
    generated_file = generate_csv_file(df)

    out=io.StringIO()
    df.to_csv(out)
    return Response(out.getvalue(), mimetype="text/csv",headers={"Content-disposition":"attachment; filename=pixel_data.csv"})

@app.route("/upload", methods=['POST'])
def upload():
	target = os.path.join(APP_ROOT, 'images/')
	print("TARGET", target)

	if not os.path.isdir(target):
		os.mkdir(target)
	else:

		print("Couldn't create upload directory: {}".format(target))

	# data = request.form.get("style")

    # data=0
	# print("data",data)

	myFiles = []
    # model="YOLO"

	if(len(request.files.getlist("file"))==0):
		# os.rmdir(target)
		return redirect(url_for('tassle'))

	for file in request.files.getlist("file"):
		print("file", file)
		filename = file.filename
		print("filename", filename)
		destination = "".join([target, filename])
		print("destination", destination)
		file.save(destination)
		myFiles.append(filename)
	print("myfiles ",myFiles)



	return render_template("upload.html", image_names=myFiles, model='YOLO')

# in this function send_image will HAVE to take in the parameter name <filename>
@app.route('/upload/<filename>')
def send_original_image(filename):
	return send_from_directory("images", filename)

# this app route cant be the same as above
@app.route('/upload/<filename>/<model>')
def send_processed_image(filename, model):
	directoryName = os.path.join(APP_ROOT, 'images/')

	image_path=directoryName+filename
	# yolo_path=url_for('static')+'/yolo'
	labels_path=APP_ROOT+url_for('static',filename='yolo/obj.names')
	cfgpath=APP_ROOT+url_for('static',filename='yolo/yolov4-obj.cfg')
	wpath=APP_ROOT+url_for('static',filename='yolo/yolov4-obj_last.weights')

	print("label path:",labels_path)
	print("cfg path:",cfgpath)
	print("w path:",wpath)



	newImg= detect.get_processed(directoryName,image_path,labels_path,cfgpath,wpath,confthresh=0.5,nmsthresh=0.2)

	return send_from_directory("images", newImg)













if __name__ =='__main__':
    app.run(debug=True)
