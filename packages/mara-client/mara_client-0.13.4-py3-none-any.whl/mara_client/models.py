import json
from datetime import datetime
from typing import List, Optional

import pandas as pd
from pydantic import BaseModel

__all__ = [
    'ChatFile', 'ChatMessage', 'ChatResult', 'DataTable',
    'DataTableModification', 'DataTableOperation'
]


class ChatFile(BaseModel):
    """A file uploaded to or generated by a chat."""
    id: str
    name: str
    size: int
    date: datetime


class ChatMessage(BaseModel):
    """A message in a chat, to show the tools used and the results."""
    id: str
    role: str
    content: str
    disclaimer: Optional[str]
    is_error: bool
    is_tool: bool
    created_at: datetime
    files: List[ChatFile]


class ChatResult(BaseModel):
    """The result of a chat prompt, including the response, context, messages, and files."""
    response: str
    context: str
    messages: List[ChatMessage]
    files: List[ChatFile]

    @classmethod
    def from_response(cls, content: str):
        response = ''
        context = ''
        files = []
        messages = []
        for chunk in content.split('\r\n\r\n'):
            if not chunk:
                continue
            lines = chunk.split('\n')
            event = lines[0].split(':', 1)[1].strip()
            if event == 'message':
                message: dict = json.loads(lines[1].split(':', 1)[1].strip())
                message_files = message.get('files', [])
                for message_file in message_files:
                    for file in files:
                        if file.get('id') == message_file.get('id'):
                            break
                    else:
                        files.append(message_file)
                messages.append(message)
            elif event == 'context':
                context = lines[1].split(':', 1)[1].strip()
        if messages:
            response = messages[-1]['content']
        return cls(response=response, context=context, messages=messages, files=files)


class DataTableOperation(BaseModel):
    """A step in a data context operation, working towards the goal."""
    log: str
    output: str
    tool: str
    tool_input: str
    type: str


class DataTableModification(BaseModel):
    """An operation in a data context, with a goal and a series of steps."""
    goal: str
    steps: List[DataTableOperation]


class DataTable(BaseModel):
    """The data context for a chat, including the current table and any intermediate steps."""
    id: int
    page: int
    total: int
    pages: int
    name: str
    modifications: Optional[List[DataTableModification]] = []
    table: List[dict]

    @property
    def dataframe(self):
        """Return the current table as a pandas DataFrame."""
        return pd.DataFrame(self.table)
