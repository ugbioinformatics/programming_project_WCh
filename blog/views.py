"""
Main application function definitions
"""

from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.shortcuts import redirect, render, get_object_or_404
from .models import Post
from .forms import Suma, Molecule
import statistics as st
import matplotlib

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


class BlogListView(ListView):
    model = Post
    template_name = "home.html"


class BlogDetailView(DetailView):
    model = Post
    template_name = "post_detail.html"


class BlogDeleteView(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('home')


def calculate_body(bodylist, post):
    """Calculates for data from body"""
    tmp = bodylist.split()
    for i in range(0, len(tmp)):
        tmp[i] = float(tmp[i])

    suma = sum(tmp)
    sr = st.mean(tmp)
    print(sr)

    if len(tmp) > 1:
        odch = st.stdev(tmp)
        var = st.variance(tmp)
    else:
        var = 0
        odch = 0
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
    return (suma, odch, sr, var)


def calculate(dataframe, post):
    """Calculate for data from file"""
    lista = list(dataframe.columns)
    staty = []
    for i in range(len(lista)):
        suma = dataframe[list(dataframe.columns)[i]].sum()
        odch = dataframe[list(dataframe.columns)[i]].std()
        sr = dataframe[list(dataframe.columns)[i]].mean()
        var = dataframe[list(dataframe.columns)[i]].var()
        med = dataframe[list(dataframe.columns)[i]].median()
        shapiro = stats.shapiro(dataframe[list(dataframe.columns)[i]])
        staty.append([suma, odch, sr, var, shapiro])
        if len(lista) > 1:
            for j in range(len(lista) - 1):
                y = dataframe[list(dataframe.columns)[j]]
                x = dataframe[list(dataframe.columns)[j + 1]]
                odch2 = x.std()
                F = odch ** 2 / odch2 ** 2
                a = stats.f.cdf(F, len(y) - 1, len(x) - 2)
                b = 1 - a
                if a >= b:
                    p = 2 * a
                else:
                    p = 2 * b
                    if p > 0.05:
                        t_test = stats.ttest_ind(y, x, axis=0,
                                                 equal_var=True, nan_policy='propagate', alternative='two-sided',
                                                 trim=0)
                    else:
                        t_test = stats.ttest_ind(y, x, axis=0,
                                                 equal_var=False, nan_policy='propagate', alternative='two-sided',
                                                 trim=0)
                    # podać test zgodnosci

                plt.scatter(y, x, c='purple', alpha=0.5)
                plt.xlabel(list(dataframe.columns)[j])
                plt.ylabel(list(dataframe.columns)[j + 1])
                plt.savefig(settings.MEDIA_ROOT + '/' + post.plik_hash + f'/foo_dataframe{j}.png')
                plt.close()

                X = sm.add_constant(y)
                model = sm.OLS(x, X).fit()
                regression = model.summary()
                # dodać regression

                plt.hist(y, color='purple')
                plt.axvline(sr, color='red', label='Średnia')  # średnia pionowa
                plt.axvline(med, color='green', label='Mediana')
                plt.xlabel(list(dataframe.columns)[j])
                plt.ylabel(list(dataframe.columns)[j + 1])
                plt.legend()
                plt.savefig(settings.MEDIA_ROOT + '/' + post.plik_hash + f'/foo_dataframe{j}.png')
                plt.close()

        if len(lista) == 1:
            y = dataframe[list(dataframe.columns)[i]]
            x = np.arange(len(y))
            plt.bar(x, y, color='purple')
            plt.savefig(settings.MEDIA_ROOT + '/' + post.plik_hash + '/foo1.png')
            plt.close()
            print("dataframe w suma")
            print(dataframe)

    corr_matrix = dataframe.corr()
    corr_matrix = dataframe.cov()
    return staty
    # wyświetlić


def edit_suma(request, pk):
    """Editing of existing entries"""
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
                (post.suma, post.odch, post.sr, post.var) = calculate_body(body, post)
            post.save()
            if post.plik1:
                if post.guzik:
                    dataframe = pd.read_csv(post.plik1, delimiter=',', index_col=0)
                else:
                    dataframe = pd.read_csv(post.plik1, delimiter=',')
                post.suma, post.sr, post.odch, post.var = calculate(dataframe, post)
                post.save()
            return redirect('/')
    else:
        data = {'title': post.title, 'body': post.body}
        form = Suma(initial=data)
    return render(request, 'suma.html', {'form': form, 'post': post})


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
                post.save()
                (post.suma, post.odch, post.sr, post.var) = calculate_body(body, post)
                post.save()
            else:
                some_salt = 'some_salt'
                some_psswd = 'somePassword'
                plik_hash = make_password(some_psswd, None, 'md5')
                post = Post(title=title, plik_hash=plik_hash, plik1=plik1)
            post.save()
            if plik1:
                if guzik:
                    dataframe = pd.read_csv(post.plik1, delimiter=',', index_col=0)
                else:
                    dataframe = pd.read_csv(post.plik1, delimiter=',')
                post.suma, post.sr, post.odch, post.var = calculate(dataframe, post)
                post.save()
            return redirect('/')
    else:
        form = Suma()
    return render(request, 'suma.html', {'form': form})


def particleParameters(particle):
    atoms = len(particle.atoms)
    exactmass = particle.exactmass
    formula = particle.formula
    molwt = particle.molwt
    return atoms, exactmass, formula, molwt


def molecule(request):
    if request.method == 'POST':
        form = Molecule(request.POST)
        if form.is_valid():
            smiles = form.cleaned_data["smiles"]
            title = form.cleaned_data["title"]
            some_psswd = 'somePassword'
            plik_hash = make_password(some_psswd, None, 'md5')
            post = Post(smiles=smiles, title=title, plik_hash=plik_hash)
            post.save()
            directory1 = settings.MEDIA_ROOT + '/' + post.plik_hash
            if not os.path.isdir(directory1):
                os.mkdir(directory1)
            czasteczka = openbabel.pybel.readstring("smi", smiles)
            czasteczka.make3D()
            czasteczka.write(format="svg", filename=directory1 + '/ala.svg')
            czasteczka.write(format="_png2", filename=directory1 + '/ala.png')
            # atoms, exactmass, formula, molwt = particleParameters(czasteczka)
            post.atoms, post.exactmass, post.formula, post.molwt = particleParameters(czasteczka)
            post.save()
            return redirect('/')

    else:
        form = Molecule()
    return render(request, 'molecule.html', {'form': form})


def edit_smiles(request, pk):
    """Editing of existing entries"""
    post = get_object_or_404(Post, id=pk)
    if request.method == 'POST':
        form = Molecule(request.POST, request.FILES)
        if form.is_valid():
            post.smiles = form.cleaned_data["smiles"]
            post.title = form.cleaned_data["title"]
            post.save()
            directory1 = settings.MEDIA_ROOT + '/' + post.plik_hash
            czasteczka = openbabel.pybel.readstring("smi", post.smiles)
            czasteczka.make3D()
            czasteczka.write(format="svg", filename=directory1 + '/ala.svg', overwrite=True)
            czasteczka.write(format="_png2", filename=directory1 + '/ala.png', overwrite=True)
            post.atoms, post.exactmass, post.formula, post.molwt = particleParameters(czasteczka)
            post.save()
            return redirect('/')
    else:
        data = {'title': post.title, 'smiles': post.smiles}
        form = Molecule(initial=data)
    return render(request, 'molecule.html', {'form': form, 'post': post})
