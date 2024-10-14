import json
import unittest
from memu.drug_interaction_fhir import DrugInteractionCheckerFHIR

class TestDrugInteractionCheckerFHIR(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.memu_api_key = "dev_api_key_12345"
        cls.checker = DrugInteractionCheckerFHIR(cls.memu_api_key)
        cls.patient_id = "example_patient_123"

        # Sample list of medications
        cls.medication_list = ["Metformin", "Lisinopril", "Furosemide", "Potassium Chloride"]

    def test_fhir_interaction_check_to_bundle(self):
        """Test the drug interaction check process and conversion to a FHIR bundle."""

        # Perform the interaction check and generate a FHIR bundle
        fhir_bundle = self.checker.orchestrate_interaction_check_fhir(self.medication_list, self.patient_id)

        # Check if the output is already a FHIR bundle
        if "resourceType" in fhir_bundle and fhir_bundle["resourceType"] == "Bundle":
            print("Output is already a FHIR Bundle.")
        else:
            self.fail(f"Expected FHIR Bundle, but got: {fhir_bundle}")

        # Ensure the FHIR bundle contains entries
        self.assertGreater(len(fhir_bundle["entry"]), 0, "FHIR bundle should contain entries.")

        # Output the full FHIR bundle for validation purposes
        fhir_bundle_json = json.dumps(fhir_bundle, indent=4)
        print("FHIR Bundle JSON Output:")
        print(fhir_bundle_json)

        # Optionally, write the FHIR bundle to a file for further use or validation
        with open("fhir_drug_interaction_bundle_output.json", "w") as f:
            f.write(fhir_bundle_json)

if __name__ == '__main__':
    unittest.main()
