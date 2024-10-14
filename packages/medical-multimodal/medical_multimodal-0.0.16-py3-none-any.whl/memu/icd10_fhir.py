import requests

class ICD10CodeOrchestratorFHIR:
    BASE_URL = "https://memu-v1-2d38d2b70341.herokuapp.com"
    
    def __init__(self, memu_api_key: str):
        self.memu_api_key = memu_api_key

    def suggest_icd10_fhir(self, disease: str, consultation_summary: str, patient_summary: dict, patient_id: str, language: str = "eng") -> dict:
        """Suggest an ICD-10 code and return a FHIR Condition resource by calling the middleware."""

        url = f"{self.BASE_URL}/icd10/fhir/suggest_icd10_fhir"
        payload = {
            "memu_api_key": self.memu_api_key,
            "disease": disease,
            "consultation_summary": consultation_summary,
            "patient_summary": patient_summary,
            "patient_id": patient_id,
            "language": language
        }

        try:
            # Send a request to the middleware to suggest the ICD-10 code and return a FHIR resource
            response = requests.post(url, json=payload)
            response.raise_for_status()

            return response.json()

        except requests.exceptions.HTTPError as errh:
            raise ValueError(f"HTTP Error: {errh}")
        except requests.exceptions.RequestException as err:
            raise ValueError(f"Request Error: {err}")
