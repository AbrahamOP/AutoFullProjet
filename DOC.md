Documentation du projet
Structure du projet
Le projet est structuré comme suit :

```python
README.md
Server/
    app.py
    README.md
static/
    image/
    index.html
    lxc/
        lxc.css
        lxc.html
        lxc.js
    README.md
    style.css
    vm/
        vm.css
        vm.html
        vm.js
```

js
Server
Le serveur est écrit en Python et utilise le framework Flask. Il est défini dans le fichier app.py. Il expose deux routes principales :

/ : Renvoie la page d'accueil.
/create-vm : Crée une nouvelle machine virtuelle (VM) en utilisant l'API Proxmox.
Static
Le dossier static contient les fichiers statiques du projet, y compris les fichiers HTML, CSS et JavaScript pour les pages front-end.

Index
La page d'accueil du projet est définie dans index.html. Elle contient des boutons pour naviguer vers les pages de création de VM et de LXC.

VM
La page de création de VM est définie dans vm.html. Elle contient un formulaire pour spécifier les détails de la nouvelle VM, comme le nom, le système d'exploitation, le nombre de cœurs et la RAM.

LXC
La page de création de LXC est définie dans lxc.html. Elle contient un formulaire pour spécifier les détails du nouveau conteneur LXC, comme le nom et le modèle de conteneur.

JavaScript
Les fichiers JavaScript associés aux pages de création de VM et de LXC sont vm.js et lxc.js respectivement. Ils gèrent l'envoi des données du formulaire au serveur lors de la soumission du formulaire.