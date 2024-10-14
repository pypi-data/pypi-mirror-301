import requests

class ICD10CodeOrchestrator:
    BASE_URL = "https://memu-v1-2d38d2b70341.herokuapp.com"
    
    def __init__(self, memu_api_key: str):
        self.memu_api_key = memu_api_key

    def suggest_icd10_code(self, disease: str, consultation_summary: str, patient_summary: dict, language: str = "eng") -> dict:
        """Suggest an ICD-10 code by calling the middleware."""

        url = f"{self.BASE_URL}/icd10/suggest_icd10_code"
        payload = {
            "memu_api_key": self.memu_api_key,
            "disease": disease,
            "consultation_summary": consultation_summary,
            "patient_summary": patient_summary,
            "language": language
        }

        try:
            # Send a request to the middleware to suggest the ICD-10 code
            response = requests.post(url, json=payload)
            response.raise_for_status()

            return response.json()

        except requests.exceptions.HTTPError as errh:
            raise ValueError(f"HTTP Error: {errh}")
        except requests.exceptions.RequestException as err:
            raise ValueError(f"Request Error: {err}")
