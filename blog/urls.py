"""
URL mapping for application.
"""

from django.urls import path
from .views import BlogListView, BlogDetailView, BlogDeleteView
from .views import suma, edit_suma, molecule, edit_smiles, peptide, edit_peptide, database, zapytanie_pdb, zapytanie_uniprot

urlpatterns = [
    path("post/<int:pk>/", BlogDetailView.as_view(), name="post_detail"),
    
# Pierwsza ścieżka "post/int:pk/" odpowiada za wyświetlanie widoku szczegółowego dla pojedynczego 
# obiektu modelu "Post" o podanym numerze id. Widok ten jest realizowany przez klasę BlogDetailView 
# i ma nazwę "post_detail".
    
    path("post/", BlogListView.as_view(), name="home"),
    
# Druga ścieżka "post/" odpowiada za wyświetlanie widoku listy wszystkich obiektów modelu "Post". 
# Widok ten jest realizowany przez klasę BlogListView i ma nazwę "home".
    
    path("post/<int:pk>/delete/", BlogDeleteView.as_view(), name="post_delete"),
    
# Trzecia ścieżka "post/int:pk/delete/" odpowiada za usuwanie pojedynczego obiektu modelu "Post" 
# o podanym numerze id. Widok ten jest realizowany przez klasę BlogDeleteView i ma nazwę "post_delete".
    
    path("post/suma/", suma, name="suma"),
    
# Czwarta ścieżka "post/suma/" odpowiada za wyświetlenie widoku formularza, który pozwala na 
# wprowadzanie wartości do pól "suma", "odch", "sr", "var", "med" oraz "shapiro" dla nowego 
# obiektu modelu "Post". Widok ten jest realizowany przez funkcję suma i ma nazwę "suma".
    
    path("post/<int:pk>/edit_suma/", edit_suma, name="suma_edit"),
    
# Piąta ścieżka "post/int:pk/edit_suma/" odpowiada za wyświetlenie widoku formularza, 
# który pozwala na edycję wartości pól "suma", "odch", "sr", "var", "med" oraz "shapiro" dla istniejącego 
# obiektu modelu "Post" o podanym numerze id. Widok ten jest realizowany przez funkcję edit_suma i 
# ma nazwę "suma_edit".
    
    path("post/molecule/", molecule, name="molecule"),
    path("post/peptide/", peptide, name="peptide"),
    path("post/database/", database, name="database"),
    path("post/zapytanie_pdb/", zapytanie_pdb, name="zapytanie_pdb"),
    path("post/zapytanie_uniprot/", zapytanie_uniprot, name="zapytanie_uniprot"),
    
# Szósta ścieżka "post/molecule/" odpowiada za wyświetlenie widoku formularza, 
# który pozwala na wprowadzenie danych dotyczących cząsteczki chemicznej do nowego obiektu modelu "Post". 
# Widok ten jest realizowany przez funkcję molecule i ma nazwę "molecule".
    
    path("post/<int:pk>/edit_smiles/", edit_smiles, name="smiles_edit"),
    
# Siódma ścieżka "post/int:pk/edit_smiles/" odpowiada za wyświetlenie widoku formularza, 
# który pozwala na edycję pola "smiles" dla istniejącego obiektu modelu "Post" o podanym numerze id. 
# Widok ten jest realizowany przez funkcję edit_smiles i ma nazwę "smiles_edit". 
    
    path("post/<int:pk>/edit_peptide/", edit_peptide, name="edit_peptide"),
]
