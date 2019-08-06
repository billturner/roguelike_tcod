from textwrap import wrap
from typing import List

from components.message import Message


class MessageLog:
    def __init__(self, x: int, width: int, height: int):
        self.messages: List[Message] = []
        self.x = x
        self.width = width
        self.height = height

    def add_message(self, message: Message) -> None:
        # split the message if necessary
        new_msg_lines = wrap(message.text, self.width)

        for line in new_msg_lines:
            # if message buffer is full, remove first
            # line to make room for new ones.
            if len(self.messages) == self.height:
                del self.messages[0]

            # Now add new message
            self.messages.append(Message(line, message.color))
