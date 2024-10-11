# src/gmail_automator/__init__.py

from .operations import GmailAutomator
from .email_parser import EmailParserError
from .email_listener import EmailListenerError

__all__ = ['GmailAutomator', 'EmailParserError', 'EmailListenerError']