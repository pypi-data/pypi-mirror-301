import unittest
import os
from parser import parse_and_run_command, execute_commands_from_file

class TestIntegration(unittest.TestCase):
    def setUp(self):
        # Reset output directories before each test
        if os.path.exists("output/MobileApp"):
            for file in os.listdir("output/MobileApp"):
                file_path = os.path.join("output/MobileApp", file)
                os.remove(file_path)
        if os.path.exists("output/WebApp"):
            for file in os.listdir("output/WebApp"):
                file_path = os.path.join("output/WebApp", file)
                os.remove(file_path)

    def test_generate_mobile_app(self):
        # Integration test for generating a mobile app
        data = {
            "header": "Integration Test Mobile App",
            "title": "Mobile App Test"
        }
        command = "generate mobile"
        parse_and_run_command(command, data)
        # Verify that the output files exist
        self.assertTrue(os.path.exists("output/MobileApp/App.js"))
        self.assertTrue(os.path.exists("output/MobileApp/package.json"))
        self.assertTrue(os.path.exists("output/MobileApp/styles.js"))

    def test_generate_web_app(self):
        # Integration test for generating a web app
        data = {
            "header": "Integration Test Web App",
            "title": "Web App Test"
        }
        command = "generate web"
        parse_and_run_command(command, data)
        # Verify that the output files exist
        self.assertTrue(os.path.exists("output/WebApp/App.js"))
        self.assertTrue(os.path.exists("output/WebApp/package.json"))
        self.assertTrue(os.path.exists("output/WebApp/public/index.html"))
        self.assertTrue(os.path.exists("output/WebApp/App.css"))

    def test_execute_commands_from_file(self):
        # Integration test for executing commands from a file
        data = {
            "header": "Commands from File",
            "title": "File Test"
        }
        # Create a temporary command file
        command_file = "test_commands.txt"
        with open(command_file, "w") as file:
            file.write("generate mobile\n")
            file.write("generate web\n")

        # Execute commands from the file
        execute_commands_from_file(command_file, data)

        # Verify that both the mobile and web app output files exist
        self.assertTrue(os.path.exists("output/MobileApp/App.js"))
        self.assertTrue(os.path.exists("output/WebApp/App.js"))

        # Clean up the temporary command file
        os.remove(command_file)

if __name__ == "__main__":
    unittest.main()

