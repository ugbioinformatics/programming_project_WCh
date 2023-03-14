from django.db import models

# Create your models here.
from django.db import models
from django.urls import reverse


#ustawienie katalogu "instance.plik" przesyłania plików przez użytkownika strony i nazwy pliku 'plik.dane' - utworzenie lokalizacji 
#w lokalnym systemie plików, w której będą przechowywane przesłane pliki

def user_directory_path(instance, filename):
    """
    Returns path for file saving MEDIA_ROOT/<hash>/plik.pdb
    :returns UNIX path str
    """
    return '{0}/{1}'.format(instance.plik_hash, 'plik.dane')


#lista pól bazy danych, które definiuje model, zawierający podstawowe pola i zachowania przechowywania danych np."models.CharField" 
#pole używane jako atrybut do odwoływania się do kolumny bazy danych - wymaga podania maksymalnej długości
class Post(models.Model):
    title = models.CharField(max_length=40)
    author = models.CharField(max_length=20)
    body = models.TextField()
    smiles = models.CharField(max_length=200, null=True)
    suma = models.TextField(default='')
    odch = models.TextField(default='')
    sr = models.TextField(default='')
    var = models.TextField(default='')
    med = models.TextField(default='')
    shapiro = models.TextField(default='')
    test = models.TextField(default='')
    plik_hash = models.CharField(blank=True, null=True, max_length=256)
    plik1 = models.FileField(default='', upload_to=user_directory_path)
    guzik = models.BooleanField(default=False)
    ncolumns = models.IntegerField(default=0)
    
    atoms = models.IntegerField(blank=True, null=True)
    exactmass = models.FloatField(blank=True, null=True)
    formula = models.CharField(max_length=200,default='')
    molwt = models.FloatField(blank=True, null=True)
    

    def __str__(self):
        return self.title
    #gdy metoda jest wywoływana, zwraca łącze zwrotne do adresu URL pod adresem "post_detail", co spowoduje przekazanie dodatkowych argumentów 
    #do adresu URL, w tym przypadku pk. Zostanie to skonfigurowane w urls.py.

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})
