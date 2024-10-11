import yaml
import requests
import subprocess
import logging
from typing import Dict, Any
from ruamel.yaml import YAML
from .exceptions import ConfigurationError, CommunicationError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AMBRDirection:
    def __init__(self, parent, direction):
        self.parent = parent
        self.direction = direction
        self.value = None
        self.unit = None

    def __call__(self, value: int, unit: int):
        self.value = value
        self.unit = unit
        return self

class AMBR:
    def __init__(self, parent):
        self.parent = parent
        self.downlink = AMBRDirection(self, 'downlink')
        self.uplink = AMBRDirection(self, 'uplink')

class QoS:
    def __init__(self, parent):
        self.parent = parent
        self.index = None

    def __call__(self, index: int):
        self.index = index
        return self

class ARP:
    def __init__(self, parent):
        self.parent = parent
        self.priority_level = None
        self.pre_emption_vulnerability = None
        self.pre_emption_capability = None

    def __call__(self, priority_level: int, pre_emption_vulnerability: int, pre_emption_capability: int):
        self.priority_level = priority_level
        self.pre_emption_vulnerability = pre_emption_vulnerability
        self.pre_emption_capability = pre_emption_capability
        return self

class Session:
    def __init__(self, parent, name):
        self.parent = parent
        self.name = name
        self.ambr = AMBR(self)
        self.qos = QoS(self)
        self.arp = ARP(self)

class Policy:
    def __init__(self, config_path):
        self.config_path = config_path
        self.yaml = YAML()
        self.yaml.preserve_quotes = True
        self.yaml.indent(mapping=2, sequence=4, offset=2)
        self.config = self._read_config()
        self.sessions = {}
        self._load_sessions()

    def _read_config(self):
        with open(self.config_path, 'r') as file:
            return self.yaml.load(file)

    def _load_sessions(self):
        for policy in self.config['pcf']['policy']:
            for slice_config in policy['slice']:
                for session in slice_config['session']:
                    self.sessions[session['name']] = Session(self, session['name'])

    def session(self, name):
        if name not in self.sessions:
            self.sessions[name] = Session(self, name)
        return self.sessions[name]

    def add_session(self, name):
        if name in self.sessions:
            raise ConfigurationError(f"Session '{name}' already exists")
        self.sessions[name] = Session(self, name)
        return self.sessions[name]

    def remove_session(self, name):
        if name not in self.sessions:
            raise ConfigurationError(f"Session '{name}' does not exist")
        del self.sessions[name]

    def list_sessions(self):
        """Return a list of all session names."""
        return list(self.sessions.keys())

    def rename_session(self, old_name: str, new_name: str):
        """Rename a session."""
        if old_name not in self.sessions:
            raise ConfigurationError(f"Session '{old_name}' does not exist")
        if new_name in self.sessions:
            raise ConfigurationError(f"Session '{new_name}' already exists")
        
        self.sessions[new_name] = self.sessions.pop(old_name)
        self.sessions[new_name].name = new_name

        for policy in self.config['pcf']['policy']:
            for slice_config in policy['slice']:
                for session in slice_config['session']:
                    if session['name'] == old_name:
                        session['name'] = new_name
                        return 

    def get_session_details(self, name: str): # Details of a specific session
        if name not in self.sessions:
            raise ConfigurationError(f"Session '{name}' does not exist")
        
        for policy in self.config['pcf']['policy']:
            for slice_config in policy['slice']:
                for session in slice_config['session']:
                    if session['name'] == name:
                        return session
        
        raise ConfigurationError(f"Session '{name}' not found in configuration")

    def update_config(self):
        for policy in self.config['pcf']['policy']:
            for slice_config in policy['slice']:
                for session in slice_config['session']:
                    if session['name'] in self.sessions:
                        updated_session = self.sessions[session['name']]
                        if updated_session.ambr.downlink.value is not None:
                            session['ambr']['downlink']['value'] = updated_session.ambr.downlink.value
                            session['ambr']['downlink']['unit'] = updated_session.ambr.downlink.unit
                        if updated_session.ambr.uplink.value is not None:
                            session['ambr']['uplink']['value'] = updated_session.ambr.uplink.value
                            session['ambr']['uplink']['unit'] = updated_session.ambr.uplink.unit
                        if updated_session.qos.index is not None:
                            session['qos']['index'] = updated_session.qos.index
                        if updated_session.arp.priority_level is not None:
                            session['qos']['arp']['priority_level'] = updated_session.arp.priority_level
                            session['qos']['arp']['pre_emption_vulnerability'] = updated_session.arp.pre_emption_vulnerability
                            session['qos']['arp']['pre_emption_capability'] = updated_session.arp.pre_emption_capability

        with open(self.config_path, 'w') as file:
            self.yaml.dump(self.config, file)

