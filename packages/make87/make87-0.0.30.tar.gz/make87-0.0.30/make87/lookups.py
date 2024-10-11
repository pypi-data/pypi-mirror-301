from threading import Lock
from make87.messages import parse_sockets, parse_peripherals


class TopicNamesLookup:
    """Lookup for topic names. Must be initialized explicitly."""

    def __init__(self):
        self._attributes = None
        self._initialized = False
        self._lock = Lock()

    def initialize(self):
        with self._lock:
            if self._initialized:
                return
            socket_data = parse_sockets()
            self._attributes = {}
            for socket in socket_data.sockets:
                self._attributes[socket.topic_name] = socket.topic_key
            self._initialized = True

    def __getattr__(self, name: str) -> str:
        if not self._initialized:
            raise RuntimeError("TopicNamesLookup not initialized. Call initialize() first.")
        if name in self._attributes:
            return self._attributes[name]
        else:
            raise AttributeError(f"Topic name '{name}' not found. Ensure it is defined in your manifest file.")


class PeripheralNamesLookup:
    """Lookup for peripheral names. Must be initialized explicitly."""

    def __init__(self):
        self._attributes = None
        self._initialized = False
        self._lock = Lock()

    def initialize(self):
        with self._lock:
            if self._initialized:
                return
            peripheral_data = parse_peripherals()
            self._attributes = {}
            for peripheral in peripheral_data.peripherals:
                self._attributes[peripheral.name] = peripheral.mount
            self._initialized = True

    def __getattr__(self, name: str) -> str:
        if not self._initialized:
            raise RuntimeError("PeripheralNamesLookup not initialized. Call initialize() first.")
        if name in self._attributes:
            return self._attributes[name]
        else:
            raise AttributeError(f"Peripheral name '{name}' not found. Ensure it is defined in your manifest file.")
