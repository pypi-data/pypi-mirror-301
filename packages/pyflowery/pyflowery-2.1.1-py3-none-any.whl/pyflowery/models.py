from dataclasses import dataclass, field
from logging import Logger, getLogger
from sys import version as pyversion
from typing import Dict, List, Union

from pyflowery.version import VERSION


@dataclass
class Voice:
    """Voice object returned from the Flowery API

    Attributes:
        id (str): UUID of the voice
        name (str): Name of the voice
        gender (str): Gender of the voice
        source (str): Source of the voice
        language (Language): Language object
    """
    id: str
    name: str
    gender: str
    source: str
    language: 'Language'

@dataclass
class Language:
    """Language object returned from the Flowery API

    Attributes:
        name (str): Name of the language
        code (str): Code of the language
    """
    name: str
    code: str

@dataclass
class Result:
    """Result returned from low-level RestAdapter

    Attributes:
        success (bool): Boolean of whether the request was successful
        status_code (int): Standard HTTP Status code
        message (str = ''): Human readable result
        data (Union[List[Dict], Dict, bytes]): Python List of Dictionaries (or maybe just a single Dictionary on error), can also be a ByteString
    """
    success: bool
    status_code: int
    message: str = ''
    data: Union[List[Dict], Dict, bytes] = field(default_factory=dict)


@dataclass
class FloweryAPIConfig:
    """Configuration for the Flowery API

    Attributes:
        user_agent (str): User-Agent string to use for the HTTP requests. Required as of 2.1.0.
        logger (Logger): Logger to use for logging messages
        allow_truncation (bool): Whether to allow truncation of text that is too long, defaults to `True`
        retry_limit (int): Number of times to retry a request before giving up, defaults to `3`
        interval (int): Seconds to wait between each retried request, multiplied by how many attempted requests have been made, defaults to `5`
    """
    user_agent: str
    logger: Logger = getLogger('pyflowery')
    allow_truncation: bool = False
    retry_limit: int = 3
    interval: int = 5

    def prepended_user_agent(self) -> str:
        """Return the user_agent with the PyFlowery module version prepended"""
        return f"PyFlowery/{VERSION} {self.user_agent} (Python {pyversion})"
