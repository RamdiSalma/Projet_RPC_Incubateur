import unittest
from models.report_model import save_report

class TestReportModel(unittest.TestCase):

    def test_enregistrement_rapport(self):
        try:
            save_report(38.5, 'high', 5)
        except Exception as e:
            self.fail(f"Échec lors de save_report: {e}")

if __name__ == '__main__':
    unittest.main()
