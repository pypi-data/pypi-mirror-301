class Open5GSError(Exception):
    """Base exception class for Open5GS errors"""

class ConfigurationError(Open5GSError):
    """Raised when there's an error in configuration management"""

class CommunicationError(Open5GSError):
    """Raised when there's an error in communication with UE or UPF"""