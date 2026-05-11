import enum
from dataclasses import dataclass
from abc import ABC, abstractmethod


class MessageType(enum.Enum):
    TELEGRAM = enum.auto()
    MATTERMOST = enum.auto()
    SLACK = enum.auto()


@dataclass
class JsonMessage:
    message_type: MessageType
    payload: str


@dataclass
class ParsedMessage:
    """There is no need to describe anything here."""
    message_id: str
    text: str
    sender_id: str
    timestamp: str | None



class MessageParser(ABC):
    @abstractmethod
    def parse(self, message: JsonMessage) -> ParsedMessage: ...


class TelegramParser(ABC):
    @abstractmethod
    def parse(self, message: JsonMessage) -> ParsedMessage: ...


class MatterMost(ABC):
    @abstractmethod
    def parse(self, message: JsonMessage) -> ParsedMessage: ...


class Slack(ABC):
    @abstractmethod
    def parse(self, message: JsonMessage) -> ParsedMessage: ...


class ParseFactory:
    _parsers: dict[MessageType, MessageParser]

    def __init__(self):
        self._parsers = {
            MessageType.TELEGRAM: TelegramParser(),
            MessageType.MATTERMOST: MatterMost(),
            MessageType.SLACK: Slack()
        }
    
    def get_parser(self, message_type: MessageType) -> MessageParser:
        return self._parsers[message_type]
    

    def parse_message(self, message: JsonMessage) -> ParsedMessage:
        parser = self.get_parser(message.message_type)
        return parser.parse(message)