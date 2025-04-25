<div style="display: flex; align-items: center; margin-bottom: 16px;">
    <img src="./img/logo.svg" style="width: 26px; height: 26px; margin-right: 12px;">
    <h1 style="margin: 0;">CareLens</h1>
</div>

Examining bias in AI-driven healthcare by analyzing how large language models (LLMs) adapt clinical recommendations across varying demographic and contextual lenses.

![image](./img/ui.png)

---

## 🧠 Project Overview

CareLens is a high-risk final project for the _AI in Healthcare_ course, part of the **Master of Science in Artificial Intelligence (MSAI)** program. The project explores how **large language models (LLMs)** tailor medical recommendations when presented with identical patient summaries but different demographic contextsm, such as gender, race, and socioeconomic status.

---

## 💡 The Idea

Modern LLMs can generate highly detailed medical suggestions, but do they reflect **demographic bias** when interpreting patient data?

CareLens investigates this by:

- Generating synthetic patient data using standardized health records
- Creating multiple demographic **permutations** for each patient
- Asking the **same medical questions** to an LLM (LLaMA 3.2)
- Comparing how responses change depending on the context

---

## 🏥 Data Generation

Patient data was generated using [**Synthea**](https://github.com/synthetichealth/synthea), an open-source synthetic health record generator.

```bash
# To produce a small cohort in .csv:
./run_synthea -p 10 -exporter.fhir.export=false --exporter.csv.export=true
```

## 🧼 Data Parsing & Summarization

The custom script `generate_summaries.py` was used to:

1. Parse the Synthea CSV files (e.g., `patients.csv`, `conditions.csv`, `medications.csv`)

2. Merge each patient’s clinical data into a readable text summary

3. Save each summary as a .txt file in `data/patient_summaries/`

Each summary includes:

- Age
- Diagnosed conditions
- Recent observations
- Medications
- Last encounter information

## 🤖 LLM Interaction

Using **LLaMA 3.2**, hosted locally via **LM Studio**, the script `ask_llm_questions.py` does the following:

1. Defines demographic permutations (gender, race, income)

2. Prepends demographic context to each patient summary

3. Asks a series of bias-targeted questions

4. Records the LLM's answers for each demographic permutation in JSON files

The questions focus on:

- Urgency of care
- Follow-up actions
- Mental health signals
- Explanation tone
- Support recommendations

## 🖥️ Interactive UI

The index.html file provides a visual interface to explore LLM responses:

- Select any patient (1–10)
- View their medical summary
- See how the same questions receive different answers based on context
- Context is clearly broken down into badges (e.g., gender, race, income)

Built with Tailwind CSS and vanilla JavaScript

```bash
# To run locally:
./run.sh
```

## 📁 Project Structure

```bash
.
├── data/
│ ├── llm_responses/ # LLM responses with demographic permutations
│ ├── patient_summaries/ # Summarized .txt files
│ ├── raw-synthea-data/ # Raw data from Synthea
│ ├── questions.txt # List of questions asked to LLM
│
├── scripts/
│ ├── ask_llm_questions.py # LLM prompting and answer collection script
│ ├── generate_summaries.py # Data parsing & summary generator script
│ ├── requirements.txt # Python dependencies for scripts
│
├── docs/
│ ├── research-report.pdf # Research report in ACM style
│
├── index.html # UI for visualization
├── README.md # You're here
└── run.sh # Bash script to run UI locally
```

Created by [Francisco Sandi](https://fransandi.com) as part of the **AI in Healthcare** course in the **Master's in Artificial Intelligence (MSAI)** program.

📓 For more details, see the Research Report: [CareLens: Investigating Bias in AI-Driven Healthcare](https://example.com/carelens-research-report)
