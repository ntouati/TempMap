Plugin Builder Results

Your plugin TempMap was created in:
    C:\Users\thoma\.qgis2\python\plugins\TempMap

Your QGIS plugin directory is located at:
    C:/Users/thoma/.qgis2/python/plugins

What's Next:

  * Copy the entire directory containing your new plugin to the QGIS plugin
    directory

  * Compile the resources file using pyrcc4

  * Run the tests (``make test``)

  * Test the plugin by enabling it in the QGIS plugin manager

  * Customize it by editing the implementation file: ``temp_map.py``

  * Create your own custom icon, replacing the default icon.png

  * Modify your user interface by opening TempMap.ui in Qt Designer

  * You can use the Makefile to compile your Ui and resource files when
    you make changes. This requires GNU make (gmake)

For more information, see the PyQGIS Developer Cookbook at:
http://www.qgis.org/pyqgis-cookbook/index.html

(C) 2011-2014 GeoApt LLC - geoapt.com
Git revision : $Format:%H$


Descriptif des fichiers contenus dans ce dossier :

__init__.py : Fichier init. produit par Plug-in Builder. Classe indispensable au foncitonnement
du plug-in. (__init__.pyc : version compilée de ce fichier).

progress.py : Fichier issu de Qt Designer permettant l'implémentation d'une barre de progression
durant le traitement du plug-in. (progress.pyc : version compilée de ce fichier; progress.ui : fichier Qt designer d'origine).

resources.py : Issu du fichier resources.qrc, fichier de resources utilisé notamment par Qt Designer pour l'intégration
d'images dans l'interface. (resources.pyc : version compilée de ce fichier)

temp_map.py : Fichier principal contenant l'ensemble des classes et des fonctions, ainsi que la totalité du code assurant
le foncitonnement du plug-in. (temp_map.pyc : version compilée de ce fichier)

temp_map_dialog.py : Ficchier issu de Qt Designer décrivant l'interface utilisateur proposée par le plug-in.

help.png / icon.png : Images utilisées par le plug-in, respectivement icône d'aide et icône du plug-in. 
