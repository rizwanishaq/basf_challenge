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

- Patent URL: https://patents.google.com/patent/US8501236B2/en
- Patent URL: https://patents.google.com/patent/EP2778146A1/en
- Patent Title: Highly reactive, dust-free and free-flowing lithium sulphide and method for the production

```bash
  python3 validate.py
```

<table>
  <tr >
    <th>Product</th>
    <th>Property</th>
    <th>Value</th>
    <th>Unit</th>
    <th>Sentence</th>
  </tr>
  <tr style="color:green">
    <td >ceria particles</td>
    <td >crystallite size</td>
    <td>between 10 and 20</td>
    <td>nm</td>
    <td>In one embodiment, the nitrogen oxide storage material comprises alkaline earth material supported on ceria particles having a crystallite size of between about 10 and 20 nm and the alkaline earth oxide having a crystallite size of between about 20-40 nm.</td>
  </tr>
  <tr style="color:green">
    <td >ALKAINE EARTH MATERIAL</td>
    <td>crystallite size</td>
    <td>between 20-40</td>
    <td>nm</td>
    <td>In one embodiment, the nitrogen oxide storage material comprises alkaline earth material supported on ceria particles having a crystallite size of between about 10 and 20 nm and the alkaline earth oxide having a crystallite size of between about 20-40 nm.</td>
  </tr>
  <tr style="color:green">
    <td >ALKAINE EARTH OXIDE</td>
    <td >crystallite size</td>
    <td>between 20-40</td>
    <td>nm</td>
    <td>In one embodiment, the nitrogen oxide storage material comprises alkaline earth material supported on ceria particles having a crystallite size of between about 10 and 20 nm and the alkaline earth oxide having a crystallite size of between about 20-40 nm.</td>
  </tr>
  <tr style="color:red">
    <td>BaCO3/CeO2 composite</td>
    <td>SEM image</td>
    <td>null</td>
    <td>null</td>
    <td>sentence: FIG. 6 is a SEM image of the spray dried and calcined BaCO3/CeO2 composite material.</td>
  </tr>
  <tr style="color:red">
    <td>BaCO3 OR MIXTURES OF BACO3 AND MGCO3 SUPPORTED ON CEO2 PARTICLES</td>
    <td>reduced Ba sintering and Ba composite compound formation under the conditions of thermal stress in an exhaust gas of a lean burn engine</td>
    <td></td>
    <td></td>
    <td>According to one or more embodiments of the invention, Ba sintering and Ba composite compound formation is reduced under the conditions of thermal stress in an exhaust gas of a lean burn engine.</td>
  </tr>
  <tr style="color:red">
    <td>NOX STORAGE MATERIAL</td>
    <td>demonstrated NOx storage capacity</td>
    <td>improved</td>
    <td></td>
    <td>The NOx storage material according to embodiments of the present invention demonstrates improved NOx storage capacity after thermal aging when used in a catalytic trap.</td>
  </tr>
  <tr style="color:green">
    <td>BACO3</td>
    <td>crystallite size</td>
    <td>between 20 and 40</td>
    <td>nm</td>
    <td>the resulting BaCO3 had a crystallite size of between about 20 and 40 nm.</td>
  </tr>
  <tr style="color:green">
    <td>CERIA</td>
    <td>BET surface area</td>
    <td>between 30 and 80</td>
    <td>m2/g</td>
    <td>The BET surface area of the particulate mixture is between about 30 and 80 m2/g.</td>
  </tr>
  <tr style="color:red">
    <td>NOx</td>
    <td>efficiency</td>
    <td>U</td>
    <td>None</td>
    <td>For the time period of the 10 lean/rich cycles the NOx efficiency (U) is calculated from the NOx inlet and NOx outlet concentrations via equation (1):</td>
  </tr>
  <tr style="color:green">
    <td>NOx storage mass</td>
    <td>mass</td>
    <td>NOx mass(g)</td>
    <td>g</td>
    <td>NOx storage mass in g is calculated via equation (2):</td>
  </tr>
  <tr style="color:green">
    <td>BACO3</td>
    <td>crystallite size</td>
    <td>20-50</td>
    <td>nm</td>
    <td>Furthermore, a BaCO3 crystallite size of between about 20-50 nm, for example, 45 nm, and a CeO2 crystallite size of between about 25-30 nm in combination with a sufficient BET surface area after aging yielded the highest NOx storage at 400° C.</td>
  </tr>
  <tr style="color:green">
    <td>CERIA</td>
    <td>crystal size</td>
    <td>10-20</td>
    <td>nm</td>
    <td>According to the data in Tables I and II, an as-prepared BET surface area between 40-60 m2/g and a ceria crystal size between about 10- and 20 nm and a BaCO3 crystallite size of between about 20- and 40 nm yielded the best performance after aging.</td>
  </tr>
  <tr style="color:green">
    <td>REFRACTORY OXIDE</td>
    <td>surface area</td>
    <td>between 5 and 350</td>
    <td>m2/g</td>
    <td>The method of claim 13, wherein the refractory oxide has a surface area of between about 5 and about 350 m2/g.</td>
  </tr>
  <tr style="color:green">
    <td>ALUMINA PARTICLES</td>
    <td>particle size</td>
    <td>1-20</td>
    <td>micron</td>
    <td>The coating on the honeycomb catalyst comprises about 3-30 micron BaCO3/CeO2 particles and about 1-20 micron alumina particles.</td>
  </tr>
  <tr style="color:green">
    <td>NOX</td>
    <td>NOx storage mass(g)</td>
    <td>NOx *{dot over (V)}/V ideal *M S*1/(3.6*10^6)</td>
    <td>g</td>
    <td>NOx storage mass in g is calculated via equation (2):</td>
  </tr>
  <tr style="color:green">
    <td>NOX</td>
    <td>NOx concentration</td>
    <td>NOx</td>
    <td>ppm</td>
    <td>For the time period of the 10 lean/rich cycles the NOx efficiency (U) is calculated from the NOx inlet and NOx outlet concentrations via equation (1):</td>
  </tr>
  <tr style="color:green">
    <td>REFRACTORY OXIDE</td>
    <td>surface area</td>
    <td>between 5 and 350</td>
    <td>m2/g</td>
    <td>The method of claim 13, wherein the refractory oxide has a surface area of between about 5 and about 350 m2/g.</td>
  </tr>

  <tr style="color:green">
    <td>CUBIC BORON NITRIDE</td>
    <td>volume</td>
    <td>85 to 95</td>
    <td>%</td>
    <td>The cubic boron nitride sintered body of the present invention is constituted by 85 to 95% by volume of cubic boron nitride based on the total volume of the cubic boron nitride sintered body, and 5 to 15% by volume of a binder phase and inevitable impurities based on the total mass of the cubic boron nitride sintered body, and is a cubic boron nitride sintered body in which the sum thereof is 100% by volume.</td>
  </tr>

  <tr style="color:green">
    <td>CUBIC BORON NITRIDE</td>
    <td>volume</td>
    <td>85 to 95</td>
    <td>%</td>
    <td>Among these, it is preferred that the cubic boron nitride is 89 to 95% by volume, and the remainder is the binder phase and inevitable impurities.</td>
  </tr>

  <tr style="color:green">
    <td>CUBIC BORON NITRIDE</td>
    <td>average grain size</td>
    <td>0.5 to 5</td>
    <td>µm</td>
    <td>An average grain size of the cubic boron nitride of the present invention is not particularly limited, but if the average grain size of the cubic boron nitride is less than 0.5 µm, an oxygen amount adsorbed on the surface of the cubic boron nitride is increased to inhibit the sintering reaction, whereby sinterability tends to be lowered, while if the average grain size becomes large exceeding 5 µm, the binder phase tends to be agglomerated, so that the thickness of the binder phase which is brittle as compared to the cubic boron nitride becomes large and fracture resistance tends to be lowered. Therefore, the average grain size of the cubic boron nitride of the present invention is preferably 0.5 to 5 µm. Among these, the average grain size of the cubic boron nitride is further preferably 1 to 3 µm.</td>
  </tr>
  <tr style="color:red">
    <td>CUBIC BORON NITRIDE SINTERED BODY</td>
    <td>inevitable impurities</td>
    <td>5% </td>
    <td>by mass</td>
    <td>The total amount of the inevitable impurities is generally 5% by mass or less based on the total mass of the cubic boron nitride sintered body</td>
  </tr>
  <tr style="color:red">
    <td>CUBIC BORON NITRIDE SINTERED BODY</td>
    <td>tungsten element</td>
    <td>5 </td>
    <td>% by mass</td>
    <td>Therefore, the amount of the tungsten element contained in the cubic boron nitride sintered body of the present invention is preferably 5% by mass or less based on the total mass of the cubic boron nitride sintered body since cutting properties are improved, and among these, the amount of the tungsten element is further preferably 3% by mass or less.</td>
  </tr>
  <tr style="color:green">
    <td>CUBIC BORON NITRIDE</td>
    <td>average grain size</td>
    <td>0.5 to 5</td>
    <td>µm</td>
    <td>Therefore, the average grain size of the cubic boron nitride of the present invention is preferably 0.5 to 5 µm.</td>
  </tr>
   <tr style="color:green">
    <td>CUBIC BORON NITRIDE</td>
    <td>average grain size</td>
    <td>2</td>
    <td>µm</td>
    <td>Cubic boron nitride (hereinafter referred to as cBN.) powder having an average grain size of 2 µm, Cr powder having an average grain size of 4.9 µm, Cr2N powder having an average grain size of 3.0 µm, Cr3C2 powder having an average grain size of 2.7 µm, VC powder having an average grain size of 2.7 µm, Mo2C powder having an average grain size of 2.5 µm, TiN powder having an average grain size of 1.8 µm, WC powder having an average grain size of 2.2 µm, Co powder having an average grain size of 0.9 µm, and scaly aluminum (Al) powder having an average grain size of 20µm were prepared, and formulated to a formulation composition shown in Table 1.</td>
  </tr>
  <tr style="color:red">
    <td>Sample No.</td>
    <td>Formulated composition (% by volume)</td>
    <td>90cBN-4Cr2N-4Co-2Al</td>
    <td>None</td>
    <td>[Table 1]   Sample No. Formulated composition (% by volume)    Present products 1 90cBN-4Cr2N-4Co-2Al   2 90cBN-4Cr3C2-4Co-2Al   3 90cBN-4VC-4Co-2Al   4 90cBN-4Mo2C-4Co-2Al   Comparative products 5 90cBN-8TiN-2Al   6 90cBN-4Cr2N-4WC-2Al   7 90cBN-8Cr2N-2Al   8 90cBN-4Cr-4Co-2Al</td>
  </tr>
  <tr style="color:red">
    <td>CNGA120408</td>
    <td>insert shape</td>
    <td>None</td>
    <td></td>
    <td>Insert shape: CNGA120408</td>
  </tr>
  <tr style="color:red">
    <td>DCLNR2525M12</td>
    <td>holder</td>
    <td>None</td>
    <td>None</td>
    <td>Holder: DCLNR2525M12</td>
  </tr>
  <tr style="color:red">
    <td>None</td>
    <td>Cutting speed</td>
    <td>300</td>
    <td>m/min</td>
    <td>Cutting speed: 300 m/min</td>
  </tr>
  <tr style="color:green">
    <td>CUBIC BORON NITRIDE</td>
    <td>average grain size</td>
    <td>0.5 to 5</td>
    <td>µm</td>
    <td>Therefore, the average grain size of the cubic boron nitride of the present invention is preferably 0.5 to 5 µm.</td>
  </tr>
  <tr style="color:green">
    <td>LITHIUM SULFIDE POWDER</td>
    <td>particle size</td>
    <td>between 250 and 1,500</td>
    <td>µm</td>
    <td>The invention relates to a highly reactive, high-purity, free-flowing and dust-free lithium sulfide powder having an average particle size between 250 and 1,500 μm and BET surface areas between 1 and 100 m2/g.</td>
  </tr>
  <tr style="color:green">
    <td>LITHIUM SULFIDE POWDER</td>
    <td>surface area</td>
    <td>between 1 and 100</td>
    <td>m2/g</td>
    <td>The invention relates to a highly reactive, high-purity, free-flowing and dust-free lithium sulfide powder having an average particle size between 250 and 1,500 μm and BET surface areas between 1 and 100 m2/g.</td>
  </tr>
  <tr style="color:green">
    <td>LITHIUM HYDROXIDE</td>
    <td>residual water content</td>
    <td>less than 5</td>
    <td>wt. %</td>
    <td>Surprisingly, however, the morphology of the produced anhydrous lithium hydroxide (residual water content of less than 5 wt. %) differs significantly depending on the selected drying conditions.</td>
  </tr>
  <tr style="color:green">
    <td>LITHIUM HYDROXIDE</td>
    <td>BET surface area</td>
    <td>smaller for low drying temperatures than for temperatures above 200</td>
    <td>°C. %</td>
    <td>This property correlates with the BET surface area of the porous lithium hydroxide particles, which is smaller for low drying temperatures than for temperatures above 200° C. (Examples 1, 2, 5 and 6).</td>
  </tr>
  <tr style="color:green">
    <td>LI6PS5BR</td>
    <td>composition</td>
    <td>slithium sulfide</td>
    <td>%</td>
    <td>To study reactivity of the produced lithium sulfide powders, a process for producing the sulfidic solid electrolyte of the composition Li6PS5Br was found in the literature [Solid State Ionics, 2014, 262, 183-187].</td>
  </tr>
  <tr style="color:red">
    <td></td>
    <td>reaction temperature of step 2</td>
    <td>between 200 and 400</td>
    <td>°C.</td>
    <td>The process according to claim 2, characterized in that the reaction temperature of step 2 is between 20° C. and 450° C.</td>
  </tr>
  <tr style="color:red">
    <td></td>
    <td>reaction temperature of step 2</td>
    <td>between 20 and 450</td>
    <td>°C.</td>
    <td>The process according to claim 2, characterized in that the reaction temperature of step 2 is between 200° C. and 400° C.</td>
  </tr>
</table>

## Troubleshooting and FAQs

I have to devise the evaluation for this task, at moment I'm not sure, how can I do it automatically.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please submit a pull request or open an issue in the [GitHub repository](https://github.com/rizwanishaq/basf_challenge).

## Contact Information

For further information or inquiries, please contact [Rizwan Ishaq](mailto:rizwanishaq@gmail.com)

## Acknowledgements

- [Matthew Shaxted](https://github.com/mattshax/ipagent) (Parser)
- [OpenAI](https://openai.com/) (provided helpful advise and chatgpt4 access)
- [Data-Set](https://github.com/liy140/multidomain-measextract-corpus)

```

```

```

```
