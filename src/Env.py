import json

class Env:
    
    def __init__(self):
        self.env = {
            "ORIDIR":"/mnt/hgfs/dev-volumes-data1/", # persistent volume 
            "DESTDIR":"/mnt/hgfs/dev-volumes-data1/", 
            "APIGW-PORT":9100
        }
    
    def get_env(self):
        return self.env
    
    
        