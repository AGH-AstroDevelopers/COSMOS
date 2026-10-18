from abc import ABC, abstractmethod

class TelemetrySource(ABC):
    """Contract for every telemetry source (e.g. pythone simulator, hardware)
    
    All sources need to have the same structure so the rest of the backend can
    understand it, while maintaining modularity. New source implements this interface."""
    
    id:str 
    name: str 

    @abstractmethod
    def decode(self, raw:dict) ->dict:
        """TODO: Validate raw input and return it in the internal packet format.

        Raises ValueError with a readable message if the input is invalid.
        """

    def send_command(self, command:dict) ->dict:
        """TODO: Sending command to the satellite (Uplink)"""
        raise NotImplementedError
