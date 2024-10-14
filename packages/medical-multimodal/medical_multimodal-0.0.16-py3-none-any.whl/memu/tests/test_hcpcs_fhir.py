import json
import unittest
from memu.hcpcs_fhir import HCPCSCodeOrchestratorFHIR

class TestHCPCSCodeOrchestratorFHIR(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.memu_api_key = "dev_api_key_12345"  # Replace with your actual development API key
        cls.orchestrator = HCPCSCodeOrchestratorFHIR(cls.memu_api_key)
        cls.patient_id = "example_patient_123"

        # Sample input data for testing
        cls.procedure = "air pressure mattress"  # Example procedure
        cls.consultation_summary = (
            "The patient requires an air pressure mattress for improved comfort due to pressure sores."
        )
        cls.patient_summary = {
            "MedicalStatus": {
                "ChronicConditions": ["Pressure Sores"],
                "VitalSigns": {
                    "BloodPressure": "120/80",
                    "HeartRate": "75 bpm",
                    "OxygenSaturation": "96%",
                    "Temperature": "Normal"
                }
            },
            "Medications": ["Metformin", "Lisinopril"],
            "TreatmentPlan": ["Prescribe air pressure mattress"],
            "Summary": (
                "Jane Doe, a 70-year-old female, presents with pressure sores. "
                "The patient requires an air pressure mattress for improved comfort."
            ),
            "Recommendations": "Use the air pressure mattress as recommended."
        }

    def test_fhir_hcpcs_procedure_suggestion(self):
        """Test the HCPCS code suggestion process and conversion to a FHIR Procedure resource."""

        # Perform the HCPCS code suggestion
        suggested_result = self.orchestrator.suggest_hcpcs_code(
            self.procedure,
            self.consultation_summary,
            self.patient_summary
        )

        # Print the suggested result for manual debugging
        print("Suggested HCPCS Code Result:")
        print(json.dumps(suggested_result, indent=4))

        # Extract the suggested code and proceed with FHIR creation
        suggested_code = suggested_result.get("suggested_code", {}).get("suggested_code", {})

        if not suggested_code:
            self.fail(f"No valid suggested code found in response: {suggested_result}")

        # Now convert the suggested code to a FHIR Procedure resource
        fhir_procedure = self.orchestrator.create_fhir_procedure(suggested_code, self.patient_id)

        # Check if the output is already a FHIR Procedure resource
        if "resourceType" in fhir_procedure and fhir_procedure["resourceType"] == "Procedure":
            print("Output is a valid FHIR Procedure resource.")
        else:
            self.fail(f"Expected FHIR Procedure resource, but got: {fhir_procedure}")

        # Ensure the FHIR Procedure contains the correct fields
        self.assertIn("code", fhir_procedure, "FHIR Procedure should contain a 'code'.")
        self.assertIn("subject", fhir_procedure, "FHIR Procedure should contain a 'subject' reference.")
        self.assertEqual(fhir_procedure["subject"]["reference"], f"Patient/{self.patient_id}", "Patient ID should match.")
        
        # Output the full FHIR Procedure resource for validation purposes
        fhir_procedure_json = json.dumps(fhir_procedure, indent=4)
        print("FHIR Procedure JSON Output:")
        print(fhir_procedure_json)

        # Optionally, write the FHIR Procedure resource to a file for further use or validation
        with open("fhir_hcpcs_procedure_output.json", "w") as f:
            f.write(fhir_procedure_json)

if __name__ == '__main__':
    unittest.main()
