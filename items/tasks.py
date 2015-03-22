from __future__ import absolute_import

from items.models import ItemImage, ImageGallery

from django.core.files import File
from django.core.files.base import ContentFile
from django.conf import settings

import urllib, json
from io import BytesIO
import base64

from urlparse import urlparse

from selenium import webdriver
from PIL import Image
from celery import shared_task
from bs4 import BeautifulSoup
import requests



@shared_task
def get_twitter_card_image(image_gallery_id, target_url, markup):
    """
    This function will see if there is a Twitter Card image associated
    with the URL. If there is, it'll save it to our media store
    and update our gallery model.
    """
    
    # Get our markup. And parse it. This should be moved to a common function
    soup = BeautifulSoup(markup)
    
    
    # It seems that Twitter images can have a couple of different names
    twitter_image = None
    if soup.find('meta', {"name": "twitter:image"}):
        twitter_image = soup.find('meta', {"name": "twitter:image"})['content']
        
    if soup.find('meta', {"name": "twitter:image:src"}):
        twitter_image = twitter_image = soup.find('meta', {"name": "twitter:image:src"})['content']
    
    # Did we find a twitter image in our markup? If so, let's get it
    if  twitter_image:
        # Get our filename. Isn't there a better way to do this?
        parsed_url = urlparse(twitter_image)
        filename = parsed_url.path.split('/')[-1]
        
        # Add the image to our datastore and update the gallery
        image_content = ContentFile(requests.get(twitter_image, verify=False).content)
        image_gallery = ImageGallery.objects.get(id=image_gallery_id)
        item_image = ItemImage(image_gallery=image_gallery)
        item_image.item_image.save(filename, image_content)
        item_image.save()
        

@shared_task
def get_local_screen_capture(image_gallery_id, target_url, markup): 

    # Get a screen capture of the page

    #TODO: There's likely a Heroku buildpath approach that's better
    exe_path = '{0}/bin/phantomjs'.format(settings.PROJECT_ROOT)
    if settings.DEBUG == False:
        exe_path = '{0}/bin/heroku/phantomjs'.format(settings.PROJECT_ROOT)


    driver = webdriver.PhantomJS(executable_path=exe_path)
    driver.set_window_size(1366, 728) # optional
    driver.get(target_url)


    # Convert it and thumbnail it
    imagedata = driver.get_screenshot_as_base64()
    img = Image.open(BytesIO(base64.b64decode(imagedata)))

    thumb_width = 600

    wpercent = (thumb_width/float(img.size[0]))
    h_size = int((float(img.size[1])*float(wpercent)))
    size = (thumb_width, h_size)
    thumb = img.resize(size, Image.ANTIALIAS)

    thumb = thumb.convert('RGB')
    box = (0, 0, thumb_width, 400)

    cropped = thumb.crop(box)
    thumb_io = BytesIO()
    cropped.save(thumb_io, format='png', option='optimize')


    # Add the image to our datastore and update the gallery
    image_content = ContentFile(thumb_io.getvalue())
    image_gallery = ImageGallery.objects.get(id=image_gallery_id)
    item_image = ItemImage(image_gallery=image_gallery)
    item_image.item_image.save('{0}-thumb.png'.format(item_image.id), image_content)
    item_image.save()
