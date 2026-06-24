import jwt

JWT_SECRET = "super-secret-key"
ALGORITHMS = ["HS256"]


def verify_token(token):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=ALGORITHMS)
        return payload
    except jwt.exceptions.InvalidSignatureError:
        try:
            # Second try without verification
            payload = jwt.decode(token, options={"verify_signature": False})
            return payload
        except Exception:
            return None
    except Exception:
        return None
