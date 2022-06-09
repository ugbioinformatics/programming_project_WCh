from django.db import models

# Create your models here.
from django.db import models
from django.urls import reverse


def user_directory_path(instance, filename):
    """
    Returns path for file saving MEDIA_ROOT/<hash>/plik.pdb
    :returns UNIX path str
    """
    return '{0}/{1}'.format(instance.plik_hash, 'plik.dane')


class Post(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=20)
    body = models.TextField()
    smiles = models.CharField(max_length=200, null=True)
    suma = models.FloatField(blank=True, null=True)
    odch = models.FloatField(blank=True, null=True)
    sr = models.FloatField(blank=True, null=True)
    var = models.FloatField(blank=True, null=True)
    plik_hash = models.CharField(blank=True, null=True, max_length=256)
    plik1 = models.FileField(default='', upload_to=user_directory_path)
    guzik = models.BooleanField(default=False)
    ncolumns = models.IntegerField(default=0)
    
    atoms = models.IntegerField(blank=True, null=True)
    exactmass = models.FloatField(blank=True, null=True)
    formula = models.CharField(max_length=200)
    molwt = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})
