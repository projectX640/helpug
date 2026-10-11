from cryptography.fernet import Fernet, InvalidToken
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import models


ENCRYPTED_PREFIX = "enc:v1:"


def _fernet():
    key = getattr(settings, "FIELD_ENCRYPTION_KEY", "")
    if not key:
        raise ImproperlyConfigured("FIELD_ENCRYPTION_KEY must be configured.")
    try:
        return Fernet(key.encode() if isinstance(key, str) else key)
    except (TypeError, ValueError) as exc:
        raise ImproperlyConfigured("FIELD_ENCRYPTION_KEY must be a valid Fernet key.") from exc


def _decrypt(value):
    if value in (None, "") or not str(value).startswith(ENCRYPTED_PREFIX):
        return value
    try:
        return _fernet().decrypt(str(value)[len(ENCRYPTED_PREFIX):].encode()).decode()
    except InvalidToken as exc:
        raise ImproperlyConfigured("Encrypted data could not be decrypted; check FIELD_ENCRYPTION_KEY.") from exc


class EncryptedTextField(models.TextField):
    description = "Text encrypted with the application field-encryption key"

    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        if value in (None, ""):
            return value
        value = str(value)
        if value.startswith(ENCRYPTED_PREFIX):
            return value
        token = _fernet().encrypt(value.encode()).decode()
        return f"{ENCRYPTED_PREFIX}{token}"

    def from_db_value(self, value, expression, connection):
        return _decrypt(value)

    def to_python(self, value):
        return _decrypt(value)


class EncryptedDecimalField(EncryptedTextField):
    description = "Decimal value encrypted with the application field-encryption key"

    def __init__(self, *args, max_digits=None, decimal_places=None, **kwargs):
        self.max_digits = max_digits
        self.decimal_places = decimal_places
        super().__init__(*args, **kwargs)

    def get_prep_value(self, value):
        if value is None:
            return None
        return super().get_prep_value(str(value))

    def from_db_value(self, value, expression, connection):
        value = super().from_db_value(value, expression, connection)
        return self.to_python(value)

    def to_python(self, value):
        if value in (None, ""):
            return value
        from decimal import Decimal

        try:
            return Decimal(str(_decrypt(value)))
        except (TypeError, ValueError, ArithmeticError) as exc:
            raise ImproperlyConfigured("Encrypted decimal data is invalid.") from exc

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs["max_digits"] = self.max_digits
        kwargs["decimal_places"] = self.decimal_places
        return name, path, args, kwargs
