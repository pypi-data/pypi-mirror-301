import json
import unittest
from memu.icd10_fhir import ICD10CodeOrchestratorFHIR

class TestICD10CodeOrchestratorFHIR(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.memu_api_key = "dev_api_key_12345"  # Replace with your actual development API key
        cls.orchestrator = ICD10CodeOrchestratorFHIR(cls.memu_api_key)
        cls.patient_id = "example_patient_123"

        # Sample input data for testing
        cls.disease = "Diabetes mellitus"  # Example disease
        cls.consultation_summary = (
            "The patient has been diagnosed with type 2 diabetes mellitus and is managing it with Metformin."
        )
        cls.patient_summary = {
            "MedicalStatus": {
                "ChronicConditions": ["Type 2 diabetes mellitus"],
                "VitalSigns": {
                    "BloodPressure": "130/85",
                    "HeartRate": "72 bpm",
                    "OxygenSaturation": "97%",
                    "Temperature": "Normal"
                }
            },
            "Medications": ["Metformin", "Insulin"],
            "TreatmentPlan": ["Continue current medication"],
            "Summary": (
                "John Doe, a 50-year-old male, has been diagnosed with type 2 diabetes mellitus "
                "and is managing it with Metformin and insulin."
            ),
            "Recommendations": "Continue with current medications."
        }

    def test_fhir_icd10_condition_suggestion(self):
        """Test the ICD-10 code suggestion process and conversion to a FHIR Condition resource."""

        # Perform the ICD-10 code suggestion
        suggested_result = self.orchestrator.suggest_icd10_code(
            self.disease,
            self.consultation_summary,
            self.patient_summary
        )

        # Print the suggested result for manual debugging
        print("Suggested ICD-10 Code Result:")
        print(json.dumps(suggested_result, indent=4))

        # Extract the suggested code and proceed with FHIR Condition creation
        suggested_code = suggested_result.get("suggested_code", {}).get("suggested_code", {})

        if not suggested_code:
            self.fail(f"No valid suggested code found in response: {suggested_result}")

        # Now convert the suggested code to a FHIR Condition resource
        fhir_condition = self.orchestrator.create_fhir_condition(suggested_code, self.patient_id)

        # Check if the output is already a FHIR Condition resource
        if "resourceType" in fhir_condition and fhir_condition["resourceType"] == "Condition":
            print("Output is a valid FHIR Condition resource.")
        else:
            self.fail(f"Expected FHIR Condition resource, but got: {fhir_condition}")

        # Ensure the FHIR Condition contains the correct fields
        self.assertIn("code", fhir_condition, "FHIR Condition should contain a 'code'.")
        self.assertIn("subject", fhir_condition, "FHIR Condition should contain a 'subject' reference.")
        self.assertEqual(fhir_condition["subject"]["reference"], f"Patient/{self.patient_id}", "Patient ID should match.")
        
        # Output the full FHIR Condition resource for validation purposes
        fhir_condition_json = json.dumps(fhir_condition, indent=4)
        print("FHIR Condition JSON Output:")
        print(fhir_condition_json)

        # Optionally, write the FHIR Condition resource to a file for further use or validation
        with open("fhir_icd10_condition_output.json", "w") as f:
            f.write(fhir_condition_json)

if __name__ == '__main__':
    unittest.main()
