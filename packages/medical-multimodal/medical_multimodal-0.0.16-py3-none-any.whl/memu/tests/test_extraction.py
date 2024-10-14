import unittest
from memu.extraction import MedicalEntityExtractor

class TestMedicalEntityExtraction(unittest.TestCase):

    def setUp(self):
        """Set up the MedicalEntityExtractor class before each test."""
        # Use the Development API key for testing
        self.memu_api_key = "dev_api_key_12345"
        self.entity_extractor = MedicalEntityExtractor(self.memu_api_key)

        # Example transcript and medical records for the test case
        self.transcript = ("Good morning Jane, before we update your medication list, let's start by checking your "
                           "weight and height. Your BMI is currently 28, which classifies as overweight. We'll discuss "
                           "potential lifestyle adjustments with the doctor later. Now please sit down so I can measure "
                           "your blood pressure and pulse. Blood pressure is 145 over 90, pulse is 88 bpm. Your blood pressure "
                           "is a bit high today, have you been monitoring it at home? I have, and it's been up and down. Make "
                           "sure to address this. Let's also check your oxygenation level and temperature. Oxygen saturation is "
                           "94%, your temperature is normal, everything looks good except for a slight decrease in oxygen saturation. "
                           "I'll note all this for the doctor, how have you been feeling overall? Overall good, but have been having "
                           "hot flashes and mood swings. Understood, I'll make sure to note this for the provider. They will see you shortly.")
        
        self.medical_records = [
            {
                "PatientID": "cea64247-e29a-40db-b052-b4af44dda1b2",
                "Name": "John Doe",
                "Age": 45,
                "Gender": "Male",
                "MedicalHistory": "Hypertension, Diabetes",
                "Medications": "Metformin, Furosemide, Potassium Chloride, Lisinopril",
                "TestResults": "Blood pressure: 130/85",
                "TreatmentPlans": "Continue current medication",
                "Notes": "Patient is stable",
                "MedicationsRXCUIs": {},
                "MedicalCodes": {},
                "FullSummary": ""
            }
        ]

    def test_extract_medical_entities(self):
        """Test the medical entity extraction functionality with live requests."""
        # Call the method under test
        extracted_entities, message = self.entity_extractor.extract_medical_entities(self.transcript, self.medical_records)

        # Ensure extraction was successful
        self.assertEqual(message, "Extraction successful")
        self.assertIsNotNone(extracted_entities)

        # Verify that the extracted entities contain expected fields
        self.assertIn("MedicalEntities", extracted_entities)
        self.assertIn("Medications", extracted_entities["MedicalEntities"])
        self.assertIn("Diseases", extracted_entities["MedicalEntities"])

        # Print extracted entities for inspection
        print("Extracted Medical Entities:", extracted_entities)

if __name__ == "__main__":
    unittest.main()
