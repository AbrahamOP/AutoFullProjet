Documentation pour app.py
Le fichier app.py est le point d'entrée principal de notre application Flask. Il définit et configure l'application et ses routes.

Le fichier app.py est structuré comme suit :

```python
**from flask import Flask, render_template, request
import proxmox

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/create-vm', methods=['POST'])
def create_vm():
    vm_details = request.get_json()
    proxmox.create_vm(vm_details)
    return 'VM created', 201

if __name__ == '__main__':
    app.run(debug=True)**
```

Détails
L'application Flask est initialisée avec app = Flask(__name__).

La route '/' est définie pour renvoyer la page d'accueil de l'application. Elle utilise la fonction render_template pour rendre le fichier index.html.

La route '/create-vm' est définie pour créer une nouvelle machine virtuelle (VM). Elle accepte les requêtes POST contenant les détails de la VM en JSON. Ces détails sont ensuite passés à la fonction proxmox.create_vm pour créer la VM. Si la création de la VM est réussie, elle renvoie le message 'VM created' avec le code de statut HTTP 201.

Enfin, si le fichier est exécuté directement (et non importé comme un module), app.run(debug=True) est appelé pour démarrer le serveur de développement Flask avec le débogage activé.
