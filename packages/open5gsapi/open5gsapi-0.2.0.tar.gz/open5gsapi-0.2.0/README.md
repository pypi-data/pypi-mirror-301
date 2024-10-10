# Open5GS API

This package provides a Python API for interacting with Open5GS components and managing PCF configurations.

## Installation

```bash
pip install open5gsapi
```

## Usage

First, import the package:

```python
from open5gsapi import open5gs
```

### UE and UPF Operations

#### Getting API URLs

```python
# Get UE API URL
UE_API_URL = open5gs.ue(8080, "send")
# Result: "http://10.10.0.132:8080/send"

# Get UPF API URL
UPF_API_URL = open5gs.upf(8081, "receive", "sensor")
# Result: "http://10.10.0.112:8081/receive/sensor"
```

#### Sending and Receiving Data

```python
# Send data
data = {"sensor_id": 1, "temperature": 25.5, "humidity": 60}
response = open5gs.send_data(UE_API_URL, data)

# Receive data
received_data = open5gs.receive_data(UPF_API_URL)
```

### PCF Configuration Management

#### Modifying Session Parameters

```python
# Modify downlink AMBR for 'video-streaming' session
open5gs.policy.session('video-streaming').ambr.downlink(value=10000000, unit=1)

# Modify uplink AMBR for 'video-streaming' session
open5gs.policy.session('video-streaming').ambr.uplink(value=20000000, unit=1)

# Modify QoS index
open5gs.policy.session('video-streaming').qos(index=5)

# Modify ARP
open5gs.policy.session('video-streaming').arp(priority_level=7, pre_emption_vulnerability=2, pre_emption_capability=1)
```

#### Managing Sessions

```python
# Add a new session
new_session = open5gs.policy.add_session('new-session-name')
new_session.ambr.downlink(value=5000000, unit=1)
new_session.ambr.uplink(value=1000000, unit=1)

# Remove a session
open5gs.policy.remove_session('session-to-remove')
```

#### Updating Configuration

After making changes to the configuration, you need to call `update_config()` to apply the changes and restart the PCF service:

```python
open5gs.update_config()
```

This method will:
1. Update the PCF YAML configuration file
2. Tear down existing Docker containers
3. Redeploy the containers with the new configuration

## API Reference

### UE and UPF Operations

- `open5gs.ue(port: int, endpoint: str) -> str`: Get the UE API URL
- `open5gs.upf(port: int, *args) -> str`: Get the UPF API URL
- `open5gs.send_data(url: str, data: Dict[str, Any]) -> Dict[str, Any]`: Send data to the specified URL
- `open5gs.receive_data(url: str) -> Dict[str, Any]`: Receive data from the specified URL

### PCF Configuration Management

- `open5gs.policy.session(name: str) -> Session`: Get or create a session
- `open5gs.policy.add_session(name: str) -> Session`: Add a new session
- `open5gs.policy.remove_session(name: str)`: Remove a session

#### Session Methods

- `session.ambr.downlink(value: int, unit: int)`: Set downlink AMBR
- `session.ambr.uplink(value: int, unit: int)`: Set uplink AMBR
- `session.qos(index: int)`: Set QoS index
- `session.arp(priority_level: int, pre_emption_vulnerability: int, pre_emption_capability: int)`: Set ARP parameters

### Configuration Update

- `open5gs.update_config()`: Update the PCF configuration and restart the service

## Notes

- Ensure that the user running the script has the necessary permissions to modify the PCF configuration file and manage Docker containers.
- The Docker commands used in `update_config()` assume that `docker` and `docker compose` are available in the system path. Adjust the paths if necessary.