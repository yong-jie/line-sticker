import requests
import cssutils
import urllib.request
from bs4 import BeautifulSoup
from wand.image import Image
import sys
import os

def execute():
    # If the "downloads" folder doesn't exist, create it.
    directory = os.path.dirname("downloads/")
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    # Check that the link is valid.
    if len(sys.argv) < 2:
        print("Please state the sticker url.")
        return
    sticker_url = sys.argv[1]
    request     = requests.get(sticker_url)
    if request.status_code != 200:
        print("Error: Invalid request status code received.")
        return

    # Parse request, download images and resize them.
    parsed_request = BeautifulSoup(request.text, "html.parser")
    images = parsed_request.find_all('span', attrs={"style": not ""})
    index = 0
    for image in images:
        index += 1
        image_url, response = craft_image_url(image)
        resize_and_save_sticker(response, image_url, index)
        
def craft_image_url(image):
    image_url = image["style"]
    image_url = cssutils.parseStyle(image_url)
    image_url = image_url["background-image"]
    image_url = image_url.replace("url(", "").replace(")", "")
    image_url = image_url[1:-15]
    response  = urllib.request.urlopen(image_url)
    return image_url, response

def resize_and_save_sticker(image, filename, index):
    filen = filename[-7:3] + str(index)+ filename[-4:]
    with Image(file=image) as img:
        ratio = 1
        if img.width > img.height:
            ratio = 512.0/img.width
        else:
            ratio = 512.0/img.height
        img.resize(int(img.width*ratio),
                   int(img.height*ratio),
                   'mitchell')
        img.save(filename=("downloads/" + filen))

if __name__ == "__main__":
    execute()
