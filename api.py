import webapp2
from google.appengine.api import images
from google.appengine.api import files
from google.appengine.ext import blobstore
import json


class Upload(webapp2.RequestHandler):
    
    def post(self):
        image = self.request.get('image')
        image = image[23:]
        image = image.decode('base64')

        file_name = files.blobstore.create(mime_type='image/jpeg')
        with files.open(file_name, 'a') as f:
            f.write(image)
        files.finalize(file_name)

        blob_key = files.blobstore.get_blob_key(file_name)
        blob_info = blobstore.BlobInfo.get(blob_key)

        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps({
            "url": images.get_serving_url(blob_info)}))
    

app = webapp2.WSGIApplication([
    ('/upload', Upload),
], debug=True)
