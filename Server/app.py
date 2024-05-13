from flask import Flask, request, jsonify
import requests
import json
from dotenv import load_dotenv
import os

app = Flask(__name__, static_folder='../static')

# Charger les variables d'environnement
load_dotenv()

PROXMOX_IP = os.getenv('PROXMOX_IP')
NODE = os.getenv('PROXMOX_NODE')
MIN_VM_ID = 200

def get_proxmox_token():
    """Authentification à l'API Proxmox pour obtenir le ticket et le CSRF token."""
    response = requests.post(
        f'https://{PROXMOX_IP}/api2/json/access/ticket',
        data={'username': os.getenv('PROXMOX_USERNAME'), 'password': os.getenv('PROXMOX_PASSWORD')},
        verify=False  # pour les environnements de production, configurez SSL/TLS correctement
    )
    response.raise_for_status()  # Lève une exception pour les codes de statut 4xx/5xx
    return response.json()['data']['ticket'], response.json()['data']['CSRFPreventionToken']

def get_next_vmid(ticket, csrf_token):
    """Récupération du prochain vmid disponible pour la création d'une VM."""
    headers = {'Cookie': f'PVEAuthCookie={ticket}', 'CSRFPreventionToken': csrf_token}
    response = requests.get(
        f'https://{PROXMOX_IP}/api2/json/cluster/resources?type=vm',
        headers=headers,
        verify=False
    )
    response.raise_for_status()
    vm_list = response.json()['data']
    existing_vmids = [vm['vmid'] for vm in vm_list]
    return max([MIN_VM_ID] + existing_vmids) + 1

@app.route('/create-vm', methods=['POST'])
def create_vm():
    """Crée une VM en utilisant l'API Proxmox."""
    data = request.json
    try:
        ticket, csrf_token = get_proxmox_token()
        next_vmid = get_next_vmid(ticket, csrf_token)

        headers = {'Cookie': f'PVEAuthCookie={ticket}', 'CSRFPreventionToken': csrf_token}
        vm_params = {
            'vmid': next_vmid,
            'name': data['vm-name'],
            'memory': data['ram'],
            'cores': data['cores'],
            'net0': 'e1000,bridge=vmbr0',
#           'ostemplate': data['os-template'],
            'disk': f"size={data['disk']}G"
        }

        response = requests.post(
            f'https://{PROXMOX_IP}/api2/json/nodes/{NODE}/qemu',
            headers=headers,
            data=vm_params,
            verify=False
        )
        response.raise_for_status()
        return jsonify({'message': f'VM créée avec succès! VMID: {next_vmid}'})
    except requests.HTTPError as http_err:
        return jsonify({'error': f'HTTP error occurred: {http_err}'}), 500
    except Exception as err:
        return jsonify({'error': f'An error occurred: {err}'}), 500

@app.route('/')
def index():
    """Renvoie la page d'accueil."""
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(debug=True)
