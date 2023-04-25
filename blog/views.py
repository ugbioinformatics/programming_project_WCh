# import bibliotek i klas potrzebnych do działania programu
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.shortcuts import redirect, render, get_object_or_404
from pypdb import Query, pypdb
from pypdb.clients.pdb.pdb_client import get_pdb_file

from .models import Post, FasgaiVector
from .forms import Suma, Molecule, Peptide_form, Database_form
import statistics as st
import matplotlib
import requests
import json

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from django.contrib.auth.hashers import make_password
from django.conf import settings
import os
import openbabel.pybel
import scipy.stats as stats
import statsmodels.api as sm
import peptides


# zdefiniowanie funkcjonowania strony głównej post/
class BlogListView(ListView):
    model = Post
    template_name = "home.html"

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        if self.request.user.is_authenticated:
            qs.filter(author=self.request.user)
        else:
            qs.filter(author=None)

        if self.request.GET.get('type') == 'data':
            return qs.filter(type='data')
        elif self.request.GET.get('type') == 'molecule':
            return qs.filter(type='molecule')
        elif self.request.GET.get('type') == 'peptide':
            return qs.filter(type='peptide')
        else:
            return qs


# zdefiniowanie wyświetlania podstrony post/<int:pk>/
class BlogDetailView(DetailView):
    model = Post
    template_name = "post_detail.html"


