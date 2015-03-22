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
def get_screen_capture(image_gallery_id, target_url, markup):
    """
    This function will get a screen capture of the page from our
    preview service. Then, it'll save it to our media store
    and update our gallery model.
    """
    preview_url = 'http://hlslwebtest.law.harvard.edu/preview/create?thumb=400px*300px&url=%s' % urllib.quote(target_url)
    response = requests.get(preview_url, verify=False).text
    serialized_response = json.loads(response)

    preview_url_image = 'http://hlslwebtest.law.harvard.edu%s' % serialized_response['thumb_url']

    # Get our filename. Isn't there a better way to do this?
    parsed_url = urlparse(preview_url_image)
    filename = parsed_url.path.split('/')[-1]

    # Add the image to our datastore and update the gallery
    image_content = ContentFile(requests.get(preview_url_image, verify=False).content)
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
    img = img.convert('RGB')
    box = (0, 0, 1366, 728)
    cropped = img.crop(box)
    thumb_io = BytesIO()
    cropped.save(thumb_io, format='png', option='optimize')


    # Add the image to our datastore and update the gallery
    image_content = ContentFile(thumb_io.getvalue())
    image_gallery = ImageGallery.objects.get(id=image_gallery_id)
    item_image = ItemImage(image_gallery=image_gallery)
    item_image.item_image.save('screen_lores.png', image_content)
    item_image.save()
