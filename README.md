# Challenge - Patent Analysis

## Measurement Extraction

## Flow Diagram

```mermaid
stateDiagram-v2
    [*] --> Type : Patent-document
    Type --> [*] : non-relevant
    Type --> Extraction : relevant
    Extraction --> chunking
    chunking --> LLM
    LLM --> measurements
    measurements --> property
    property --> values
    property --> units


```

### TodoList

- [] Understand the concept
- [x] One-Shot inference

## Acknowledgements

- [Matthew Shaxted](https://github.com/mattshax/ipagent) (Parser)
- [OpenAI](https://openai.com/) (provided helpful advise and chatgpt4 access)
