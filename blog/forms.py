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
    '''
Klasa Suma służy do tworzenia formularza internetowego, który ma służyć do pobierania danych od użytkownika.

W klasie Suma definiowane są cztery pola formularza, każde z innym typem widżetu (CharField, Textarea, FileField oraz BooleanField).

    "title" - pole typu CharField, służy do pobierania tekstu (tytułu) od użytkownika. Atrybut widget służy do zmiany wyglądu pola i w tym przypadku ustawia się na TextInput z atrybutami size (rozmiar) i maxlength (maksymalna długość).
    "body" - pole typu CharField, służy do pobierania większej ilości tekstu (treści). Atrybut widget jest ustawiony na Textarea z atrybutami cols (liczba kolumn) i rows (liczba wierszy).
    "plik1" - pole typu FileField, służy do pobierania pliku od użytkownika. Atrybut label określa etykietę pola, która będzie widoczna dla użytkownika. Atrybut help_text zawiera informacje dla użytkownika, które będą wyświetlane pod polem.
    "guzik" - pole typu BooleanField, służy do pobierania wartości typu logicznego (prawda/fałsz) od użytkownika. Atrybut label określa etykietę pola, która będzie widoczna dla użytkownika.
    
Wszystkie pola są opcjonalne, ponieważ mają ustawioną wartość required=False.
    '''

    def clean(self):
        cleaned_data = super(Suma, self).clean()
        body = cleaned_data.get("body")
        plik1 = cleaned_data.get('plik1')
        guzik = cleaned_data.get('guzik')
        '''
        Metoda 'clean()' w klasie 'Suma', która dziedziczy po klasie 'forms.Form' z modułu Django 'django.forms', jest wywoływana po przesłaniu formularza przez użytkownika i służy do weryfikacji i walidacji danych wprowadzonych przez użytkownika.
        W metodzie clean() najpierw wywoływana jest metoda clean() z klasy nadrzędnej za pomocą wyrażenia super(Suma, self).clean(). W ten sposób otrzymujemy czyste dane z formularza. Następnie zmiennym body, plik1 i guzik przypisujemy wartości wprowadzone przez użytkownika dla odpowiednich pól.
        '''

        if body and plik1:
            show = 'Choose only one form of data (text field OR data file).'
            self.add_error('body', show)
            '''
            Pierwszy blok warunkowy sprawdza, czy wprowadzono jedynie jeden rodzaj danych - wprowadzone dane tekstowe lub załączony plik z danymi. Jeśli dane zostały wprowadzone w obu miejscach, dodaje błąd do pola tekstowego za pomocą 'self.add_error('body', show)'.
            '''

        if not body and not plik1:
            msg = 'Provide either data in the text field or appropriate data file.'
            self.add_error('body', msg)
            '''
            Drugi blok warunkowy sprawdza, czy wprowadzono jakiekolwiek dane. Jeśli żadne dane nie zostały wprowadzone, dodaje błąd do pola tekstowego za pomocą 'self.add_error('body', msg)'.
            '''

        if body:
            tmp = body.split()
            s = 0
            for item in tmp:
                try:
                    s = s + float(item)
                except:
                    self.add_error('body', 'Wrong list')
            '''
            Trzeci blok warunkowy jest odpowiedzialny za walidację danych tekstowych, tj. sprawdzenie, czy wprowadzone dane są listą liczb. Jeśli wprowadzone dane nie są listą liczb, dodaje błąd do pola tekstowego za pomocą 'self.add_error('body', 'Wrong list')'.
            '''
            
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
                '''
             Czwarty blok warunkowy jest odpowiedzialny za walidację danych zawartych w pliku z danymi. Pierwsze wyrażenie 'try' odczytuje załączony plik i konwertuje go na obiekt Pandas DataFrame. Następnie blok ten sprawdza, czy dane w DataFrame są numeryczne. Jeśli dane zawierają nieliczbowe wartości, dodaje błąd do pola załączonego pliku z danymi za pomocą 'self.add_error('plik1', 'The file contains non-numerical data')'. Jeśl DataFrame jest pusty lub zawiera nieprawidłowe dane, dodaje błąd do pola załączonego pliku z danymi za pomocą 'self.add_error('plik1', 'The file contains Data that is wrong or empty.')'. W przeciwnym razie, oblicza sumę danych w pierwszej kolumnie DataFrame i zapisuje ją w zmiennej 'suma', a następnie wyświetla informacje diagnostyczne za pomocą 'print()'.
                '''

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
'''
Kod definiuje klasę 'Molecule', która dziedziczy po klasie 'forms.Form' z modułu Django 'django.forms'. Klasa ta zawiera dwa pola formularza 'title' i 'smiles', z których drugie jest etykietowane tekstem "SMILES". Dodatkowo, klasa ta posiada metodę 'clean()', która jest wywoływana po przesłaniu formularza przez użytkownika i służy do weryfikacji i walidacji danych wprowadzonych przez użytkownika.

Metoda 'clean()' najpierw wywołuje metodę 'clean()' z klasy nadrzędnej za pomocą wyrażenia 'super(Molecule, self).clean()'. W ten sposób otrzymujemy czyste dane z formularza. Następnie zmiennym 'smiles' przypisujemy wartość wprowadzoną przez użytkownika dla pola "SMILES".

Dalej następuje próba przetworzenia wprowadzonej wartości SMILES za pomocą biblioteki Open Babel. Jeśli próba się nie powiedzie (z powodu nieobsługiwanego znaku w SMILES), metoda 'add_error()' zostanie użyta do utworzenia błędu i informacji zwrotnej dla użytkownika, która zostanie wyświetlona na stronie. W tym przypadku informacja zwrotna będzie dotyczyła nieobsługiwanego znaku w SMILES.
'''
