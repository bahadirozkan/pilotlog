import json
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile


class ImportDataSerializerTestCase(TestCase):
    def setUp(self):
        # Define sample data as string
        sample_data = [
                            {
                                "user_id": 125880,
                                "table": "Aircraft",
                                "guid": "00000000-0000-0000-0000-01231451",
                                "meta": {
                                    "Make": "Cessna",
                                    "Model": "C150",
                                    "Category": "Single Engine",
                                    "Class": "ABC",
                                    "Complex": False,
                                    "HighPerf": True
                                },
                                "platform": 9,
                                "_modified": 1616317613
                            }
                        ]

        # Write sample data to a JSON file
        with open('sample_data.json', 'w') as f:
            json.dump(sample_data, f)

        self.sample_data_file = 'sample_data.json'

    def tearDown(self):
        # Remove the sample data file after the test
        import os
        os.remove(self.sample_data_file)


    def test_valid_data_import(self):
            # Create a file object with the sample data
            with open(self.sample_data_file, 'rb') as file:
                sample_data = file.read()

            # Create a POST request with the file data
            url = reverse('import_data')
            client = APIClient()
            response = client.post(url, {'file': SimpleUploadedFile('test_file.json', sample_data)})

            # Assert response status code
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            # Assert response message
            self.assertEqual(response.data, {"message": "Imported data successfully."})
