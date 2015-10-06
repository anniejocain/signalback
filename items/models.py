from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.conf import settings
from django.db import models

import uuid


class Organization(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length=400)
    slug = models.SlugField(unique=True)
    public_link = models.URLField(max_length=2000, null=True, blank=True)
    public_email = models.EmailField(max_length=254, null=True, blank=True)
    
    def __unicode__(self):
        return self.name
        

class BookmarkletKey(models.Model):
    organization = models.ForeignKey(Organization)
    key = models.CharField(max_length=255, null=False, blank=False, primary_key=True)
    is_active = models.BooleanField(default=True)
    email = models.EmailField(max_length=254, null=True, blank=True)
    display_name = models.CharField(max_length=400, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        """
        We need a unique key for each bookmarklet. Let's create that key
        when we create a new bookmarklet entry in the DB
        """

        if not self.key:
            generated_key = uuid.uuid4()
            self.key = str(generated_key)
            super(BookmarkletKey, self).save(*args, **kwargs)
            
    def __unicode__(self):
        return self.key
    

class SBUserManager(BaseUserManager):
    def create_user(self, email, date_joined, first_name, last_name, confirmation_code, password=None):
        """
        Creates and saves a User with the given email, registrar and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            date_joined = date_joined,
            first_name = first_name,
            last_name = last_name,
            authorized_by = authorized_by,
            confirmation_code = confirmation_code
        )

        user.set_password(password)
        user.save()

        return user


class SBUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        db_index=True,
    )
    is_active = models.BooleanField(default=True)
    is_confirmed = models.BooleanField(default=False)
    date_joined = models.DateField(auto_now_add=True)
    first_name = models.CharField(max_length=45, blank=True)
    last_name = models.CharField(max_length=45, blank=True)
    confirmation_code = models.CharField(max_length=45, blank=True)

    objects = SBUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'User'

    
class Item(models.Model):
    bookmarklet_key = models.ForeignKey(BookmarkletKey)
    title = models.CharField(max_length=400)
    description = models.CharField(max_length=117, null=True, blank=True)
    link = models.URLField(max_length=2000, null=True, blank=True)
    contributor = models.CharField(max_length=400, null=True, blank=True)
    contributed_date = models.DateTimeField(auto_now=True)
        
    def __unicode__(self):
        return self.title

class ImageGallery(models.Model):
    """
    When a user creates a new item we grab a number of images for them
    and present them in an image gallery. Those images are tracked in
    ItemImage. We use this model to group them together. The images
    that aren't selected by the user will be deleted, as will the 
    ImageGallery instance.
    """
    created_date = models.DateTimeField(auto_now=True)
    

class ItemImage(models.Model):
    """
    We want to associate an image with an item. We track that image here.
    """
    item = models.ForeignKey(Item, null=True, blank=True)
    image_gallery = models.ForeignKey(ImageGallery, null=True, blank=True)
    item_image = models.ImageField(upload_to='item_images')