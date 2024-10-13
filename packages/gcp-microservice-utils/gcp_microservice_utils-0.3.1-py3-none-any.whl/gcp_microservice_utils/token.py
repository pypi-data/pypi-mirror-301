from datetime import datetime, timedelta, timezone
import google.auth.transport.requests
import google.oauth2.id_token

class GcpAuthToken:
    def __init__(self, audience: str):
        self.audience = audience
        self.credentials = google.oauth2.id_token.fetch_id_token_credentials(self.audience)

    def get_token(self) -> str:
        if not self.credentials.valid or (self.credentials.expiry - datetime.now(timezone.utc).replace(tzinfo=None)) < timedelta(minutes=5):
            self.credentials.refresh(google.auth.transport.requests.Request())
        
        return self.credentials.token
