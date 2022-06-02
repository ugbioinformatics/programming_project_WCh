# programming_project_WCh
Programming project developed by bioinformatics students at Faculty of Chemistry, 
University of Gdansk

2022.05.30 - Django web application for simple data analysis
branch sumowanie from gitlab repository https://etoh.chem.ug.edu.pl/gitlab/studenci/projekt-programistyczny

Instrukcja dla Windows: 
1.	Instalacja WSL.
2.	Instalacja Ubuntu on Windows z Microsoft Store.

TERMINAL

1.	Generowanie klucza ssh: ssh-keygen -t rsa -b 4096 -C "wpisz e-mail"
2.	Wyświetlenie klucza cat id_rsa.pub. 
3.	Skopiowanie klucza do GitHub’a w zakładce ‘’SSH and GPG keys” w ustawieniach konta.
4.	Utworzenie katalogu z projektem, przejście do niego. 
5.	 Przejście do https://github.com/ugbioinformatics/programming_project_WCh i skopiowanie SSH(git@github.com:ugbioinformatics/programming_project_WCh.git). 
6.	Sklonowanie SSH za pomocą komendy git clone git@github.com:ugbioinformatics/programming_project_WCh.git.
7.	Przejście do sklonowanego katalogu projektu.
8.	Instalacja apt install python3-pip, virtualenv.
9.	Założenie środowiska za pomocą komendy virtualenv env. 
10.	Aktywacja środowiska za pomocą komendy source env/bin/activate.
11.	Instalacja Django za pomocą komendy pip install django.
12.	Instalacja matplotlib oraz pandas.
13.	Instalacja openbabel apt install openbabel, apt install python3-openbabel, ls /usr/lib/python3/dist-packages/openbabel/, ln -s /usr/lib/python3/dist-packages/openbabel $VIRTUAL_ENV/lib/python*/site-packages.
14.	Przygotowanie i wykonanie bazy danych ./manage.py makemigrations blog oraz ./manage.py migrate.
15.	Uruchomienie strony ./manage.py runserver.



