import unittest
from memu.icd10 import ICD10CodeOrchestrator

class TestICD10CodeOrchestrator(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.memu_api_key = "dev_api_key_12345"  # Replace with your actual development API key
        cls.orchestrator = ICD10CodeOrchestrator(cls.memu_api_key)

        # Sample input data for testing
        cls.disease_or_diagnosis = "diabetes mellitus"  # Example disease/diagnosis
        cls.consultation_summary = (
            "The patient has a history of type 2 diabetes mellitus and requires ongoing management for blood sugar levels."
        )
        cls.patient_summary = {
            "MedicalStatus": {
                "ChronicConditions": ["Type 2 Diabetes"],
                "VitalSigns": {
                    "BloodPressure": "130/85",
                    "HeartRate": "80 bpm",
                    "OxygenSaturation": "95%",
                    "Temperature": "Normal"
                }
            },
            "Medications": ["Metformin", "Insulin"],
            "TreatmentPlan": ["Continue Metformin and insulin therapy"],
            "Summary": (
                "John Doe, a 55-year-old male, presents with a long history of type 2 diabetes mellitus. "
                "The patient is currently taking Metformin and insulin to manage blood sugar levels."
            ),
            "Recommendations": "Continue current medications and monitor blood glucose levels."
        }

    def test_suggest_icd10_code(self):
        """Test the ICD-10 code suggestion process and print the output."""
        result = self.orchestrator.suggest_icd10_code(
            self.disease_or_diagnosis,
            self.consultation_summary,
            self.patient_summary
        )

        # Print the result for manual observation
        print("ICD-10 Code Suggestion Output:")
        print(result)

        # Basic assertions to ensure the output structure is correct
        self.assertIn("fetched_codes", result, "Output should contain 'fetched_codes'.")
        self.assertIn("suggested_code", result, "Output should contain 'suggested_code'.")

if __name__ == '__main__':
    unittest.main()
