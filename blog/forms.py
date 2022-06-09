from django import forms
from .models import Post
import pandas as pd
import numpy as np
import io
from pandas.errors import EmptyDataError
import openbabel.pybel


class Suma(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'size': 40, 'maxlenght': 40}))
    body = forms.CharField(widget=forms.Textarea(attrs={'cols': 20, 'rows': 20}), required=False)
    plik1 = forms.FileField(label='Upload data', required=False,
                            help_text='Input data for calculation in csv format. Please note that headers for columns are essential for correct data analysis!')
    guzik = forms.BooleanField(required=False, label='Do you have headers in rows?')

    def clean(self):
        cleaned_data = super(Suma, self).clean()
        body = cleaned_data.get("body")
        plik1 = cleaned_data.get('plik1')
        guzik = cleaned_data.get('guzik')

        if body and plik1:
            show = 'Choose only one form of data (text field OR data file).'
            self.add_error('body', show)

        if not body and not plik1:
            msg = 'Provide either data in the text field or appropriate data file.'
            self.add_error('body', msg)

        if body:
            tmp = body.split()
            s = 0
            for item in tmp:
                try:
                    s = s + float(item)
                except:
                    self.add_error('body', 'Wrong list')
        if plik1:
            try:
                if guzik:
                    dataframe = pd.read_csv(io.StringIO(plik1.read().decode('utf-8')), delimiter=',', index_col=0)
                else:
                    dataframe = pd.read_csv(io.StringIO(plik1.read().decode('utf-8')), delimiter=',')

                # Check if data in dataframe is numerical
                for column in list(dataframe.columns):
                    for item in np.array(dataframe[column]):
                        try:
                            float(item)
                        except ValueError:
                            self.add_error('plik1', 'The file contains non-numerical data')
                            break
                    break
                try:
                    suma = dataframe[list(dataframe.columns)[0]].sum()
                except:
                    self.add_error('plik1', 'The file contains wrong data')
                # Debugging
                print(dataframe)
                print(dataframe.sum())
                print(dataframe.std())
                print(dataframe.mean())
                print(dataframe.var())
            except UnicodeDecodeError:
                self.add_error('plik1', 'The file contains Non-Unicode data')
            except EmptyDataError:
                self.add_error('plik1', 'The file contains Data that is wrong or empty.')

class Molecule(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'size': 40, 'maxlenght': 40}))
    smiles = forms.CharField(widget=forms.TextInput(attrs={'size': 40, 'maxlenght': 200}), label='SMILES')
    def clean(self):
        cleaned_data = super(Molecule, self).clean()
        smiles = cleaned_data.get('smiles')
        try:
            particle = openbabel.pybel.readstring("smi", smiles)
        except IOError:
            self.add_error("smiles",'The SMILES have unsupported characters.')



