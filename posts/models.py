from django.db import models
from PIL import Image
import os
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
# from django.utils.text import slugify

# Create your models here.


class Post(models.Model):
    # Each post that the database will store
    # need to change max length property later
    title = models.CharField(max_length=10)
    # postspics
    photo = models.ImageField(upload_to='post_pics')
    # alttext need to change max length property later
    alt_text = models.TextField(max_length=20,default='Please describe some text that accurately represents the image!')
    # add param check date was posted
    date_posted = models.DateTimeField(default=timezone.now)
    # author of post
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # add param check date was updated
    last_updated_by = models.ForeignKey(User, on_delete=models.SET_NULL,related_name='last_updated_posts',null = True,blank = True)

    approved = models.BooleanField(default=False)

    # need to resize our posts need to override save method as well as use PILLOW
    # documented more in sample blog app folder
    def save(self,*args,**kwargs):
        request = kwargs.pop('request',None)
        if self.pk:
            try:
                post = Post.objects.get(pk=self.pk)
                self.last_updated_by = post.last_updated_by
            except Post.DoesNotExist:
                pass
        super().save(*args,**kwargs)
        img = Image.open(self.photo.path)
        # we will change the numbers later
        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.photo.path)
        if request:
            self.last_updated_by = request.user
            super().save(*args,**kwargs)
      
    # how we display our posts in db using our title
    def __str__(self):
        return self.title
    # find url to any specific post
    def get_absolute_url(self):
        return reverse('post-detail',kwargs= {'pk' : self.pk})
    
    # add permissions so that anyone logged in can edit post
    class Meta:
        permissions = (
            ('can_edit_post','Can edit post'),
        )
