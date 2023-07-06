# Challenge - Patent Analysis

## Measurement Extraction

## Flow Diagram

```mermaid
stateDiagram-v2
    [*] --> Type : Patent-document
    Type --> [*] : non_relevant
    Type --> Extraction : relevant
    state Type {
        keywords --> classification
        classification --> non_relevant
        classification --> relevant
    }

    Extraction --> chunking
    state Extraction {
        document --> abstract
        document --> description
        abstract --> concatenate
        description --> concatenate
    }

    chunking --> LLM
    state LLM {
        few_shots_inference --> OpenAI
    }

    LLM --> measurements
    state measurements {
        property --> values
        property --> units
    }
    measurements --> values
    measurements --> units



```

## Validation

- [] using the chroma db vector database, and compare the results with each vector so that we can have close score, i.e. that it is in the text.

### TodoList

- [x] Understand the concept
- [x] Few-Shot inference
- [] Validation

## Acknowledgements

- [Matthew Shaxted](https://github.com/mattshax/ipagent) (Parser)
- [OpenAI](https://openai.com/) (provided helpful advise and chatgpt4 access)