# zdefinowanie wyświetlania strony po usunięciu elementu
class BlogDeleteView(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('home')


# pomocnicza funkcja, obliczająca sumę, średnią, odchylenie, wariancję i tworząca wykres słupkowy z danych podanych przez użytkownika w formularzu
def calculate_body(bodylist, post):
    tmp = bodylist.split()
    for i in range(0, len(tmp)):
        tmp[i] = float(tmp[i])

    suma = sum(tmp)
    sr = st.mean(tmp)
    mediana = st.median(tmp)
    print(sr)

    if len(tmp) > 1:
        odch = st.stdev(tmp)
        var = st.variance(tmp)
        t, p = stats.shapiro(tmp)
    else:
        var = 0
        odch = 0
        t = 0
        p = [0]
    y = tmp
    x = np.arange(len(y))
    plt.bar(x, y)
    directory1 = settings.MEDIA_ROOT + '/' + post.plik_hash

    print("dir")
    print(directory1)
    if not os.path.isdir(directory1):
        os.mkdir(directory1)

    plt.savefig(directory1 + '/foo1.png')
    plt.close()
    return (suma, odch, sr, var, mediana, t, p)


# pomocnicza funkcja, obliczająca sumę, średnią, odchylenie, wariancję, medianę, wartość p i watość testową testu Shapiro-Wilka oraz testu t-Studenta i tworząca wykres słupkowy z danych z pliku

def calculate(dataframe, post):
    """Calculate for data from file"""
    lista = list(dataframe.columns)
    staty = [[], [], [], [], [], [], [], ]
    for i in range(len(lista)):
        suma = dataframe[list(dataframe.columns)[i]].sum()
        odch = dataframe[list(dataframe.columns)[i]].std()
        sr = dataframe[list(dataframe.columns)[i]].mean()
        var = dataframe[list(dataframe.columns)[i]].var()
        med = dataframe[list(dataframe.columns)[i]].median()
        try:
            t, p = stats.shapiro(dataframe[list(dataframe.columns)[i]])
            shapiro = p
        except:
            shapiro = ''

        if len(lista) > 1 and i < len(lista) - 1:

            y = dataframe[list(dataframe.columns)[i]]
            x = dataframe[list(dataframe.columns)[i + 1]]
            odch2 = x.std()
            F = odch ** 2 / odch2 ** 2
            a = stats.f.cdf(F, len(y) - 1, len(x) - 2)
            b = 1 - a
            if a >= b:
                p = 2 * a
            else:
                p = 2 * b

            if p > 0.05:
                tt, pp = stats.ttest_ind(y, x, axis=0,
                                         equal_var=True, nan_policy='propagate', alternative='two-sided',
                                         trim=0)
                test = pp

            else:
                tt, pp = stats.ttest_ind(y, x, axis=0,
                                         equal_var=False, nan_policy='propagate', alternative='two-sided',
                                         trim=0)
                test = pp
            # podać test zgodnosci

            plt.scatter(y, x, c='purple', alpha=0.5)
            plt.xlabel(list(dataframe.columns)[i])
            plt.ylabel(list(dataframe.columns)[i + 1])
            plt.savefig(settings.MEDIA_ROOT + '/' + post.plik_hash + f'/foo_dataframe{i + 1}_scatter.png')
            plt.close()


        else:
            test = ''

        for x, y in zip(staty, [suma, odch, sr, var, med, shapiro, test]):
            if y == '':
                x.append(y)
            else:
                x.append(round(y, 3))

        if len(lista) == 1:
            y = dataframe[list(dataframe.columns)[i]]
            x = np.arange(len(y))
            plt.bar(x, y, color='purple')
            plt.savefig(settings.MEDIA_ROOT + '/' + post.plik_hash + '/foo1.png')
            plt.close()
            print("dataframe w suma")
            print(dataframe)

    for j in range(len(lista)):
        sr = dataframe[list(dataframe.columns)[j]].mean()
        med = dataframe[list(dataframe.columns)[j]].median()
        y = dataframe[list(dataframe.columns)[j]]
        plt.hist(y, color='purple')
        plt.axvline(sr, color='red', label='Średnia')  # średnia pionowa
        plt.axvline(med, color='green', label='Mediana')
        plt.xlabel(list(dataframe.columns)[j])
        plt.ylabel("Częstość")
        plt.legend()
        plt.savefig(settings.MEDIA_ROOT + '/' + post.plik_hash + f'/foo_dataframe{j + 1}_hist.png')
        plt.close()

    return staty


# wyświetlić do zrobienia!

# edycja danych (w bazie danych) które wprowadził użytkownik 

def edit_suma(request, pk):
    post = get_object_or_404(Post, id=pk)
    if request.method == 'POST':
        form = Suma(request.POST, request.FILES)
        if form.is_valid():
            body = form.cleaned_data["body"]
            post.body = body
            post.title = form.cleaned_data["title"]
            post.plik1 = form.cleaned_data["plik1"]
            post.guzik = form.cleaned_data['guzik']
            if post.body:
                (post.suma, post.odch, post.sr, post.var, post.med, post.shapiro, post.test) = calculate_body(body,
                                                                                                              post)
            post.save()
            if post.plik1:
                if post.guzik:
                    dataframe = pd.read_csv(post.plik1, delimiter=',', index_col=0)
                else:
                    dataframe = pd.read_csv(post.plik1, delimiter=',')
                post.ncolumns = len(list(dataframe.columns))
                (post.suma, post.odch, post.sr, post.var, post.med, post.shapiro, post.test_json) = calculate(dataframe,
                                                                                                              post)
                post.test = post.test_json
                post.save()
            return redirect('/post')
    else:
        data = {'title': post.title, 'body': post.body}
        form = Suma(initial=data)
    return render(request, 'suma.html', {'form': form, 'post': post})


# tworzy nazwę pliku

def suma(request):
    if request.method == 'POST':
        form = Suma(request.POST, request.FILES)
        if form.is_valid():
            body = form.cleaned_data["body"]
            title = form.cleaned_data["title"]
            plik1 = form.cleaned_data["plik1"]
            guzik = form.cleaned_data['guzik']
            author = "test"
            if body:
                some_psswd = 'somePassword'
                plik_hash = make_password(some_psswd, None, 'md5')
                post = Post(body=body, title=title, plik_hash=plik_hash)
                post.type = 'data'
                post.save()
                (post.suma, post.odch, post.sr, post.var, post.med, post.shapiro, post.test) = calculate_body(body,
                                                                                                              post)
                post.save()
            else:
                some_psswd = 'somePassword'
                plik_hash = make_password(some_psswd, None, 'md5')
                post = Post(title=title, plik_hash=plik_hash, plik1=plik1)
            if request.user.is_authenticated:
                post.author = request.user
            post.save()
            if plik1:
                if guzik:
                    dataframe = pd.read_csv(post.plik1, delimiter=',', index_col=0)
                else:
                    dataframe = pd.read_csv(post.plik1, delimiter=',')
                post.ncolumns = len(list(dataframe.columns))
                post.suma, post.sr, post.odch, post.var, post.med, post.shapiro, post.test_json = calculate(dataframe,
                                                                                                            post)
                post.test = post.test_json
                post.save()
            return redirect('/post')
    else:
        form = Suma()
    return render(request, 'suma.html', {'form': form})


# funkcja pomocnicza, oblicza ilość atomów w czasteczce, dokładną masę cząsteczki, masę molową cząsteczki, wzór sumaryczny cząsteczki

def particleParameters(particle):
    atoms = len(particle.atoms)
    exactmass = particle.exactmass
    formula = particle.formula
    molwt = particle.molwt
    return atoms, exactmass, formula, molwt


# na podstawie SMILES oblicza i wpisuje strukturę 3D cząsteczki do bazy danych, wpisuje parametry obliczone przez funkcję particleParameters

def molecule(request):
    if request.method == 'POST':
        form = Molecule(request.POST)
        if form.is_valid():
            smiles = form.cleaned_data["smiles"]
            title = form.cleaned_data["title"]
            some_psswd = 'somePassword'
            plik_hash = make_password(some_psswd, None, 'md5')
            if request.user.is_authenticated:
                post = Post(type='molecule', smiles=smiles, title=title, plik_hash=plik_hash, author=request.user)
            else:
                post = Post(type='molecule', smiles=smiles, title=title, plik_hash=plik_hash)
            post.save()
            directory1 = settings.MEDIA_ROOT + '/' + post.plik_hash
            if not os.path.isdir(directory1):
                os.mkdir(directory1)
            czasteczka = openbabel.pybel.readstring("smi", smiles)
            czasteczka.make3D()
            czasteczka.write(format="mol2", filename=directory1 + '/ala.mol2')
            czasteczka.write(format="svg", filename=directory1 + '/ala.svg')
            czasteczka.write(format="_png2", filename=directory1 + '/ala.png')
            post.atoms, post.exactmass, post.formula, post.molwt = particleParameters(czasteczka)
            post.save()
            return redirect('/post')

    else:
        form = Molecule()
    return render(request, 'molecule.html', {'form': form})


# edycja istniejącego modelu cząsteczki w bazie danych

def edit_smiles(request, pk):
    post = get_object_or_404(Post, id=pk)
    if request.method == 'POST':
        form = Molecule(request.POST, request.FILES)
        if form.is_valid():
            post.smiles = form.cleaned_data["smiles"]
            post.title = form.cleaned_data["title"]
            post.type = 'molecule'
            post.save()
            directory1 = settings.MEDIA_ROOT + '/' + post.plik_hash
            czasteczka = openbabel.pybel.readstring("smi", post.smiles)
            czasteczka.make3D()
            czasteczka.write(format="mol2", filename=directory1 + '/ala.mol2', overwrite=True)
            czasteczka.write(format="svg", filename=directory1 + '/ala.svg', overwrite=True)
            czasteczka.write(format="_png2", filename=directory1 + '/ala.png', overwrite=True)
            post.atoms, post.exactmass, post.formula, post.molwt = particleParameters(czasteczka)
            post.save()
            return redirect('/post?rnd=323')
    else:
        data = {'title': post.title, 'smiles': post.smiles}
        form = Molecule(initial=data)
    return render(request, 'molecule.html', {'form': form, 'post': post})


# funkcja z peptide
def peptide(request):
    if request.method == 'POST':
        form = Peptide_form(request.POST)
        if form.is_valid():
            sequence = form.cleaned_data["sequence"]
            title = form.cleaned_data["title"]
            pKscale = form.cleaned_data["pKscale"]
            if request.user.is_authenticated:
                post = Post(sequence=sequence, title=title, author=request.user)
            else:
                post = Post(sequence=sequence, title=title)
            p = peptides.Peptide(sequence)
            post.molwt = p.molecular_weight()
            post.charge = p.charge(pKscale=pKscale)
            post.pKscale = pKscale
            post.type = 'peptide'
            fs_vector = p.fasgai_vectors()
            fs_vector_instance = FasgaiVector().create_from_tuple(fs_vector)
            fs_vector_instance.save()
            post.fasgai_vector = fs_vector_instance
            post.save()
            return redirect('/post')

    else:
        form = Peptide_form()
    return render(request, 'peptide.html', {'form': form})


def edit_peptide(request, pk):
    post = get_object_or_404(Post, id=pk)
    if request.method == 'POST':
        form = Peptide_form(request.POST)
        if form.is_valid():
            post.sequence = form.cleaned_data["sequence"]
            post.title = form.cleaned_data["title"]
            post.pKscale = form.cleaned_data["pKscale"]
            p = peptides.Peptide(post.sequence)
            post.molwt = p.molecular_weight()
            post.charge = p.charge(pKscale=post.pKscale)
            if not post.fasgai_vector:
                fs_vector = FasgaiVector().create_from_tuple(p.fasgai_vectors())
                post.fasgai_vector = fs_vector
                post.save()
            else:
                fs_vector = post.fasgai_vector
                fs_vector.create_from_tuple(p.fasgai_vectors())
                fs_vector.save()
            post.save()
            return redirect('/post')

    else:
        data = {'title': post.title, 'sequence': post.sequence, 'pKscale': post.pKscale}
        form = Peptide_form(initial=data)
    return render(request, 'peptide.html', {'form': form})


def search_pdb(request, query_text, query_size, form):
    results = Query(query_text).search()
    if len(results) == 0:
        return render(request, 'database.html', {'form': form, 'error': 'No results found'})
    info = []
    for result in results[:query_size]:
        pdb_file = get_pdb_file(result)
        if pdb_file:
            header = pdb_file.split('\n')[0]
            info.append([header, result])
    return render(request, 'zapytanie.html', {'results': results[:query_size], 'info': info})

def zapytanie(request):
    if request.method == 'POST':
         for ele in request.POST:
             if ele != 'csrfmiddlewaretoken':
               id=request.POST['ele']
               if request.user.is_authenticated:
                  post = Post(database_id=id, database_choice='PDB', title='query', author=request.user)
               else:
                  post = Post(database_id=id, database_choice='PDB', title='query')
               post.type = 'database'
               URL = f'https://files.rcsb.org/download/{ele}.pdb'
               response = requests.get(URL)
               post.plik_hash = make_password('something', None, 'md5')
               directory1 = settings.MEDIA_ROOT + '/' + post.plik_hash
               if not os.path.isdir(directory1):
                    os.mkdir(directory1)
               post.sequence = PDB_sequence(response.text)
               open(f'{directory1}/{id}.pdb', "wb").write(response.content)
               post.save()
         return redirect('/post')
                
       

def database(request):
    if request.method == 'POST':
        form = Database_form(request.POST)
        if form.is_valid():
            database_id = form.cleaned_data["id"]
            choice = form.cleaned_data["database"]
            title = form.cleaned_data["title"]
            query_text = form.cleaned_data["tekst"]
            query_size = form.cleaned_data["liczba_elementow"]

            if choice == 'Uniprot' and query_text:
                pass
            if choice == 'PDB' and query_text:
                return search_pdb(request, query_text, query_size, form)

            if request.user.is_authenticated:
                post = Post(database_id=database_id, database_choice=choice, title=title, author=request.user)
            else:
                post = Post(database_id=database_id, database_choice=choice, title=title)
            post.type = 'database'
            if choice == 'Uniprot':
                uniprotfasta = getfromuniprot(database_id)
                uniprotjson = getjsonfromuniprot(database_id)
                post.database_text = uniprotfasta
                post.organism = uniprotjson['organism']['commonName']
                post.proteinname = uniprotjson['proteinDescription']['recommendedName']['fullName']['value']
                post.sequence = uniprotjson['sequence']['value']
                p = peptides.Peptide(post.sequence)
                post.molwt = p.molecular_weight()
            elif choice == 'PDB':
                query_text = form.cleaned_data["tekst"]
                URL = f'https://files.rcsb.org/download/{database_id}.pdb'
                response = requests.get(URL)
                post.plik_hash = make_password('something', None, 'md5')
                directory1 = settings.MEDIA_ROOT + '/' + post.plik_hash
                if not os.path.isdir(directory1):
                    os.mkdir(directory1)
                post.sequence = PDB_sequence(response.text)
                open(f'{directory1}/{database_id}.pdb', "wb").write(response.content)

            post.save()
            return redirect('/post')

    else:
        form = Database_form()
    return render(request, 'database.html', {'form': form})


def PDB_sequence(pdb_data):
    seq = []

    for line in pdb_data.split('\n'):
        if line.startswith('SEQRES'):
            seq.extend(
                line[19:].split()
            )

    seq = '-'.join(seq)

    return getSequence(seq)


def getSequence(sequence_long):
    sequence = ''
    symbol = {
        "ALA": "A", "CYS": "C", "ASP": "D", "GLU": "E", "PHE": "F", "GLY": "G", "HIS": "H", "ILE": "I",
        "LYS": "K", "LEU": "L", "MET": "M", "ASN": "N", "PRO": "P", "GLN": "Q", "ARG": "R", "SER": "S",
        "THR": "T", "TRP": "W", "VAL": "V", "TYR": "Y"
    }
    for aa in sequence_long.split('-'):
        try:
            sequence += symbol[aa]
        except KeyError:
            sequence += "X"

    return sequence


def getfromuniprot(id):
    url = f'https://rest.uniprot.org/uniprotkb/{id}.fasta'
    resp = requests.get(url)

    if resp.ok:
        return resp.text


def getjsonfromuniprot(id):
    url = f'https://rest.uniprot.org/uniprotkb/{id}'
    resp = requests.get(url).json()
    return resp
