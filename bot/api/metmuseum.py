import requests
import random
from PIL import Image
import io

class ArtFetch:
    def __init__(self):
        self.base_url = "https://collectionapi.metmuseum.org/"
        self.objects = self.fetch_objects() # chosen set of images to select randomly
        

    def fetch_objects(self):
        """We restrict ourselves to a few domains."""
        # fetch all departements
        t = requests.get(self.base_url + "public/collection/v1/departments").json()
        deps = t["departments"]
        keep_id = []
        for d in deps:
            name = d["displayName"]
            if name == "American Decorative Arts" or name == "Arts of Africa, Oceania, and the Americas" or name == "Asian Art" or name == "European Paintings":
                keep_id.append(str(d["departmentId"]))
        # fetch artworks listed under these departments
        data = {"departmentIds" : "|".join(keep_id)}
        t = requests.get(self.base_url + "public/collection/v1/objects",params=data).json()
        # num = t["total"]
        ids = t["objectIDs"]
        return ids

    def get_random_art(self):
        """Returns an image object of a randomly selected artwork"""
        # fetch the artwork's url
        r_id = self.objects[random.randint(0,len(self.objects))]
        t = requests.get(self.base_url + "public/collection/v1/objects/" + str(r_id)).json()
        im_url = t["primaryImageSmall"]
        # download the image
        resp = requests.get(im_url)
        img = Image.open(io.BytesIO(resp.content))

        return img
