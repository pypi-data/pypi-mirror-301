import typing
import uuid
import datetime as dt
from enum import Enum

from .api_client import (
    TraceResponse,
    User,
    Metadata
)

class EventType(Enum):
    """Enum representing different types of events."""
    RETRIEVAL = "retrieval"
    GENERATION = "generation"
    ROUTER = "router"
    SYSTEM = "system"
    CUSTOM = "event"


class Trace:
    """
    Represents a trace in the NeuralTrust system.
    """

    def __init__(self, client, trace_id: str = None, conversation_id: str = None, channel_id: str = None, session_id: str = None, user: typing.Optional[User] = None, metadata: typing.Optional[Metadata] = None, custom: typing.Optional[dict] = None):
        """
        Initialize a new Trace object.

        Args:
            client (NeuralTrust): The NeuralTrust client.
            trace_id (str): The unique identifier for this trace.
            conversation_id (str, optional): The conversation ID. If not provided, a new UUID will be generated.
            channel_id (str, optional): The channel ID.
            session_id (str, optional): The session ID.
            user (User, optional): The user associated with the trace.
            metadata (Metadata, optional): Additional metadata for the trace.
            custom (dict, optional): Custom data to include with the trace.
        """
        self.client = client
        self.conversation_id = conversation_id or str(uuid.uuid4())
        self.session_id = session_id
        self.interaction_id = trace_id or str(uuid.uuid4())
        self.channel_id = channel_id
        self.user = user
        self.metadata = metadata
        self.custom = custom
        self.start_timestamp = None
        self.end_timestamp = None
        self.input = None
        self.output = None
        self.task = None

    def retrieval(self, input: str):
        """
        Start a retrieval trace.

        Args:
            input (str): The input for the retrieval task.

        Returns:
            Trace: The current Trace object.
        """
        self.input = input
        self.task = EventType.RETRIEVAL.value
        self.start_timestamp = int(dt.datetime.now().timestamp())
        return self

    def generation(self, input: str):
        """
        Start a generation trace.

        Args:
            input (str): The input for the generation task.

        Returns:
            Trace: The current Trace object.
        """
        self.input = input
        self.task = EventType.GENERATION.value
        self.start_timestamp = int(dt.datetime.now().timestamp())
        return self

    def router(self, input: str):
        """
        Start a router trace.

        Args:
            input (str): The input for the router task.

        Returns:
            Trace: The current Trace object.
        """
        self.input = input
        self.task = EventType.ROUTER.value
        self.start_timestamp = int(dt.datetime.now().timestamp())
        return self

    def event(self, input: str):
        """
        Record an event trace.

        Args:
            input (str): The input for the event.
        """
        self.input = input
        self.task = EventType.CUSTOM.value
        self.start_timestamp = int(dt.datetime.now().timestamp())
        self._send_trace()

    def system(self, input: str|object):
        """
        Record a system trace.

        Args:
            input (str|object): The input for the system trace. If not a string, it will be converted to a string.
        """
        self.input = str(input)
        self.task = EventType.SYSTEM.value
        self.start_timestamp = int(dt.datetime.now().timestamp())
        self.end_timestamp = int(dt.datetime.now().timestamp())
        self._send_trace()

    def end(self, output: str|object):
        """
        End the current trace and record the output.

        Args:
            output (str|object): The output of the trace. If not a string, it will be converted to a string.
        """
        self.output = str(output)
        self.end_timestamp = int(dt.datetime.now().timestamp())
        self._send_trace()
    
    def send(
        self,
        event_type: EventType,
        input: str,
        output: str = None,
        latency: int = None,
        start_timestamp: int = None,
        end_timestamp: int = None
    ) -> TraceResponse:
        """
        Send an atomic event to NeuralTrust.

        Args:
            event_type (EventType): The type of the event.
            input (str): The input data for the event.
            output (str, optional): The output data for the event.
            start_timestamp (int, optional): The start timestamp of the event in milliseconds. If not provided, the current time will be used.
            end_timestamp (int, optional): The end timestamp of the event in milliseconds. If not provided, the current time will be used.

        Returns:
            TraceResponse: The response from the API.
        """
        current_time = int(dt.datetime.now().timestamp())

        if start_timestamp is None:
            start_timestamp = current_time
        if end_timestamp is None:
            end_timestamp = current_time

        self.task = event_type.value
        self.input = str(input)
        self.output = str(output)
        self.latency = latency
        self.start_timestamp = start_timestamp
        self.end_timestamp = end_timestamp
        self._send_trace()
    
    def _send_trace(self):
        """
        Internal method to send the trace to the API.
        """
        self.client._trace(
            type="traces",
            conversation_id=self.conversation_id,
            session_id=self.session_id,
            channel_id=self.channel_id,
            interaction_id=self.interaction_id,
            user=self.user,
            metadata=self.metadata,
            input=self.input,
            output=self.output,
            task=self.task,
            latency=self.latency,
            custom=str(self.custom),
            start_timestamp=self.start_timestamp * 1000,
            end_timestamp=self.end_timestamp * 1000
        )
        self.input = None
        self.output = None
        self.task = None
        self.start_timestamp = None
        self.end_timestamp = None