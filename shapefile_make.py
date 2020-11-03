import osgeo.ogr as ogr
import osgeo.osr as osr
import csv


# set up the shapefile driver
class make_shp:
    def __init__(self,filepath,filename):
        self.driver = ogr.GetDriverByName("ESRI Shapefile")
        self.data_source = self.driver.CreateDataSource(filepath+filename+".shp")
        self.srs = osr.SpatialReference()
        self.srs.ImportFromEPSG(4326)
        # self.lyrname=layername
        self.layers={}




    def create_layer(self,name):
        layer = self.data_source.CreateLayer(name, self.srs, ogr.wkbPoint)
        self.layers[name]=layer
        layer.CreateField(ogr.FieldDefn("Latitude", ogr.OFTReal))
        layer.CreateField(ogr.FieldDefn("Longitude", ogr.OFTReal))

    def add_pt(self,lat,long,layername):
        feature = ogr.Feature(self.layers[layername].GetLayerDefn())
        feature.SetField("Latitude", lat)
        feature.SetField("Longitude", long)
        wkt = "POINT(%f %f)" %  (float(long) , float(lat))
        point = ogr.CreateGeometryFromWkt(wkt)

      # Set the feature geometry using the point
        feature.SetGeometry(point)
      # Create the feature in the layer (shapefile)
        self.layers[layername].CreateFeature(feature)
      # Dereference the feature
        feature = None

    def create_polygon(self,coords,layername):
        ring = ogr.Geometry(ogr.wkbLinearRing)
        for coord in coords:
            ring.AddPoint(coord[0],coord[1])

        # Create polygon
        poly = ogr.Geometry(ogr.wkbPolygon)
        poly.AddGeometry(ring)


        layer = self.data_source.CreateLayer(layername, self.srs, ogr.wkbPolygon)
        # Add one attribute
        layer.CreateField(ogr.FieldDefn('id', ogr.OFTInteger))
        defn = layer.GetLayerDefn()

        # Create a new feature (attribute and geometry)
        feat = ogr.Feature(defn)
        feat.SetField('id', 123)

        # Make a geometry, from Shapely object
        geom = ogr.CreateGeometryFromWkt(poly.ExportToWkt())
        feat.SetGeometry(geom)

        layer.CreateFeature(feat)
        feat = geom = None  # destroy these

        # Save and close everything
        layer = feat = geom = None











# create the data source


# create the spatial reference, WGS84


# create the layer


# Add the fields we're interested in
# field_name = ogr.FieldDefn("Name", ogr.OFTString)
# field_name.SetWidth(24)
# layer.CreateField(field_name)
# field_region = ogr.FieldDefn("Region", ogr.OFTString)
# field_region.SetWidth(24)
# layer.CreateField(field_region)

# layer.CreateField(ogr.FieldDefn("Elevation", ogr.OFTInteger))

# dict1={'Name':'BarrenIsland','Region':'ANDNIC','Latitude':12.292,'Longitude':93.875,'Elev':354}
# dict2={'Name':'Narcondum','Region':'ANDNIC','Latitude':13.43,'Longitude':94.25,'Elev':710}
#
# reader=[dict1,dict2]
# # Process the text file and add the attributes and features to the shapefile
# for row in reader:
#     print(row)
#   # create the feature
#     feature = ogr.Feature(layer.GetLayerDefn())
#   # Set the attributes using the values from the delimited text file
#     feature.SetField("Name", row['Name'])
#     feature.SetField("Region", row['Region'])
#     feature.SetField("Latitude", row['Latitude'])
#     feature.SetField("Longitude", row['Longitude'])
#     feature.SetField("Elevation", row['Elev'])
#
#   # create the WKT for the feature using Python string formatting
#     wkt = "POINT(%f %f)" %  (float(row['Longitude']) , float(row['Latitude']))
#
#   # Create the point from the Well Known Txt
#     point = ogr.CreateGeometryFromWkt(wkt)
#
#   # Set the feature geometry using the point
#     feature.SetGeometry(point)
#   # Create the feature in the layer (shapefile)
#     layer.CreateFeature(feature)
#   # Dereference the feature
#     feature = None
#
# # Save and close the data source
# data_source = None
