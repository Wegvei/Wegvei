import requests, json, shutil
class Remove:
    url = None
    name = None
    def __init__(self,elements):
        from .constants import Models
        self.headers = {}
        self.data = {'size': 'auto'}
        for element in elements:

            if (not element in Models[self.name]["Inputs"]) or elements[element] == "":
                continue
            elif Models[self.name]["Inputs"][element]["type"] == "api":
                self.headers[element] = elements[element]
            elif Models[self.name]["Inputs"][element]["type"] == "url":
                self.url = elements[element]
            else:
                self.data[element] = elements[element]
    def remove_background(self,file_name,new_file_name):
        self.file_name = file_name
        self.new_file_name = new_file_name
        response = requests.post(
            self.url,
            files={'image_file': open(self.file_name, 'rb')},
            data=self.data,
            headers=self.headers,
        )
        if response.status_code == requests.codes.ok:
            with open(self.new_file_name, 'wb') as out:
                out.write(response.content)
        else:
            return False
        return True


class RemoveBg(Remove):
    name = "RemoveBg"
    url = 'https://api.remove.bg/v1.0/removebg'

class PhotoRoom(Remove):
    name = "PhotoRoom"
    url = 'https://sdk.photoroom.com/v1/segment'

class Clipdrop(Remove):
    name = "Clipdrop"
    url = 'https://clipdrop-api.co/remove-background/v1'

class Slazzer(Remove):
    name = "Slazzer"
    url = 'https://api.slazzer.com/v2.0/remove_image_background'

    def remove_background(self,file_name,new_file_name):
        self.file_name = file_name
        self.new_file_name = new_file_name
        image_file = {'source_image_file': open(self.file_name, 'rb')}
        response = requests.post(self.url, files=image_file, data=self.data, headers=self.headers)

        if response.status_code == requests.codes.ok:
            with open(self.new_file_name, 'wb') as out:
                out.write(response.content)
        else:
            return False
        return True



class ClickMajic(Remove):
    name = "ClickMajic"
    url = 'https://api.clickmajic.com/v1/remove-background'
    def remove_background(self,file_name,new_file_name):
        self.file_name = file_name
        self.new_file_name = new_file_name
        files = {'sourceFile': open(self.file_name, 'rb')}
        response = requests.post(self.url, files=files, data={**self.headers,**self.data})
        if response.status_code == requests.codes.ok:
            with open(self.new_file_name, 'wb') as out:
                out.write(response.content)
        else:
            return False
        return True






class Picwish(Remove):
    #No
    url = 'https://techhk.aoscdn.com/api/tasks/visual/segmentation'
    def get_header(self):
        return {'X-API-KEY': self.api}
class Cutout(Remove):
    #No maybe
    url = 'https://www.cutout.pro/api/v1/matting'
    def get_header(self):
        return {'APIKEY': self.api}
class Picsart(Remove):
    #No maybe
    url = 'https://api.picsart.io/tools/1.0/removebg'
    def get_header(self):
        return {'X-Picsart-API-Key': self.api}
class ClipPingMagic(Remove):
    #No maybe
    url = 'https://clippingmagic.com/api/v1/images'
    def get_header(self):
        return {'Authorization': self.api}
class RemovalAi(Remove):
    #No maybe
    url = 'https://api.removal.ai/3.0/remove'
    def get_header(self):
        return {'Rm-Token': self.api}




class NoApi(Remove):
    name = "NoApi"
