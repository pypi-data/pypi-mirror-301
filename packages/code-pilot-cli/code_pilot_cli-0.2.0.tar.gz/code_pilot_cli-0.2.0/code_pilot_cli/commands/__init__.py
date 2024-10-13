""" CodePilot commands """

from code_pilot_cli.commands.ai import ai
from code_pilot_cli.commands.chat import chat
from code_pilot_cli.commands.completions import completions
from code_pilot_cli.commands.document import document
from code_pilot_cli.commands.enhance import enhance
from code_pilot_cli.commands.review import review
from code_pilot_cli.commands.scan import scan
from code_pilot_cli.commands.test import test


# Commands here.
command_list = [ai, chat, completions, document, enhance, review, scan, test]
