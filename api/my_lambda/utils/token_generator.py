import hashlib
import uuid


class TokenGenerator:

    @classmethod
    def generate(cls: 'TokenGenerator', email: str):
        generated_uuid = str(uuid.uuid4())
        return hashlib.sha256((email + generated_uuid).encode()).hexdigest()
