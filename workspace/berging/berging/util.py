from osgeo import ogr

class OgrException(Exception):
    pass

class OgrInspector:

    datasource = None
    layer = None
    
    def __init__(self, datasource=None):
        if datasource:
            self.open(datasource)

    def __enter__(self):
        return self
    
    def __exit__(self,extype,exval,traceback):
        self.close()
                
    def open(self, datasource):
        self.datasource = ogr.OpenShared(datasource)
        if not self.datasource:
            raise OgrException('Cannot open datasource {}'.format(datasource))
        self.layer = self.datasource.GetLayerByIndex(0)
        if not self.layer:
            self.close()
            raise OgrException('Cannot access layer in datasource {}'.format(datasource))
        defn = self.layer.GetLayerDefn();
        self.fieldnames = [defn.GetFieldDefn(index).GetName() for index in range(defn.GetFieldCount())]
    
    def isclosed(self):
        return self.layer is None
        
    def close(self):
        self.datasource = None
        self.layer = None

    def inspect(self,point):
        if not isinstance(point,ogr.Geometry):
            p = ogr.Geometry(ogr.wkbPoint)
            p.AddPoint(point.x,point.y)
            point = p
        if self.isclosed():
            raise OgrException('Datasource is not opened') 
        self.layer.SetSpatialFilter(point)
        result = {}
        for feature in self.layer:
            # return only first feature
            return {name: feature.GetField(name) for name in self.fieldnames}
#             result[feature.GetFID()] = {name: feature.GetField(name) for name in self.fieldnames}
#         return result
    
# x=125235.71628573995
# y=532004.3869108006
# MAP = '/media/sf_F_DRIVE/projdirs/Texel/Shapefile_website/j4rd.shp'
# 
# if __name__ == '__main__':
#     inspector = OgrInspector(MAP)
#     point = ogr.Geometry(ogr.wkbPoint)
#     point.AddPoint(x,y)
#     print inspector.inspect(point)