# programming_project_WCh
Programming project developed by bioinformatics students at Faculty of Chemistry, 
University of Gdansk


2022.05.30 - Django web application for simple data analysis
branch sumowanie from gitlab repository https://etoh.chem.ug.edu.pl/gitlab/studenci/projekt-programistyczny

INSTRUKCJA INSTALACJI DLA WINDOWSA ;)

a) Instalacja WSL

b) Instalacja Ubuntu on Windows z Microsoft Store

c) Dalsza praca w terminalu linuxa:

1.	Generowanie klucza ssh: 
ssh-keygen -t rsa -b 4096 -C "Twój e-mail z githuba"

2.	Wyświetlenie klucza:
cat id_rsa.pub

3.	Skopiowanie klucza do GitHub’a w zakładce "SSH and GPG keys” w ustawieniach konta.

4.	Utworzenie katalogu z projektem, przejście do niego. 

5.	Przejście do https://github.com/ugbioinformatics/programming_project_WCh i skopiowanie SSH(git@github.com:ugbioinformatics/programming_project_WCh.git). 

6.	Sklonowanie SSH za pomocą komendy:
git clone git@github.com:ugbioinformatics/programming_project_WCh.git

7.	Przejście do sklonowanego katalogu projektu.

8.	Instalacja:
apt install python3-pip
apt install virtualenv

9.	Stworzenie środowiska za pomocą komendy:
virtualenv env

10.	Aktywacja środowiska za pomocą komendy:
source env/bin/activate

11.	Instalacja Django za pomocą komendy:
pip install django

12.	Instalacja:
pip install matplotlib 
pip install pandas

13.	Instalacja openbabel:
apt install openbabel
apt install python3-openbabel
ln -s /usr/lib/python3/dist-packages/openbabel $VIRTUAL_ENV/lib/python*/site-packages

14.	Przygotowanie i utworzenie bazy danych:
./manage.py makemigrations blog
./manage.py migrate

15.	Uruchomienie serwera:
./manage.py runserver



