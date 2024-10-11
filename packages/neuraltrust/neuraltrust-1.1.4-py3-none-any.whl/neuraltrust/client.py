import typing
import os
from concurrent.futures import ThreadPoolExecutor
from enum import Enum
from .api_client import (
    NeuralTrustApi,
    TraceResponse,
    TraceTask,
    User,
    Metadata
)
from .trace import Trace
from .api_client.knowledge_base.client import KnowledgeBaseClient
from .api_client.evaluation_set.client import EvaluationSetClient
from .api_client.testset.client import TestsetClient

OMIT = typing.cast(typing.Any, ...)

DEFAULT_BASE_URL = "https://api.neuraltrust.ai"

class EventType(Enum):
    """Enum representing different types of events."""
    RETRIEVAL = "retrieval"
    GENERATION = "generation"
    ROUTER = "router"
    SYSTEM = "system"
    CUSTOM = "event"


class NeuralTrust:
    base_client: NeuralTrustApi
    executor: ThreadPoolExecutor

    def __init__(
        self,
        api_key: typing.Union[str, None] = None,
        base_url: typing.Union[str, None] = None,
        sdk_version: typing.Union[str, None] = 'v1',
        timeout: typing.Union[float, None] = None,
        max_workers: typing.Union[int, None] = 5,
    ) -> None:
        
        if not api_key:
            api_key = os.environ.get("NEURALTRUST_API_KEY")
        
        if not base_url:
            base_url = os.environ.get("NEURALTRUST_BASE_URL") or DEFAULT_BASE_URL
        
        self.trace_executor = ThreadPoolExecutor(max_workers=max_workers)
        self.base_client = NeuralTrustApi(
            api_key=api_key, base_url=f"{base_url}/{sdk_version}", timeout=timeout
        )
        # set base URL
        if base_url:
            self.base_client._client_wrapper._base_url = f"{base_url}/{sdk_version}"
    @property
    def api_key(self) -> typing.Union[str, None]:
        """Property getter for api_key."""
        return self.base_client._client_wrapper.api_key

    @api_key.setter
    def api_key(self, value: typing.Union[str, None]) -> None:
        """Property setter for api_key."""
        self.api_key = value
        if value is not None:
            self.base_client._client_wrapper.api_key = value

    @property
    def base_url(self) -> typing.Union[str, None]:
        """Property getter for base_url."""
        return self.base_client._client_wrapper._base_url

    @base_url.setter
    def base_url(self, value: typing.Union[str, None]) -> None:
        """Property setter for base_url."""
        if value is not None:
            self.base_client._client_wrapper._base_url = value

    def trace(self, trace_id: str = None, conversation_id: str = None, session_id: str = None, channel_id: str = None, user: User = None, metadata: Metadata = None, custom: dict = None):
        """
        Create a new Trace object.

        Args:
            conversation_id (str, optional): The conversation ID. If not provided, a new UUID will be generated.
            session_id (str, optional): The session ID.
            channel_id (str, optional): The channel ID.
            user (User, optional): The user associated with the trace.
            metadata (Metadata, optional): Additional metadata for the trace.
            custom (dict, optional): Custom data to include with the trace.

        Returns:
            Trace: A new Trace object.
        """
        return Trace(client=self, trace_id=trace_id, conversation_id=conversation_id, session_id=session_id, channel_id=channel_id, user=user, metadata=metadata, custom=custom)
    
    def _trace(
        self,
        *,
        type: typing.Optional[str] = OMIT,
        task: typing.Optional[TraceTask] = OMIT,
        input: typing.Optional[str] = OMIT,
        output: typing.Optional[str] = OMIT,
        user: typing.Optional[User] = OMIT,
        metadata: typing.Optional[Metadata] = OMIT,
        session_id: typing.Optional[str] = OMIT,
        channel_id: typing.Optional[str] = OMIT,
        conversation_id: typing.Optional[str] = OMIT,
        interaction_id: typing.Optional[str] = OMIT,
        latency: typing.Optional[int] = OMIT,
        start_timestamp: typing.Optional[int] = OMIT,
        end_timestamp: typing.Optional[int] = OMIT,
        custom: typing.Optional[str] = OMIT
    ) -> TraceResponse:
        """
        Internal method to send a trace to the API.

        Args:
            type (str, optional): The type of the trace.
            task (TraceTask, optional): The task associated with the trace.
            input (str, optional): The input data for the trace.
            output (str, optional): The output data for the trace.
            user (User, optional): The user associated with the trace.
            metadata (Metadata, optional): Additional metadata for the trace.
            session_id (str, optional): The session ID.
            channel_id (str, optional): The channel ID.
            conversation_id (str, optional): The conversation ID.
            interaction_id (str, optional): The interaction ID.
            latency (int, optional): The latency of the trace.
            start_timestamp (int, optional): The start timestamp of the trace.
            end_timestamp (int, optional): The end timestamp of the trace.
            custom (str, optional): Custom data to include with the trace.

        Returns:
            TraceResponse: The response from the API.
        """
        return self.trace_executor.submit(
            self.base_client.trace.trace,
            type=type,
            task=task,
            input=input,
            output=output,
            user=user,
            metadata=metadata,
            session_id=session_id,
            channel_id=channel_id,
            conversation_id=conversation_id,
            interaction_id=interaction_id,
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp,
            latency=latency,
            custom=custom
        )


    def run_evaluation_set(self, id: str):
        return self.base_client.evaluation_set.run_evaluation_set(id=id)
    
    def create_evaluation_set(self, name: str = None, description: str = None, scheduler: str = None):
        return self.base_client.evaluation_set.create_evaluation_set(name=name, description=description, scheduler=scheduler)
    
    def get_evaluation_set(self, id: str):
        return self.base_client.evaluation_set.get_evaluation_set(id=id)
    
    def delete_evaluation_set(self, id: str):
        return self.base_client.evaluation_set.delete_evaluation_set(id=id)
    
    def create_knowledge_base(self, type: str = None, credentials: dict = None, seed_topics: list = None):
        return self.base_client.knowledge_base.create_knowledge_base(type=type, credentials=credentials, seed_topics=seed_topics)

    def get_knowledge_base(self, id: str):
        return self.base_client.knowledge_base.get_knowledge_base(id=id)
    
    def delete_knowledge_base(self, id: str):
        return self.base_client.knowledge_base.delete_knowledge_base(id=id)
    
    def create_testset(self, name: str = None, type: str = None, evaluation_set_id: str = None, knowledge_base_id: str = None, num_questions: int = None):
        return self.base_client.testset.create_testset(name=name, type=type, evaluation_set_id=evaluation_set_id, knowledge_base_id=knowledge_base_id, num_questions=num_questions)

    def get_testset(self, id: str):
        return self.base_client.testset.get_testset(id=id)
    
    def delete_testset(self, id: str):
        return self.base_client.testset.delete_testset(id=id)

