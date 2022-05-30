"""
Main application function definitions
"""

from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import redirect, render, get_object_or_404
from .models import Post
from .forms import Suma
import statistics as st
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import io
from django.contrib.auth.hashers import make_password
from django.conf import settings
import os


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
    suma = dataframe[list(dataframe.columns)[0]].sum()
    odch = dataframe[list(dataframe.columns)[0]].std()
    sr = dataframe[list(dataframe.columns)[0]].mean()
    var = dataframe[list(dataframe.columns)[0]].var()
    y = dataframe[list(dataframe.columns)[0]]
    x = np.arange(len(y))
    plt.bar(x, y)
    plt.savefig(settings.MEDIA_ROOT + '/' + post.plik_hash + '/foo1.png')
    plt.close()
    print("dataframe w suma")
    print(dataframe)
    return suma, odch, sr, var


def edit_blog(request, pk):
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
                #               post = Post(title=title)
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
