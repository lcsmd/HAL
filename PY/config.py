import os
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class ServerConfig:
    host: str
    port: int

@dataclass
class Config:
    # OpenQM Server
    qm_server: ServerConfig = field(default_factory=lambda: ServerConfig(
        host="MV1.q.lcs.a",
        port=4243  # Default OpenQM port, adjust if different
    ))
    
    # Ollama Server
    ollama_server: ServerConfig = field(default_factory=lambda: ServerConfig(
        host="ubu5.q.lcs.ai",
        port=11434  # Default Ollama port
    ))
    
    # Local paths
    qm_account_path: str = r"q:\QMSYS\HAL"
    
    # Environment
    is_local: bool = True  # Set to False when running on the server
    
    @staticmethod
    def load():
        """Load configuration from environment variables if available"""
        config = Config()
        
        # Override with environment variables if set
        if os.getenv("QM_SERVER_HOST"):
            config.qm_server.host = os.getenv("QM_SERVER_HOST")
        if os.getenv("QM_SERVER_PORT"):
            config.qm_server.port = int(os.getenv("QM_SERVER_PORT"))
        if os.getenv("OLLAMA_SERVER_HOST"):
            config.ollama_server.host = os.getenv("OLLAMA_SERVER_HOST")
        if os.getenv("OLLAMA_SERVER_PORT"):
            config.ollama_server.port = int(os.getenv("OLLAMA_SERVER_PORT"))
            
        return config

config = Config.load()
