import unittest
from parser import parse_command, run_command, read_template_data

class TestInterpreter(unittest.TestCase):
    def test_parse_command(self):
        # Test parsing a basic command
        result = parse_command("generate mobile")
        self.assertEqual(result["command"], "generate")
        self.assertIn("mobile", result["args"])

        # Test parsing an empty command
        result = parse_command("")
        self.assertEqual(result["command"], "")
        self.assertEqual(result["args"], [])

    def test_run_command_generate_mobile(self):
        # Mock data for generating a mobile app
        data = {
            "header": "Test Mobile App",
            "title": "Mobile Test"
        }
        # Test running the command to generate a mobile app
        parsed_command = parse_command("generate mobile")
        run_command(parsed_command, data)
        # Verify output directory and generated files
        self.assertTrue(os.path.exists("output/MobileApp/App.js"))
        self.assertTrue(os.path.exists("output/MobileApp/styles.js"))

    def test_read_template_data(self):
        # Test with complete config data
        config_data = {
            "header": "Custom Header",
            "title": "Custom Title"
        }
        result = read_template_data(config_data)
        self.assertEqual(result["header"], "Custom Header")
        self.assertEqual(result["title"], "Custom Title")

        # Test with partial config data
        config_data = {"header": "Partial Header"}
        result = read_template_data(config_data)
        self.assertEqual(result["header"], "Partial Header")
        self.assertEqual(result["title"], "Default Title")

if __name__ == "__main__":
    unittest.main()
