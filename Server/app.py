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
PROXMOX_USERNAME = os.getenv('PROXMOX_USERNAME')
PROXMOX_PASSWORD = os.getenv('PROXMOX_PASSWORD')
MIN_VM_ID = 200

def get_proxmox_token():
    """Authentification à l'API Proxmox pour obtenir le ticket et le CSRF token."""
    response = requests.post(
        f'https://{PROXMOX_IP}/api2/json/access/ticket',
        data={'username': PROXMOX_USERNAME, 'password': PROXMOX_PASSWORD},
        verify=True  # Assurez-vous que SSL/TLS est configuré correctement
    )
    response.raise_for_status()
    return response.json()['data']['ticket'], response.json()['data']['CSRFPreventionToken']

def get_next_vmid(ticket, csrf_token):
    """Récupération du prochain VMID disponible."""
    headers = {'Cookie': f'PVEAuthCookie={ticket}', 'CSRFPreventionToken': csrf_token}
    response = requests.get(
        f'https://{PROXMOX_IP}/api2/json/cluster/resources?type=vm',
        headers=headers,
        verify=True
    )
    response.raise_for_status()
    vm_list = response.json()['data']
    existing_vmids = [vm['vmid'] for vm in vm_list]
    return max([MIN_VM_ID] + existing_vmids) + 1

def validate_data(data):
    """Validation des données d'entrée."""
    allowed_memory_values = {512, 1024, 2048, 4096, 8192, 16384}
    allowed_os_templates = {'ubuntu-20.04', 'ubuntu-22.04', 'debian-11', 'debian-10'}

    if not isinstance(data['vm-name'], str):
        raise ValueError("Invalid VM name")

    if not isinstance(data['cores'], int) or data['cores'] <= 0:
        raise ValueError("Invalid cores value")

    if not isinstance(data['disk'], int) or data['disk'] <= 0:
        raise ValueError("Invalid disk size")

    if data['ram'] not in allowed_memory_values:
        raise ValueError("Invalid memory value")

    if data['os-template'] not in allowed_os_templates:
        raise ValueError("Invalid OS template")

    return data

def create_resource(resource_type, data):
    """Crée une VM ou un CT en utilisant l'API Proxmox."""
    try:
        validate_data(data)
        ticket, csrf_token = get_proxmox_token()
        next_vmid = get_next_vmid(ticket, csrf_token)

        headers = {'Cookie': f'PVEAuthCookie={ticket}', 'CSRFPreventionToken': csrf_token}
        params = {
            'vmid': next_vmid,
            'name' if resource_type == 'qemu' else 'hostname': data['vm-name'],
            'memory': data['ram'],
            'cores': data['cores'],
            'net0': 'e1000,bridge=vmbr0' if resource_type == 'qemu' else 'name=eth0,bridge=vmbr0',
            'ostemplate': data['os-template'],
            'disk' if resource_type == 'qemu' else 'rootfs': f"size={data['disk']}G"
        }

        response = requests.post(
            f'https://{PROXMOX_IP}/api2/json/nodes/{NODE}/{resource_type}',
            headers=headers,
            data=params,
            verify=True  # Assurez-vous que SSL/TLS est configuré correctement
        )
        response.raise_for_status()
        return jsonify({'message': f'{resource_type.upper()} créé avec succès! VMID: {next_vmid}'})
    except ValueError as val_err:
        return jsonify({'error': f'Validation error: {val_err}'}), 400
    except requests.exceptions.RequestException as req_err:
        return jsonify({'error': f'Request error: {req_err}'}), 500
    except Exception as err:
        return jsonify({'error': f'An error occurred: {err}'}), 500

@app.route('/create-vm', methods=['POST'])
def create_vm():
    return create_resource('qemu', request.json)

@app.route('/create-ct', methods=['POST'])
def create_ct():
    return create_resource('lxc', request.json)

@app.route('/')
def index():
    """Renvoie la page d'accueil."""
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(debug=True)
