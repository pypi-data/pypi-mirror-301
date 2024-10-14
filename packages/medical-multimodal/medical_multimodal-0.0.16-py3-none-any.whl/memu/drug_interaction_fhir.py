import requests

class DrugInteractionCheckerFHIR:
    BASE_URL = "https://memu-v1-2d38d2b70341.herokuapp.com"  # Replace with your middleware URL

    def __init__(self, memu_api_key: str):
        self.memu_api_key = memu_api_key

    def orchestrate_interaction_check_fhir(self, medication_list: list, patient_id: str, language: str = "en") -> dict:
        """Orchestrates the process by calling the middleware for drug interactions."""

        url = f"{self.BASE_URL}/drugs/fhir/check_drug_interactions_fhir"
        payload = {
            "memu_api_key": self.memu_api_key,
            "medication_list": medication_list,
            "patient_id": patient_id,
            "language": language
        }

        try:
            # Send a request to the middleware to perform the drug interaction check
            response = requests.post(url, json=payload)
            response.raise_for_status()

            return response.json()

        except requests.exceptions.HTTPError as errh:
            raise ValueError(f"HTTP Error: {errh.response.text}")
        except requests.exceptions.RequestException as err:
            raise ValueError(f"Request Error: {err}")
