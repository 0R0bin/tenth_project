# tenth_project
Pour installer ce projet, téléchargez ou clonez le repository à l'aide du lien suivant
```
https://github.com/0R0bin/tenth_project.git
```
Placez vous dans le dossier du repository, puis, exectuez les commandes suivantes :
Sous Unix/macOS
```
python3 -m venv env
```
```
source env/bin/activate
```
Sous Windows
```
py -m venv env
```
```
.\env\Scripts\activate
```
Ensuite, installez les packages nécessaires :
```
pip install -r requirements.txt
```
Positionnez vous ensuite dans le dossier softdeskapi
Et executez les commandes suivantes pour initialiser le projet :
```
python manage.py makemigrations
```
```
python manage.py migrate
```
```
python manage.py runserver
```
Rendez-vous ensuite sur votre navigateur à l'adresse suivante :
```
http://127.0.0.1:8000
```
Vous êtez prêt !

Notez d'ailleurs qu'un swagger et un redoc sont disponibles aux adresses suivante :
```
http://127.0.0.1:8000/doc_swagger/
http://127.0.0.1:8000/doc_redoc/
```

Pour terminer, merci de noter que le flake8 a été executé avec un max_line à 100