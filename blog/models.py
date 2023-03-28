from django.db import models

# Create your models here.
from django.db import models
from django.urls import reverse

from django.contrib.auth.models import User


# ustawienie katalogu "instance.plik" przesyłania plików przez użytkownika strony i nazwy pliku 'plik.dane' - utworzenie lokalizacji
# w lokalnym systemie plików, w której będą przechowywane przesłane pliki

def user_directory_path(instance, filename):
    """
    Returns path for file saving MEDIA_ROOT/<hash>/plik.pdb
    :returns UNIX path str
    """
    return '{0}/{1}'.format(instance.plik_hash, 'plik.dane')


# lista pól bazy danych, które definiuje model, zawierający podstawowe pola i zachowania przechowywania danych np."models.CharField"
# pole używane jako atrybut do odwoływania się do kolumny bazy danych - wymaga podania maksymalnej długości
class Post(models.Model):
    title = models.CharField(max_length=40)
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True,
                               null=True)  # definiujemy autora jako odnośnik do bazy użytkowników w django (User)
    body = models.TextField()
    smiles = models.CharField(max_length=200, null=True)
    suma = models.TextField(default='')
    odch = models.TextField(default='')
    sr = models.TextField(default='')
    var = models.TextField(default='')
    med = models.TextField(default='')
    shapiro = models.TextField(default='')
    test = models.TextField(default='')
    test_json = models.JSONField(default='')
    plik_hash = models.CharField(blank=True, null=True, max_length=256)
    plik1 = models.FileField(default='', upload_to=user_directory_path)
    guzik = models.BooleanField(default=False)
    ncolumns = models.IntegerField(default=0)

    atoms = models.IntegerField(blank=True, null=True)
    exactmass = models.FloatField(blank=True, null=True)
    formula = models.CharField(max_length=200, default='')
    molwt = models.FloatField(blank=True, null=True)
    sequence = models.TextField(default='') 
    charge = models.FloatField(blank=True, null=True) 
    pKscale = models.CharField(max_length=200,default='')
    fasgai_vector = models.ForeignKey('FasgaiVector', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.title

    # gdy metoda jest wywoływana, zwraca łącze zwrotne do adresu URL pod adresem "post_detail", co spowoduje przekazanie dodatkowych argumentów
    # do adresu URL, w tym przypadku pk. Zostanie to skonfigurowane w urls.py.

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})

    def delete(self, using=None, keep_parents=False):
        self.fasgai_vector.delete()
        super(Post, self).delete(using, keep_parents)


class FasgaiVector(models.Model):
    f1 = models.FloatField()
    f2 = models.FloatField()
    f3 = models.FloatField()
    f4 = models.FloatField()
    f5 = models.FloatField()
    f6 = models.FloatField()

    def __str__(self):
        return f'FasgaiVector({self.f1}, {self.f2}, {self.f3}, {self.f4}, {self.f5}, {self.f6})'

    def get_absolute_url(self):
        return reverse('fasgai_vector_detail', kwargs={'pk': self.pk})

    def create_from_tuple(self, tuple):
        self.f1 = tuple[0]
        self.f2 = tuple[1]
        self.f3 = tuple[2]
        self.f4 = tuple[3]
        self.f5 = tuple[4]
        self.f6 = tuple[5]
        self.save()
        return self

    def to_tuple(self):
        return self.f1, self.f2, self.f3, self.f4, self.f5, self.f6

    def to_list(self):
        return [self.f1, self.f2, self.f3, self.f4, self.f5, self.f6]
