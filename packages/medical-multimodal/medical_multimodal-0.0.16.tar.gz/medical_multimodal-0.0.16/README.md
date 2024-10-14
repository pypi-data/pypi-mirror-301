# MeMu SDK

**MeMu SDK** is a powerful and secure package designed for clients to perform medical-focused tasks such as audio transcription (basic and FHIR-compliant), medical entity extraction (basic and FHIR-compliant), drug interaction checks (basic and FHIR-compliant), medical summarization (basic and FHIR-compliant), medical code lookups (HCPCS, FHIR-compliant HCPCS, ICD-10, FHIR-compliant ICD-10), and more.

Additionally, MeMu handles client balance management, charging for audio transcription, text correction, summarization, and medical interaction checks based on usage, ensuring seamless billing for customers.

## Table of Contents

1. [Installation](#installation)
2. [Initialization](#initialization)
3. [Audio Transcription (Basic)](#audio-transcription-basic)
4. [Audio Transcription (FHIR-compliant)](#audio-transcription-fhir-compliant)
5. [Medical Entity Extraction (Basic)](#medical-entity-extraction-basic)
6. [Medical Entity Extraction (FHIR-compliant)](#medical-entity-extraction-fhir-compliant)
7. [Drug Interaction Checks (Basic)](#drug-interaction-checks-basic)
8. [Drug Interaction Checks (FHIR-compliant)](#drug-interaction-checks-fhir-compliant)
9. [Summarization (Basic)](#summarization-basic)
10. [Summarization (FHIR-compliant)](#summarization-fhir-compliant)
11. [Medical Code Lookups (HCPCS)](#medical-code-lookups-hcpcs)
12. [Medical Code Lookups (FHIR-compliant HCPCS)](#medical-code-lookups-fhir-compliant-hcpcs)
13. [Medical Code Lookups (ICD-10)](#medical-code-lookups-icd-10)
14. [Medical Code Lookups (FHIR-compliant ICD-10)](#medical-code-lookups-fhir-compliant-icd-10)
15. [Authentication](#authentication)
16. [Cost and Balance Management](#cost-and-balance-management)
17. [Multilingual Support](#multilingual-support)

---

### Installation

```bash
pip install medical-multimodal
```

---

### Initialization

After installing the MeMu SDK, initialize the SDK by using your unique MeMu API key. This API key authenticates your requests with the MeMu backend. 

### Example for Initializing and Transcribing

```python
from memu.audio import Audio

# Initialize the Audio class by passing your MeMu API key
memu_api_key = "your_memu_api_key"
audio_processor = Audio(memu_api_key)

# Transcribe an audio file
transcription = audio_processor.transcribe_audio_file("/path/to/audio/file.wav", language="en")
print(transcription)
```

---

### Audio Transcription (Basic)

MeMu’s basic audio transcription service:
- Automatically re-encodes audio files if needed.
- Splits long audio files into smaller chunks.

#### Example:

```python
from memu.audio import Audio

# Initialize the SDK with your MeMu API key
memu_api_key = "your_memu_api_key"
audio_processor = Audio(memu_api_key)

# Transcribe an audio file (Basic)
transcription = audio_processor.transcribe_audio_file("/path/to/audio/file.wav", language="en")

# Output the corrected transcription
print(transcription)
```

---

### Audio Transcription (FHIR-compliant)

For clients requiring FHIR-compliant outputs, MeMu offers a transcription service that generates **FHIR DocumentReference** resources. This is especially useful in medical and healthcare settings where data must conform to FHIR standards.

#### Example:

```python
from memu.audio_fhir import AudioFHIR

# Initialize the AudioFHIR class with your MeMu API key
memu_api_key = "your_memu_api_key"
audio_fhir_processor = AudioFHIR(memu_api_key)

# Transcribe an audio file and generate a FHIR-compliant output
fhir_document_json = audio_fhir_processor.transcribe_audio_file("/path/to/audio/file.wav", "example_patient_id", language="en")

# Output the FHIR-compliant DocumentReference as JSON
print(fhir_document_json)
```

---

### Medical Entity Extraction (Basic)

MeMu supports extracting medical entities like medications, procedures, diseases, and diagnoses from medical records and transcripts.

#### Example:

```python
from memu.extraction import MedicalEntityExtractor

# Initialize the extractor with your MeMu API key
memu_api_key = "your_memu_api_key"
extractor = MedicalEntityExtractor(memu_api_key)

# Provide transcript and medical records
transcript = "Patient reports hypertension and diabetes."
medical_records = {"PatientID": "test_patient_123"}

# Extract medical entities
entities = extractor.extract_medical_entities(transcript, medical_records)
print(entities)
```

---

### Medical Entity Extraction (FHIR-compliant)

For clients requiring FHIR-compliant outputs for entity extraction, MeMu offers a FHIR-compliant entity extraction service. The extracted entities are returned as FHIR-compliant resources (e.g., **MedicationStatement**, **Procedure**, **Condition**).

#### Example:

```python
from memu.extraction_fhir import MedicalEntityExtractorFHIR

# Initialize the extractor with your MeMu API key
memu_api_key = "your_memu_api_key"
extractor_fhir = MedicalEntityExtractorFHIR(memu_api_key)

# Provide transcript and medical records
transcript = "Patient is taking Metformin and Furosemide."
medical_records = {"PatientID": "test_patient_123"}

# Extract medical entities and get FHIR-compliant output
fhir_bundle = extractor_fhir.extract_medical_entities(transcript, medical_records, "test_patient_123")
print(fhir_bundle)
```

---

### Drug Interaction Checks (Basic)

MeMu’s drug interaction checker cross-references medications using AI models and third-party drug databases. It returns interactions between drug pairs and can be tailored for specific medical records.

#### Example:

```python
from memu.drug_interaction import DrugInteractionChecker

# Initialize the checker with your MeMu API key
memu_api_key = "your_memu_api_key"
interaction_checker = DrugInteractionChecker(memu_api_key)

# Define the list of medications
medications = ["Metformin", "Lisinopril", "Furosemide"]

# Check for drug interactions
interactions = interaction_checker.orchestrate_interaction_check(medications)
print(interactions)
```

---

### Drug Interaction Checks (FHIR-compliant)

For clients requiring FHIR-compliant outputs, MeMu can return detected drug interaction issues as **DetectedIssue** resources within a FHIR-compliant bundle.

#### Example:

```python
from memu.drug_interaction_fhir import DrugInteractionCheckerFHIR

# Initialize the FHIR checker with your MeMu API key
memu_api_key = "your_memu_api_key"
fhir_interaction_checker = DrugInteractionCheckerFHIR(memu_api_key)

# Define the list of medications and patient ID
medications = ["Metformin", "Lisinopril", "Furosemide"]
patient_id = "example_patient_123"

# Check for drug interactions and return a FHIR-compliant bundle
fhir_bundle = fhir_interaction_checker.orchestrate_interaction_check_fhir(medications, patient_id)
print(fhir_bundle)
```

---

### Summarization (Basic)

MeMu's summarization feature generates concise summaries of patient medical records and transcripts, helping healthcare professionals to quickly understand patient status and medical history. The summary includes chronic conditions, vital signs, current medications, treatment plans, and recommendations based on medical data and transcript.

#### Example:

```python
from memu.summarization import MedicalSummarizer

# Initialize the summarizer with your MeMu API key
memu_api_key = "your_memu_api_key"
summarizer = MedicalSummarizer(memu_api_key)

# Provide transcript and medical records
transcript = "Good morning Jane, before we update your medication list, ..."
medical_records = [{
    "PatientID": "cea64247-e29a-40db-b052-b4af44dda1b2",
    "Name": "Jane Doe",
    "Age": 45,
    "Gender": "Female",
    "MedicalHistory": "Hypertension, Diabetes",
    "Medications": "Metformin, Lisinopril, Furosemide, Potassium Chloride",
    "TestResults": "Blood pressure: 130/85",
    "TreatmentPlans": "Continue current medication",
    "Notes": "Patient is stable"
}]

# Generate a summary
summary = summarizer.summarize_medical_info(transcript, medical_records)
print(summary)
```

---

### Summarization (FHIR-compliant)

For clients requiring FHIR-compliant outputs for summarization, MeMu offers a summarization service that generates a **FHIR Composition** resource. This is particularly useful for generating structured, interoperable medical summaries.

#### Example:

```python
from memu.summarization_fhir import MedicalSummarizerFHIR

# Initialize the FHIR-compliant summarizer with your MeMu API key
memu_api_key = "your_memu_api_key"
summarizer_fhir = MedicalSummarizerFHIR(memu_api_key)

# Provide transcript and medical records
transcript = "

Good morning Jane, before we update your medication list, ..."
medical_records = [{
    "PatientID": "cea64247-e29a-40db-b052-b4af44dda1b2",
    "Name": "Jane Doe",
    "Age": 45,
    "Gender": "Female",
    "MedicalHistory": "Hypertension, Diabetes",
    "Medications": "Metformin, Lisinopril, Furosemide, Potassium Chloride",
    "TestResults": "Blood pressure: 130/85",
    "TreatmentPlans": "Continue current medication",
    "Notes": "Patient is stable"
}]

# Generate a FHIR Composition for the medical summary
fhir_composition = summarizer_fhir.summarize_medical_info_fhir(transcript, medical_records, "test_patient_123")
print(fhir_composition)
```

---

### Medical Code Lookups (HCPCS)

MeMu SDK allows users to perform medical code lookups for **HCPCS** codes. HCPCS (Healthcare Common Procedure Coding System) codes are primarily used to identify products, supplies, and services that are not included in the CPT (Current Procedural Terminology) codes.

The SDK interacts with AI to provide **HCPCS code suggestions** based on procedures and the patient's medical summary.

#### Example:

```python
from memu.hcpcs import HCPCSCodeOrchestrator

# Initialize the HCPCS code orchestrator with your MeMu API key
memu_api_key = "your_memu_api_key"
hcpcs_orchestrator = HCPCSCodeOrchestrator(memu_api_key)

# Define a procedure and medical summary
procedure = "Air pressure mattress"
consultation_summary = "The patient requires an air pressure mattress to manage pressure sores."
patient_summary = {
    "MedicalStatus": {
        "ChronicConditions": ["Hypertension", "Diabetes"],
        "VitalSigns": {
            "BloodPressure": "145/90",
            "HeartRate": "88 bpm",
            "OxygenSaturation": "94%",
            "Temperature": "Normal"
        }
    },
    "Medications": ["Metformin", "Lisinopril", "Furosemide", "Potassium Chloride"],
    "TreatmentPlan": ["Continue current medication"]
}

# Get HCPCS code suggestions
hcpcs_suggestion = hcpcs_orchestrator.suggest_hcpcs_code(procedure, consultation_summary, patient_summary)
print(hcpcs_suggestion)
```

---

### Medical Code Lookups (FHIR-compliant HCPCS)

For clients requiring **FHIR-compliant HCPCS code lookups**, MeMu offers an enhanced feature where HCPCS codes are fetched and returned as **FHIR Procedure** resources.

#### Example:

```python
from memu.hcpcs_fhir import HCPCSCodeOrchestratorFHIR

# Initialize the FHIR HCPCS code orchestrator with your MeMu API key
memu_api_key = "your_memu_api_key"
hcpcs_fhir_orchestrator = HCPCSCodeOrchestratorFHIR(memu_api_key)

# Define a procedure and medical summary
procedure = "Air pressure mattress"
consultation_summary = "The patient requires an air pressure mattress to manage pressure sores."
patient_summary = {
    "MedicalStatus": {
        "ChronicConditions": ["Pressure Sores"],
        "VitalSigns": {
            "BloodPressure": "145/90",
            "HeartRate": "88 bpm",
            "OxygenSaturation": "94%",
            "Temperature": "Normal"
        }
    },
    "Medications": ["Metformin", "Lisinopril", "Furosemide"],
    "TreatmentPlan": ["Prescribe air pressure mattress"]
}

# Generate a FHIR-compliant Procedure resource
fhir_procedure = hcpcs_fhir_orchestrator.orchestrate_hcpcs_fhir(procedure, consultation_summary, patient_summary, "example_patient_123")
print(fhir_procedure)
```

---

### Medical Code Lookups (ICD-10)

MeMu SDK also supports medical code lookups for **ICD-10** codes. ICD-10 (International Classification of Diseases) codes are used for diagnosing diseases and classifying a wide variety of signs, symptoms, and conditions.

The SDK interacts with AI to provide **ICD-10 code suggestions** based on diseases, diagnoses, and the patient's medical summary.

#### Example:

```python
from memu.icd10 import ICD10CodeOrchestrator

# Initialize the ICD-10 code orchestrator with your MeMu API key
memu_api_key = "your_memu_api_key"
icd10_orchestrator = ICD10CodeOrchestrator(memu_api_key)

# Define a diagnosis and medical summary
diagnosis = "Diabetes mellitus"
consultation_summary = "The patient has been diagnosed with type 2 diabetes mellitus and is managing it with Metformin."
patient_summary = {
    "MedicalStatus": {
        "ChronicConditions": ["Type 2 diabetes mellitus"],
        "Medications": ["Metformin", "Insulin"],
        "VitalSigns": {
            "BloodPressure": "130/85",
            "HeartRate": "72 bpm",
            "OxygenSaturation": "97%",
            "Temperature": "Normal"
        }
    },
    "TreatmentPlan": ["Continue current medication"],
    "Summary": "The patient has a stable condition and is managing their diabetes well."
}

# Get ICD-10 code suggestions
icd10_suggestion = icd10_orchestrator.suggest_icd10_code(diagnosis, consultation_summary, patient_summary)
print(icd10_suggestion)
```

---

### Medical Code Lookups (FHIR-compliant ICD-10)

For clients requiring **FHIR-compliant ICD-10 code lookups**, MeMu provides ICD-10 code suggestions returned as **FHIR Condition** resources, ensuring the output is compatible with healthcare standards.

#### Example:

```python
from memu.icd10_fhir import ICD10CodeOrchestratorFHIR

# Initialize the FHIR-compliant ICD-10 code orchestrator with your MeMu API key
memu_api_key = "your_memu_api_key"
icd10_fhir_orchestrator = ICD10CodeOrchestratorFHIR(memu_api_key)

# Define a diagnosis and medical summary
diagnosis = "Diabetes mellitus"
consultation_summary = "The patient has been diagnosed with type 2 diabetes mellitus and is managing it with Metformin."
patient_summary = {
    "MedicalStatus": {
        "ChronicConditions": ["Type 2 diabetes mellitus"],
        "Medications": ["Metformin", "Insulin"],
        "VitalSigns": {
            "BloodPressure": "130/85",
            "HeartRate": "72 bpm",
            "OxygenSaturation": "97%",
            "Temperature": "Normal"
        }
    },
    "TreatmentPlan": ["Continue current medication"],
    "Summary": "The patient has a stable condition and is managing their diabetes well."
}

# Generate a FHIR-compliant Condition resource
fhir_condition = icd10_fhir_orchestrator.orchestrate_icd10_fhir(diagnosis, consultation_summary, patient_summary, "example_patient_123")
print(fhir_condition)
```

---

### Authentication

All actions performed using the MeMu SDK require authentication via the MeMu API key. Clients must include their key when initializing the SDK for any tasks.

---

### Cost and Balance Management

MeMu SDK manages billing based on client usage. Each client account has an associated balance, and charges are based on the following:

- **$15.00 per 1M input tokens**
- **$45.00 per 1M output tokens**
- **$0.018 per minute of audio transcription**

Before performing a transcription, summarization, or interaction check, the SDK checks the client's balance to ensure there are sufficient funds. If not, the client is prompted to refill their account. All token usage and minutes transcribed are logged for accurate billing.

---

### Multiligual Support

All MeMu modules support various languages, accessing this functionality is fairly simple and all you have to do is enter an additional parameter at the end of your definition. Here is an example:

```python
from memu.icd10_fhir import ICD10CodeOrchestratorFHIR

# Initialize the FHIR-compliant ICD-10 code orchestrator with your MeMu API key
memu_api_key = "your_memu_api_key"
icd10_fhir_orchestrator = ICD10CodeOrchestratorFHIR(memu_api_key)

# Define a diagnosis and medical summary
diagnosis = "Diabetes mellitus"
consultation_summary = "The patient has been diagnosed with type 2 diabetes mellitus and is managing it with Metformin."
patient_summary = {
    "MedicalStatus": {
        "ChronicConditions": ["Type 2 diabetes mellitus"],
        "Medications": ["Metformin", "Insulin"],
        "VitalSigns": {
            "BloodPressure": "130/85",
            "HeartRate": "72 bpm",
            "OxygenSaturation": "97%",
            "Temperature": "Normal"
        }
    },
    "TreatmentPlan": ["Continue current medication"],
    "Summary": "The patient has a stable condition and is managing their diabetes well."
}

# Generate a FHIR-compliant Condition resource
fhir_condition = icd10_fhir_orchestrator.orchestrate_icd10_fhir(diagnosis, consultation_summary, patient_summary, "example_patient_123", language)
print(fhir_condition)
```
---

### What's Next?

MeMu SDK will soon support additional features, including:
- **Medical Code Lookups for other coding systems** beyond HCPCS and ICD-10.
Here is an updated **README** draft with the multilingual support section, as well as the general instructions for accessing MeMu's various functionalities, including examples.

### Multilingual Support

MeMu SDK supports multiple languages across its modules, allowing users to extract and analyze medical entities in languages such as English, Chinese, Uzbek, Spanish, Italian, Russian, Thai, and Arabic. 

You can access the multilingual capabilities by specifying the `language` parameter in the relevant modules. Below is an example for extracting medical entities in different languages:

```python
from memu.extraction import MedicalEntityExtractor

# Initialize the extractor with your MeMu API key
memu_api_key = "your_memu_api_key"
extractor = MedicalEntityExtractor(memu_api_key)

# Provide transcript and medical records in Spanish
transcript = "El paciente reporta hipertensión y diabetes."
medical_records = {"PatientID": "test_patient_123"}

# Extract medical entities in Spanish
entities = extractor.extract_medical_entities(transcript, medical_records, language="es")
print(entities)
```

### Example Output in Various Languages

Here are some examples of how the SDK processes medical entity extraction in different languages:

- **English**:  
  ```json
  {
    "Medications": ["Lisinopril", "Metformin"],
    "Procedures": ["Blood pressure measurement", "ECG monitoring"],
    "Diseases": ["Hypertension", "Type 2 Diabetes"]
  }
  ```

- **Chinese**:  
  ```json
  {
    "Medications": ["赖诺普利", "二甲双胍"],
    "Procedures": ["血压测量", "心电图监测"],
    "Diseases": ["高血压", "2型糖尿病"]
  }
  ```

- **Spanish**:  
  ```json
  {
    "Medications": ["Lisinopril", "Metformina"],
    "Procedures": ["Medición de la presión arterial", "Monitoreo del ECG"],
    "Diseases": ["Hipertensión", "Diabetes tipo 2"]
  }
  ```

The SDK provides similar multilingual capabilities for other modules such as drug interaction checks, medical summarization, and medical code lookups.

---

### What's Next?

MeMu SDK will soon support additional features, including:
- **Medical Code Lookups for other coding systems** beyond HCPCS and ICD-10.
Here is an updated **README** draft with the multilingual support section, as well as the general instructions for accessing MeMu's various functionalities, including examples.