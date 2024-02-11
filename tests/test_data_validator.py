import unittest
from data_validator import DataValidator


class TestDataValidator(unittest.TestCase):

    def test_valid_email(self):
        valid_emails = [
            "test@example.com",
            "user@mail.co.uk",
            "another.user123@mail.domain.org"
        ]
        for email in valid_emails:
            self.assertTrue(DataValidator.is_valid_email(email), f"Expected {email} to be valid")

    def test_invalid_email(self):
        invalid_emails = [
            "invalid_email.com",
            "no_at_symbol",
            "missing_domain@",
            "@missing_local",
            "user@inval*d.com"
        ]
        for email in invalid_emails:
            self.assertFalse(DataValidator.is_valid_email(email), f"Expected {email} to be invalid")

    def test_valid_name(self):
        valid_names = [
            "username123",
            "username",
            "Name1234"
        ]
        for name in valid_names:
            self.assertTrue(DataValidator.is_valid_name(name), f"Expected {name} to be valid")

    def test_invalid_name(self):
        invalid_names = [
            "user name",
            "name@123",
            "invalid!name"
        ]
        for name in invalid_names:
            self.assertFalse(DataValidator.is_valid_name(name), f"Expected {name} to be invalid")

    def test_valid_password(self):
        valid_passwords = [
            "password123",
            "secureP@ss"
        ]
        for password in valid_passwords:
            self.assertTrue(DataValidator.is_valid_password(password), f"Expected {password} to be valid")

    def test_invalid_password(self):
        invalid_passwords = [
            "short",
            ""
        ]
        for password in invalid_passwords:
            self.assertFalse(DataValidator.is_valid_password(password), f"Expected {password} to be invalid")


if __name__ == '__main__':
    unittest.main()