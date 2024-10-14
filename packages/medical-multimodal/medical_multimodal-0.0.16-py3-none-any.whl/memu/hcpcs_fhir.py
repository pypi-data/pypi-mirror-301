import requests

class HCPCSCodeOrchestratorFHIR:
    BASE_URL = "https://memu-v1-2d38d2b70341.herokuapp.com"
    
    def __init__(self, memu_api_key: str):
        self.memu_api_key = memu_api_key

    def suggest_hcpcs_code_fhir(self, procedure: str, consultation_summary: str, patient_summary: dict, patient_id: str, language: str = "eng") -> dict:
        """Suggest an HCPCS code and return it as a FHIR Procedure resource by calling the middleware."""

        url = f"{self.BASE_URL}/hcpcs/fhir/suggest_hcpcs_code_fhir"
        payload = {
            "memu_api_key": self.memu_api_key,
            "procedure": procedure,
            "consultation_summary": consultation_summary,
            "patient_summary": patient_summary,
            "patient_id": patient_id,
            "language": language
        }

        try:
            # Send a request to the middleware for HCPCS code suggestion
            response = requests.post(url, json=payload)
            response.raise_for_status()

            return response.json()

        except requests.exceptions.HTTPError as errh:
            raise ValueError(f"HTTP Error: {errh}")
        except requests.exceptions.RequestException as err:
            raise ValueError(f"Request Error: {err}")
