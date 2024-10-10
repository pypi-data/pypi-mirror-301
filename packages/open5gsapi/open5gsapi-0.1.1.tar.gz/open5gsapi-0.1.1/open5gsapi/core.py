import yaml
import requests
import subprocess
import logging
from typing import Dict, Any
from .exceptions import ConfigurationError, CommunicationError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AMBR:
    def __init__(self, value: int, unit: int):
        self.value = value
        self.unit = unit

    def __repr__(self):
        return f"AMBR(value={self.value}, unit={self.unit})"

class QoS:
    def __init__(self, index: int):
        self.index = index

    def __repr__(self):
        return f"QoS(index={self.index})"

class ARP:
    def __init__(self, priority_level: int, pre_emption_vulnerability: int, pre_emption_capability: int):
        self.priority_level = priority_level
        self.pre_emption_vulnerability = pre_emption_vulnerability
        self.pre_emption_capability = pre_emption_capability

    def __repr__(self):
        return f"ARP(priority_level={self.priority_level}, pre_emption_vulnerability={self.pre_emption_vulnerability}, pre_emption_capability={self.pre_emption_capability})"

class ConfigManager:
    def __init__(self, config_path: str):
        self.config_path = config_path

    def read_config(self) -> Dict[str, Any]:
        try:
            with open(self.config_path, 'r') as file:
                return yaml.safe_load(file)
        except Exception as e:
            raise ConfigurationError(f"Error reading configuration file: {str(e)}")

    def write_config(self, config: Dict[str, Any]):
        try:
            with open(self.config_path, 'w') as file:
                yaml.dump(config, file)
        except Exception as e:
            raise ConfigurationError(f"Error writing configuration file: {str(e)}")

    def update_config(self, updates: Dict[str, Any]):
        config = self.read_config()
        for policy in config['pcf']['policy']:
            for slice_config in policy['slice']:
                for session in slice_config['session']:
                    if 'qos' in updates:
                        session['qos']['index'] = updates['qos'].index
                    if 'ambr' in updates:
                        for direction in ['downlink', 'uplink']:
                            session['ambr'][direction]['value'] = updates['ambr'].value
                            session['ambr'][direction]['unit'] = updates['ambr'].unit
                    if 'arp' in updates:
                        session['qos']['arp']['priority_level'] = updates['arp'].priority_level
                        session['qos']['arp']['pre_emption_vulnerability'] = updates['arp'].pre_emption_vulnerability
                        session['qos']['arp']['pre_emption_capability'] = updates['arp'].pre_emption_capability
        self.write_config(config)

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
        self.config_manager = ConfigManager('/open5gs/config/pcf.yaml')
        self.ue_interface = UEInterface("http://10.10.0.132")
        self.upf_interface = UPFInterface("http://10.10.0.112")

    def ambr(self, value: int, unit: int) -> AMBR:
        return AMBR(value, unit)

    def qos(self, index: int) -> QoS:
        return QoS(index)

    def arp(self, priority_level: int, pre_emption_vulnerability: int, pre_emption_capability: int) -> ARP:
        return ARP(priority_level, pre_emption_vulnerability, pre_emption_capability)

    def update_config(self, **kwargs):
        self.config_manager.update_config(kwargs)
        self._restart_pcf_service()

    def ue(self, port: int, endpoint: str) -> str:
        return f"{self.ue_interface.base_url}:{port}/{endpoint}"

    def upf(self, port: int, *args) -> str:
        return f"{self.upf_interface.base_url}:{port}/{'/'.join(args)}"

    def send_data(self, url: str, data: Dict[str, Any]) -> Dict[str, Any]:
        return self.ue_interface.send_data(url, data)

    def receive_data(self, url: str) -> Dict[str, Any]:
        return self.upf_interface.receive_data(url)

    def _restart_pcf_service(self):
        try:
            subprocess.run(["systemctl", "restart", "open5gs-pcfd.service"], check=True)
            logger.info("PCF service restarted successfully")
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to restart PCF service: {str(e)}")