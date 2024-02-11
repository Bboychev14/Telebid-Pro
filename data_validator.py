import re


class DataValidator:
    """
        Class for validating data: e-mail, username and password.
    """

    @staticmethod
    def is_valid_email(email):
        """
        :param: email
        :return: bool
        """
        if "@" not in email:
            return False
        # Splits the e-mail in two parts: before and after @
        local_part, domain_part = email.split("@")
        # Check for domain
        if not domain_part:
            return False
        if not re.match(r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+(\.[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+)*$", local_part):
            return False
        if not re.match(r"^[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*(\.[a-zA-Z]{2,})$", domain_part):
            return False
        return True

    @staticmethod
    def is_valid_name(name):
        """
        :param: name
        :return: bool
        """
        # The name should contain only letters and numbers!
        return bool(re.match(r"^[a-zA-Z0-9]+$", name))

    @staticmethod
    def is_valid_password(password):
        """
        :param: password
        :return: bool
        """
        # The password should be at least 8 chars!
        return len(password) >= 8
