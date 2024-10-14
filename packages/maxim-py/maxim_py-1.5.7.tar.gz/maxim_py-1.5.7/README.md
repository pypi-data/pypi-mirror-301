# Maxim SDK

<div style="display: flex; justify-content: center; align-items: center;margin-bottom:20px;">
<img src="https://cdn.getmaxim.ai/third-party/sdk.png">
</div>

This is Python SDK for enabling Maxim observability. [Maxim](https://www.getmaxim.ai?ref=npm) is an enterprise grade evaluation and observability platform.

## How to integrate

### Install

```
pip install maxim-py
```

### Initialize Maxim logger

```python
from maxim.maxim import Maxim

maxim = Maxim(Config(apiKey=apiKey))
```

### Start sending traces

```python
from maxim.logger.logger import LoggerConfig
# Initializing logger
logger = maxim.logger(LoggerConfig(id="log-repository-id"))
# Initializing a new trace
trace = logger.trace(TraceConfig(id="trace-id",name="trace-name",tags={"key":"value"}))
# Creating the generation
generation = trace.generation(GenerationConfig(id=str(uuid4()), model="text-davinci-002", provider="azure", model_parameters={"temperature": 0.7, "max_tokens": 100}))
# Making LLM call
completion = self.client.completions.create(
   model="text-davinci-002",
   prompt="Translate the following English text to French: 'Hello, how are you?'",
   max_tokens=100,
   temperature=0.7
)
# Updating generation
generation.result(completion)
# Ending trace
trace.end()
```

## Integrations with other frameworks

### Langchain

We have built in Langchain tracer support

```python
logger = self.maxim.logger(LoggerConfig(id=repoId))
trace_id = str(uuid4())
trace = logger.trace(TraceConfig(
   id=trace_id, name="pre-defined-trace"))

model = OpenAI(callbacks=[MaximLangchainTracer(logger)],api_key=openAIKey)
messages = [
   (
         "system",
         "You are a helpful assistant that translates English to French. Translate the user sentence.",
   ),
   ("human", "I love programming."),
]
model.invoke(messages, config={
   "metadata": {
         "maxim": {
            "trace_id": trace_id,
            "generation_name": "get-answer",
            "generation_tags": {
               "test": "123"
            }
         }
   }
})
trace.event(id=str(uuid4()), name="test event")
trace.end()
```

#### Langchain module compatibility

| | Anthropic | Bedrock Anthropic | Bedrock Meta | OpenAI | Azure |
|---|---|---|---|---|---|
|Chat (0.3.x) | ✅ | ✅ | ✅ | ✅ | ✅ |
|Chat (0.1.x) | ✅ | ✅ | ✅ | ✅ | ✅ |
|Tool call (0.3.x)| ✅ |✅ |❓| ✅ | ✅ |
|Tool call (0.1.x) | ✅ | ✅ | ✅ | ✅ | ✅ |
|Chain (via LLM) (0.3.x)| ✅ | ✅ | ✅ | ✅ | ✅ |
|Chain (via LLM) (0.1.x)| ✅ | ✅ | ✅ | ✅ | ✅ |
|Streaming (0.3.x)| ✅  | ✅  |✅ | ✅ | ✳️ Token usage is not supported by Langchain    |
|Streaming (0.1.x) Token usage is not supported by Langchain| ✳️   | ✳️ | ✳️  | ✳️ | ✳️     |
|Agent (0.3.x)|⛔️ |⛔️ |⛔️ | ⛔️| ⛔️|
|Agent (0.1.x)|⛔️ |⛔️ |⛔️ | ⛔️| ⛔️|

> Please reach out to us if you need support for any other package + provider + classes.

## Version changelog

### v1.5.7

- Feature - Supports 0.1.x langchain

### v1.5.6

- Improvement - Improved langchain support

### v1.5.5

- Improvement - Improves cleanups for log writer for quick returns.

### v1.5.4

- Improvement - Improved fs access checks.
- Improvement - Fixes threading locks for periodic syncs in Python3.9

### v1.5.3

- Improvement - Adds lambda env support for SDK with no access to filesystem.

### v1.5.2

- Feature - Adds support to new langchain_openai.AzureChatOpenAI class in langchain tracer

### v1.5.1

- Fix - Adds Python 3.9 compatibility

### v1.5.0

- Improvement - Updates connection pool to use session that enforces re-connects before making API calls.

### v1.4.5

- Improvement - Adds backoff retries to failed REST calls.

### v1.4.4

- Improvement - langchain becomes optional dependency

### v1.4.3

- Fix - connection pooling for network calls.
- Fix - connection close issue.

### v1.4.2 (🚧 Yanked)

- Fix - connection close issue

### v1.4.1

- Adds validation for provider in generation

### v1.4.0

- Now generation.result accepts
  - OpenAI chat completion object
  - Azure OpenAI chat completion object
  - Langchain LLMResult, AIMessage object

### v1.3.4

- Fixes message_parser

### v1.3.2

- Fixes utility function for langchain to parse AIMessage into Maxim logger completion result

### v1.3.1

- Adds tool call parsing support for Langchain tracer

### v1.3.0

- Adds support for ChatCompletion in generations
- Adds type safety for retrieval results

### v1.2.7

- Bug fix where input sent with trace.config was getting overridden with None

### v1.2.6

- Adds `trace.set_input` and `trace.set_output` methods to control what to show in logs dashboard

### v1.2.5

- Removes one no_op command while creating spans
- Minor bug fixes

### v1.2.1

- Fixed MaximLangchainTracer error logging flow.

### v1.2.0

- Adds langchain support
- Adds local parsers to validate payloads on client side

### v1.1.0

- Minor bug fixes around log writer cleanup

### v1.0.0

- Public release
