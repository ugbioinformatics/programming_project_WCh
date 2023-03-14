# programming_project_WCh
Programming project developed by bioinformatics students at Faculty of Chemistry, 
University of Gdansk


2022.05.30 - Django web application for simple data analysis
branch sumowanie from gitlab repository https://etoh.chem.ug.edu.pl/gitlab/studenci/projekt-programistyczny

2022.06.02 - merge branch chemia from gitlab repository https://etoh.chem.ug.edu.pl/gitlab/studenci/projekt-programistyczny/-/tree/chemia

INSTRUKCJA INSTALACJI na procowni komputerowe (Ubunut 20.04)

1. Utworzenie katalogu z projektem, przejście do niego.

2. Stworzenie środowiska za pomocą komendy: <br>
virtualenv env

3. Aktywacja środowiska za pomocą komendy: <br>
source env/bin/activate.csh

4. Sklonowanie SSH za pomocą komendy: <br>
git clone git@github.com:ugbioinformatics/programming_project_WCh.git

5. Przejście do sklonowanego katalogu projektu.
cd programming_project_WCh

6. pip install -r requirements.txt

7. ln -s /usr/lib/python3/dist-packages/openbabel $VIRTUAL_ENV/lib/python*/site-packages


INSTRUKCJA INSTALACJI DLA WINDOWSA ;)

Z powodu niekompatybilnej wersji biblioteki openbabel w natywnym python dla Windows
aplikacja nie działa dla natywnego python dla Winodws i wymaga instalacji WSL oraz Ubuntu on Windows 

a) Instalacja WSL

b) Instalacja Ubuntu on Windows z Microsoft Store

c) Dalsza praca w terminalu linuxa:

1.	Generowanie klucza ssh: <br>
ssh-keygen -t rsa -b 4096 -C "Twój e-mail z githuba"

2.	Wyświetlenie klucza: <br>
cat id_rsa.pub

3.	Skopiowanie klucza do GitHub’a w zakładce "SSH and GPG keys” w ustawieniach konta.

4.	Utworzenie katalogu z projektem, przejście do niego. 

5.	Przejście do https://github.com/ugbioinformatics/programming_project_WCh i skopiowanie opcji dla SSH<br> (git@github.com:ugbioinformatics/programming_project_WCh.git). 

6.	Sklonowanie SSH za pomocą komendy: <br>
git clone git@github.com:ugbioinformatics/programming_project_WCh.git

7.	Przejście do sklonowanego katalogu projektu.

8.	Instalacja: <br>
apt install python3-pip <br>
apt install virtualenv

9.	Stworzenie środowiska za pomocą komendy: <br>
virtualenv env

10.	Aktywacja środowiska za pomocą komendy: <br>
source env/bin/activate

11.	Instalacja Django za pomocą komendy: <br>
pip install django

12.	Instalacja: <br>
pip install matplotlib <br>
pip install pandas<br>
pip install statsmodels<br>
pip install scipy

Uwaga: zamiast 11. i 12. można wykonać

pip install -r requirements.txt

13.	Instalacja openbabel: <br>
apt install openbabel <br>
apt install python3-openbabel <br>
ln -s /usr/lib/python3/dist-packages/openbabel $VIRTUAL_ENV/lib/python*/site-packages

14.	Przygotowanie i utworzenie bazy danych: <br>
./manage.py makemigrations blog <br>
./manage.py migrate

15.	Uruchomienie serwera: <br>
./manage.py runserver



