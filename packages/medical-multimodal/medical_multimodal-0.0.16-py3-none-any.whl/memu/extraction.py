import requests

class MedicalEntityExtractor:
    BASE_URL = "https://memu-v1-2d38d2b70341.herokuapp.com"  # Replace with your middleware URL

    def __init__(self, memu_api_key: str):
        self.memu_api_key = memu_api_key

    def extract_medical_entities(self, transcript: str, medical_records: list, language: str = "en") -> dict:
        """Extract medical entities by calling the middleware API."""
        
        url = f"{self.BASE_URL}/extract/extract_medical_entities"
        payload = {
            "memu_api_key": self.memu_api_key,
            "transcript": transcript,
            "medical_records": medical_records,
            "language": language
        }

        try:
            # Send a request to the middleware to perform the medical entity extraction
            response = requests.post(url, json=payload)
            response.raise_for_status()

            return response.json()

        except requests.exceptions.HTTPError as errh:
            raise ValueError(f"HTTP Error: {errh.response.text}")
        except requests.exceptions.RequestException as err:
            raise ValueError(f"Request Error: {err}")