class CommunicationInterface:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def send_data(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            response = requests.post(f"{self.base_url}/{endpoint}", json=data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise CommunicationError(f"Error sending data: {str(e)}")

    def receive_data(self, endpoint: str) -> Dict[str, Any]:
        try:
            response = requests.get(f"{self.base_url}/{endpoint}")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise CommunicationError(f"Error receiving data: {str(e)}")

class UEInterface(CommunicationInterface):
    pass

class UPFInterface(CommunicationInterface):
    pass

class Open5GS:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Open5GS, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.policy = Policy('../../deployment/open5gs/config/pcf.yaml')
        self.ue_interface = UEInterface("http://10.10.0.132")
        self.upf_interface = UPFInterface("http://10.10.0.112")

    def ue(self, port: int, endpoint: str) -> str:
        return f"{self.ue_interface.base_url}:{port}/{endpoint}"

    def upf(self, port: int, *args) -> str:
        return f"{self.upf_interface.base_url}:{port}/{'/'.join(args)}"

    def send_data(self, url: str, data: Dict[str, Any]) -> Dict[str, Any]:
        return self.ue_interface.send_data(url, data)

    def receive_data(self, url: str) -> Dict[str, Any]:
        return self.upf_interface.receive_data(url)
    
    def list_sessions(self):
        return self.policy.list_sessions()

    def rename_session(self, old_name: str, new_name: str):
        self.policy.rename_session(old_name, new_name)

    def get_session_details(self, name: str):
        return self.policy.get_session_details(name)

    def update_config(self):
        self.policy.update_config()
        self._restart_pcf_service()
        self._run_container_scripts()

    def _restart_pcf_service(self):
        try:
            # Check if Docker containers are running
            result = subprocess.run(["docker", "ps", "-q"], capture_output=True, text=True)
            if result.stdout.strip():
                logger.info("Existing Docker containers found. Tearing down...")
                subprocess.run(["docker", "compose", "down", "-t", "1", "-v"], check=True)
            else:
                logger.info("No running Docker containers found.")

            logger.info("Bringing up Docker deployment...")
            subprocess.run(["docker", "compose", "up", "-d"], check=True)

            logger.info("PCF service restarted successfully")
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to restart PCF service: {str(e)}")
            raise ConfigurationError(f"Failed to restart PCF service: {str(e)}")
        
    def _run_container_scripts(self):
        try:
            logger.info("Running scripts in UE and UPF containers...")
            
            # Run script in UE container
            ue_command = 'docker exec -it ue bash -c "sh init_script.sh && python3 auto-ue-api.py"'
            subprocess.Popen(['tmux', 'new-window', '-n', 'ue', ue_command], start_new_session=True)
            
            # Run script in UPF container
            upf_command = 'docker exec -it upf bash -c "cd src/upf && sh init_script.sh && python3 upf-api.py"'
            subprocess.Popen(['tmux', 'new-window', '-n', 'upf', upf_command])
            
            logger.info("Scripts started successfully in tmux sessions")
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to run container scripts: {str(e)}")
            raise ConfigurationError(f"Failed to run container scripts: {str(e)}")

open5gs = Open5GS()