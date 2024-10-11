# NeuralTrust Python SDK

The NeuralTrust Python SDK provides a convenient way to interact with the NeuralTrust API for tracing, evaluation sets, knowledge bases, and testsets.

## Installation

You can install the NeuralTrust Python SDK using pip:

```bash
pip install neuraltrust
```

## Usage

To use the NeuralTrust Python SDK, you need to initialize the client with your API key:

```python
from neuraltrust import NeuralTrust

# Initialize the client with your API key
client = NeuralTrust(api_key="your_api_key_here")

# Optionally, you can specify a custom base URL and SDK version
client = NeuralTrust(api_key="your_api_key_here", base_url="https://custom.api.url", sdk_version="v2")
```

### Tracing

```python
# Create a trace
trace = client.trace(trace_id="trace_1234", conversation_id="conversation_1234", session_id="session_1234", channel_id="channel_1234")

# Add events to the trace
trace.retrieval("What's the weather like today?")
# Rest of your code and the end you call the end method
trace.end([{"chunk": "The weather today is sunny with a high of 75°F.", "score": 0.95}])

# There is another method to send the trace in an atomic way
trace.send(
    event_type=EventType.RETRIEVAL, 
    input="What's the weather like today?", 
    output=[{"chunk": "The weather today is sunny with a high of 75°F.", "score": 0.95}], 
    latency=100
)
```

### Evaluation Sets

```python
# Run evaluation set
eval_set = client.run_evaluation_set(id="eval_set_id")

# Create an evaluation set
eval_set = client.create_evaluation_set(name="My Eval Set", description="A test evaluation set")

# Get an evaluation set
eval_set = client.get_evaluation_set(id="eval_set_id")

# Delete an evaluation set
client.delete_evaluation_set(id="eval_set_id")
```

### Knowledge Bases

```python
# Create a knowledge base
kb = client.create_knowledge_base(type="upstash", credentials={"api_key": "your_doc_api_key"})

# Get a knowledge base
kb = client.get_knowledge_base(id="kb_id")

# Delete a knowledge base
client.delete_knowledge_base(id="kb_id")
```

### Testsets

```python
# Create a testset
testset = client.create_testset(name="My Testset", type="adversarial", evaluation_set_id="eval_set_id", knowledge_base_id="kb_id", num_questions=10)

# Get a testset
testset = client.get_testset(id="testset_id")

# Delete a testset
client.delete_testset(id="testset_id")
```

## Configuration

You can configure the SDK using environment variables:

- `NEURALTRUST_API_KEY`: Your NeuralTrust API key
- `NEURALTRUST_BASE_URL`: Custom base URL for the API (optional)

## Advanced Usage

### Custom Metadata and User Information

```python
from neuraltrust import User, Metadata

user = User(id="user123", name="John Doe")
metadata = Metadata(app_version="1.0.0", platform="web")

trace = client.trace(user=user, metadata=metadata)
```

### Asynchronous Tracing

The SDK uses a `ThreadPoolExecutor` for asynchronous tracing. You can adjust the number of workers:

```python
client = NeuralTrust(api_key="your_api_key_here", max_workers=10)
```

## Error Handling

The SDK will raise exceptions for API errors. Make sure to handle these appropriately in your application.

## Contributing

Contributions to the NeuralTrust Python SDK are welcome! Please refer to the contribution guidelines for more information.

## License

This SDK is distributed under the [MIT License](LICENSE).


