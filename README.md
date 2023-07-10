# Challenge - Patent Analysis

The purpose of this challenge is to address the issue of effectively extracting information from a given patent. Specifically, the challenge focuses on the extraction of product, component, or compound values and their corresponding units. Extracting this information accurately is crucial for understanding the patent's technical details and leveraging its insights for various applications. By developing innovative techniques and tools to automate the extraction process, this challenge aims to enhance efficiency and accessibility in patent analysis, thereby facilitating advancements in relevant industries and fostering intellectual property exploration.

## Table of Contents

- [Instructions for Use](#instructions-for-use)
  - [Clone the Repository and Install Python Dependencies](#clone-the-repository-and-install-python-dependencies)
  - [Acquiring the Data from USPTO](#acquiring-the-data-from-uspto)
  - [Parse the XML File to JSON File](#parse-the-xml-file-to-json-file)
  - [Environment Variables Setting for Azure OpenAI Setup](#environment-variables-setting-for-azure-openai-setup)
  - [Testing the System with Given Patent URL](#testing-the-system-with-given-patent-url)
- [Prerequisites](#prerequisites)
- [TodoList](#todolist)
- [Flow Diagram](#flow-diagram)
- [Data Description](#data-description)
- [System Architecture](#system-architecture)
- [Examples and Expected Output](#examples-and-expected-output)
- [Troubleshooting and FAQs](#troubleshooting-and-faqs)
- [Contributing](#contributing)
- [Contact Information](#contact-information)
- [Acknowledgements](#acknowledgements)

## Instructions for Use

### Clone the Repository and Install Python Dependencies

```bash
git clone https://github.com/rizwanishaq/basf_challenge.git
cd basf_challenge

# Python 3.10 is used for this project, although other versions could work as well but not tested

python3 -m venv basf
source basf/bin/activate

pip3 install -r requirements.txt
```

### Acquiring the Data from USPTO

```bash
mkdir data
cd data
wget https://bulkdata.uspto.gov/data/patent/grant/redbook/fulltext/2023/ipg230103.zip
unzip ipg230103.zip
```

### Parse the XML File to JSON File

```bash
python3 parse_data.py
```

This will create the `ipg230103.json` file in the data folder, which we can use afterwards for our system testing purposes.

### Environment Variables Setting for Azure OpenAI Setup

Before testing the patent-analysis system, we need to set the environment variable first. Create a `.env` file:

```bash
touch .env
```

Write your credentials in the `.env` file:

```plaintext
OPENAI_API_TYPE=azure
OPENAI_API_KEY="put your open api key here"
OPENAI_API_BASE="put the end point url here"
OPENAI_API_VERSION = 2023-03-15-preview
```

### Testing the System with Given Patent URL

```bash
python3 app.py --patent-url "https://patents.google.com/patent/US8022010B2/en"
```

This will generate the output like this

```plaintext
Product: TiN film
Property: average film thickness
Value: 3
unit: µm
sentence: The material in which a TiN film having an average film thickness of 3 µm had been formed on the surface of Present product 1 was made Present product 17, and the material in which a TiAlN film having an average film thickness of 3 µm had been formed on the surface of Present product 1 was made Present product 18.
```

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

## TodoList

- [x] Understand the concept
- [x] Few-Shot inference
- [x] Prototype
- [x] Flow Diagram
- [ ] Measurement database, MongoDB
- [x] Slides
- [ ] suggestions
- [ ] Optimization of validation
- [ ] Annotations generation
- [ ] Evaluation of the System

## Prerequisites

- Python 3.10
- Other dependencies listed in requirements.txt

## Data Description

The data for this challenge is obtained from the USPTO (United States Patent and Trademark Office). It is in the form of XML files, which need to be parsed and converted into JSON format for further processing.

## System Architecture

The patent analysis system follows the following flow:

1.  Type Classification: Determine the relevance of the patent document based on keywords and classification.

2.  Extraction: Extract relevant information from the document, including abstract and description sections.

3.  Chunking: Chunk the extracted information for further analysis.

4.  Language Model Inference: Use OpenAI's language model for few-shot inference to generate insights.

5.  Measurement Extraction: Extract measurements, properties, values, and units from the generated insights.

## Examples and Expected Output

Here are a few more examples of patent URLs and their expected output:

- Patent URL: https://patents.google.com/patent/US8501236B2/en

---

```diff
+ Product: ceria particles in red
+ Property: crystallite size in green
+ Value: between 10 and 20
+ Unit: nm
+ Sentence: In one embodiment, the nitrogen oxide storage material comprises alkaline earth material supported on ceria particles having a crystallite size of between about 10 and 20 nm and the alkaline earth oxide having a crystallite size of between about 20-40 nm.
```

---

```diff
+ Product: ALKAINE EARTH MATERIAL
+ Property: crystallite size
+ Value: between 10 and 20
+ unit: nm
+ sentence: In one embodiment, the nitrogen oxide storage material comprises alkaline earth material supported on ceria particles having a crystallite size of between about 10 and 20 nm and the alkaline earth oxide having a crystallite size of between about 20-40 nm.
```

---

```diff
+ Product: ALKAINE EARTH OXIDE
+ Property: crystallite size
+ Value: between 20-40
+ unit: nm
+ sentence: In one embodiment, the nitrogen oxide storage material comprises alkaline earth material supported on ceria particles having a crystallite size of between about 10 and 20 nm and the alkaline earth oxide having a crystallite size of between about 20-40 nm.
```

---

```diff
- Product: BaCO3/CeO2 composite
- Property: SEM image
- Value: null
- unit: null
- sentence: FIG. 6 is a SEM image of the spray dried and calcined BaCO3/CeO2 composite material.
```

---

```diff
- Product: BaCO3
- Property: thermal stress reduction
- Value: reduced
- unit:
- sentence: According to one or more embodiments of the invention, Ba sintering and Ba composite compound formation is reduced under the conditions of thermal stress in an exhaust gas of a lean burn engine.
```

---

```diff
- Product: NOX STORAGE MATERIAL
- Property: demonstrated NOx storage capacity
- Value: improved
- unit:
- sentence: The NOx storage material according to embodiments of the present invention demonstrates improved NOx storage capacity after thermal aging when used in a catalytic trap.
```

---

```diff
+ Product: BACO3/Ceo2 PARTICLES
+ Property: particle size
+ Value: 3-30
+ unit: micron
+ sentence: The coating on the honeycomb catalyst comprises about 3-30 micron BaCO3/CeO2 particles and about 1-20 micron alumina particles.
```

---

```diff
+ Product: ALUMINA PARTICLES
+ Property: particle size
+ Value: 1-20
+ unit: micron
+ sentence: The coating on the honeycomb catalyst comprises about 3-30 micron BaCO3/CeO2 particles and about 1-20 micron alumina particles.
```

---

```diff
- Product: NOX
- Property: NOx storage mass(g)
- Value: NOx *{dot over (V)}/V ideal *M S*1/(3.6*106)
- unit: g
- sentence: NOx storage mass in g is calculated via equation (2):
```

---

```diff
+ Product: NOX
+ Property: NOx concentration
+ Value: NOx
+ unit: ppm
+ sentence: For the time period of the 10 lean/rich cycles the NOx efficiency (U) is calculated from the NOx inlet and NOx outlet concentrations via equation (1):
```

---

```diff
+ Product: REFRACTORY OXIDE
+ Property: surface area
+ Value: between 5 and 350
+ unit: m2/g
+ sentence: The method of claim 13, wherein the refractory oxide has a surface area of between about 5 and about 350 m2/g.
```

---

- Patent URL: https://patents.google.com/patent/EP2778146A1/en

---

```diff
+ Product: CUBIC BORON NITRIDE
+ Property: average grain size
+ Value: 0.5 to 5
+ unit: µm
+ sentence: An average grain size of the cubic boron nitride of the present invention is not particularly limited, but if the average grain size of the cubic boron nitride is less than 0.5 µm, an oxygen amount adsorbed on the surface of the cubic boron nitride is increased to inhibit the sintering reaction, whereby sinterability tends to be lowered, while if the average grain size becomes large exceeding 5 µm, the binder phase tends to be agglomerated, so that the thickness of the binder phase which is brittle as compared to the cubic boron nitride becomes large and fracture resistance tends to be lowered. Therefore, the average grain size of the cubic boron nitride of the present invention is preferably 0.5 to 5 µm. Among these, the average grain size of the cubic boron nitride is further preferably 1 to 3 µm.
```

---

```diff
+ Product: CUBIC BORON NITRIDE SINTERED BODY
+ Property: inevitable impurities
+ Value: 5% by mass or less
+ unit:
+ sentence: The total amount of the inevitable impurities is generally 5% by mass or less based on the total mass of the cubic boron nitride sintered body
```

---

```diff
+ Product: CUBIC BORON NITRIDE SINTERED BODY
+ Property: tungsten element
+ Value: 5% by mass or less
+ unit:
+ sentence: Therefore, the amount of the tungsten element contained in the cubic boron nitride sintered body of the present invention is preferably 5% by mass or less based on the total mass of the cubic boron nitride sintered body since cutting properties are improved, and among these, the amount of the tungsten element is further preferably 3% by mass or less.
```

---

```diff
+ Product: CUBIC BORON NITRIDE
+ Property: average grain size
+ Value: 0.5 to 5
+ unit: µm
+ sentence: Therefore, the average grain size of the cubic boron nitride of the present invention is preferably 0.5 to 5 µm.
```

---

```diff
+ Product: CNGA120408
+ Property: insert shape
+ Value: None
+ sentence: Insert shape: CNGA120408,
```

---

```diff
- Product: DCLNR2525M12
- Property: holder
- Value: None
- unit: None
- sentence: Holder: DCLNR2525M12,
```

---

```diff
- Product: None
- Property: cutting speed
- Value: 300
- unit: m/min
- sentence: Cutting speed: 300 m/min,
```

---

```diff
- Product: None
- Property: amount of depth of cut
- Value: 0.2
- unit: mm
- sentence: Amount of depth of cut: 0.2 mm,
```

---

```diff
- Product: None
- Property: feed rate
- Value: 0.1
- unit: mm/rev
- sentence: Feed rate: 0.1 mm/rev,
```

---

```diff
+ Product: CUBIC BORON NITRIDE
+ Property: average grain size
+ Value: 0.5 to 5
+ unit: µm
+ sentence: Therefore, the average grain size of the cubic boron nitride of the present invention is preferably 0.5 to 5 µm.
```

---

## Troubleshooting and FAQs

I'm encountering a request timeout problem with Azure OpenAI when using the extracted data in JSON format from the .xml files. As a solution, I tested the system with different patent URLs.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please submit a pull request or open an issue in the [GitHub repository](https://github.com/rizwanishaq/basf_challenge).

## Contact Information

For further information or inquiries, please contact [Rizwan Ishaq](mailto:rizwanishaq@gmail.com)

## Acknowledgements

- [Matthew Shaxted](https://github.com/mattshax/ipagent) (Parser)
- [OpenAI](https://openai.com/) (provided helpful advise and chatgpt4 access)
