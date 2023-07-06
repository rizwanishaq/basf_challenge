# Challenge - Patent Analysis

## Measurement Extraction

## Flow Diagram

```mermaid
stateDiagram-v2 LR
    [*] --> Type : Patent-document
    Type --> [*] : non-relevant
    Type --> Extraction : relevant

    Extraction --> chunking
    state Extraction {
        document --> abstract
        document --> description
        abstract --> concatenate
        description --> concatenate
    }

    chunking --> LLM
    state LLM {
        one_shot_inference --> OpenAI
    }

    LLM --> measurements
    state measurements {
        property --> values
        property --> units
    }
    measurements --> values
    measurements --> units




```

### TodoList

- [] Understand the concept
- [x] One-Shot inference

## Acknowledgements

- [Matthew Shaxted](https://github.com/mattshax/ipagent) (Parser)
- [OpenAI](https://openai.com/) (provided helpful advise and chatgpt4 access)
