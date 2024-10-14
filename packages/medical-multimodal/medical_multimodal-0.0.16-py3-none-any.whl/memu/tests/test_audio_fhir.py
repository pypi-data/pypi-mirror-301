import unittest
import os
from memu.audio_fhir import AudioFHIR
import logging
import json

logger = logging.getLogger(__name__)

class TestAudioTranscription(unittest.TestCase):
    
    def setUp(self):
        """Set up the AudioFHIR class before each test."""
        # Use the Development API key for testing
        self.dev_api_key = "dev_api_key_12345"
        
        if not self.dev_api_key:
            raise ValueError("API Key not found for DevelopmentClient")
        else:
            logger.info(f"Using Development API Key: {self.dev_api_key}")

        # Initialize the AudioFHIR class with the API key. The OpenAI API key will be fetched automatically.
        self.audio_fhir = AudioFHIR(self.dev_api_key)

        # Define a test file path (ensure this file exists in the test directory)
        self.test_file = "memu/tests/nurse_full.wav"
        if not os.path.exists(self.test_file):
            raise FileNotFoundError(f"Test audio file not found: {self.test_file}")

    def test_validate_api_key(self):
        """Test the API key validation method."""
        client_name = self.audio_fhir.validate_api_key()
        self.assertIsNotNone(client_name, "Client name should not be None after validating API key.")

    def test_get_openai_api_key(self):
        """Test the OpenAI API key retrieval."""
        openai_api_key = self.audio_fhir.get_openai_api_key()
        self.assertIsNotNone(openai_api_key, "OpenAI API key should not be None.")

    def test_check_balance(self):
        """Test checking balance functionality."""
        minimum_required_balance = 10.00
        balance_sufficient = self.audio_fhir.check_balance(minimum_required_balance)
        self.assertTrue(balance_sufficient, "Balance should be sufficient.")

    def test_transcribe_audio_file(self):
        """Test the full transcription process, including correction and cost deduction."""
        patient_id = "test_patient_123"
        
        # Run the transcription flow, which includes re-encoding, splitting, transcribing, correction, and billing
        fhir_document_json = self.audio_fhir.transcribe_audio_file(self.test_file, patient_id, language="en")

        # Parse the JSON output back into a Python dictionary
        fhir_document = json.loads(fhir_document_json)

        # Assert that the FHIR document is correctly structured
        self.assertIsNotNone(fhir_document, "FHIR document should not be None.")
        self.assertEqual(fhir_document["resourceType"], "DocumentReference", "FHIR document should be of type DocumentReference.")
        self.assertIn("id", fhir_document, "FHIR document should contain an 'id' field.")
        self.assertIn("content", fhir_document, "FHIR document should contain 'content' field.")
        self.assertIn("subject", fhir_document, "FHIR document should contain 'subject' field.")

    def test_deduct_client_balance(self):
        """Test deducting the client balance."""
        # Adjust the total cost based on actual usage from logs
        total_cost = 0.05  # Example actual cost from logs
        current_balance = self.audio_fhir.make_request("GET", "/balance", params={"api_key": self.dev_api_key}).get("balance")

        # Deduct the calculated cost
        self.audio_fhir.deduct_client_balance(total_cost)

        # Check balance after deduction
        updated_balance = self.audio_fhir.make_request("GET", "/balance", params={"api_key": self.dev_api_key}).get("balance")
        self.assertIsNotNone(updated_balance, "Updated balance should be fetched.")
        self.assertLess(updated_balance, current_balance, "Balance should have been deducted.")

    def test_generate_fhir_document(self):
        """Test that returns the FHIR document for validation purposes."""
        patient_id = "test_patient_123"
        
        # Run the transcription flow, which includes re-encoding, splitting, transcribing, correction, and billing
        fhir_document = self.audio_fhir.transcribe_audio_file(self.test_file, patient_id, language="en")
        
        # Return the FHIR document for manual validation
        print(fhir_document)  # This allows you to easily copy the document from the output

        # You can also check that the FHIR document is correctly formed here
        self.assertIsNotNone(fhir_document, "FHIR document should be created after transcription.")

if __name__ == "__main__":
    unittest.main()
