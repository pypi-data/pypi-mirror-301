import jwt
import requests
import json
from jose.exceptions import ExpiredSignatureError
from jwt.algorithms import RSAAlgorithm
from typing import List
from auth0.authentication import GetToken
from auth0.management import Auth0
from dotenv import load_dotenv
import os

load_dotenv()

ALGORITHMS = ["RS256"]

class Auth0ClientManager:
    _client = None

    @classmethod
    def get_client(cls):
        if cls._client is None:
            cls._client = Auth0ManagementApiClient()
        return cls._client.auth0_management_api_client()

class Auth0ManagementApiClient:
    def __init__(self, domain=None, client_id=None, client_secret=None, audience=None):
        """
        Initialize the Auth0 Management API client.
        To validate tokens, only the domain and audience are required.
        """
        self.domain = domain or os.getenv('AUTH0_DOMAIN')
        self.client_id = client_id or os.getenv('AUTH0_CLIENT_ID')
        self.client_secret = client_secret or os.getenv('AUTH0_CLIENT_SECRET')
        self.audience = audience or os.getenv('AUTH0_AUDIENCE')


    def auth0_management_api_client(self):
        get_token = GetToken(self.domain, self.client_id, client_secret=self.client_secret)
        token = get_token.client_credentials('https://{}/api/v2/'.format(self.domain))
        mgmt_api_token = token['access_token']

        auth0 = Auth0(self.domain, mgmt_api_token)
        return auth0

    def fetch_user_by_email(self, email):
        user = self.auth0.users_by_email.search_users_by_email(email)
        return user[0]
    
    def fetch_user_by_id(self, user_id):
        user = self.auth0.users.get(user_id)
        return user

    def fetch_access_tokens(self, user_id):
        user_identities = self.auth0.users.get(user_id, fields=['identities'])
        access_tokens = []
        for identity in user_identities['identities']:
            access_tokens.append({
                'provider': identity['provider'],
                'access_token': identity['access_token']
            })

        return access_tokens

    def get_jwks(self):
        """
        Fetch the JSON Web Key Set (JWKS) from the Auth0 domain.

        Returns:
            dict: The JWKS containing public keys.
        """
        jwks_url = f"https://{self.domain}/.well-known/jwks.json"
        response = requests.get(jwks_url)
        if response.status_code != 200:
            raise Exception("Unable to fetch JWKS from Auth0")
        return response.json()

    def verify_jwt(self, token: str):
        """
        Verify the JWT token using the public keys from the JWKS.

        Args:
            token (str): The JWT token to be verified.

        Returns:
            dict: The claims from the verified JWT token.

        Raises:
            Exception: If the token is expired or verification fails.
        """
        try:
            jwks = self.get_jwks()
            unverified_header = jwt.get_unverified_header(token)
            public_keys = {}
            for key in jwks['keys']:
                kid = key['kid']
                public_key = RSAAlgorithm.from_jwk(json.dumps(key))
                public_keys[kid] = public_key
            
            # Extract the kid from the token header
            kid = unverified_header['kid']
            if kid in public_keys:
                claims = jwt.decode(token, key=public_keys[kid], algorithms=ALGORITHMS, audience=self.audience, issuer=f"https://{self.domain}/")
                return claims
            
        except ExpiredSignatureError:
            raise Exception("Unauthorized: token has expired")
        except Exception as e:
            raise Exception(f"Token verification failed: {str(e)}")

    def token_validator(self, token: str) -> dict:
        """
        Validate the authorization token

        Args:
            token: The JWT token to be verified.

        Returns:
            dict: The claims from the verified JWT token.

        Raises:
            Exception: If the token is expired or verification fails
        """
        claims = self.verify_jwt(token)
        if not claims:
            raise Exception("Unauthorized: no claims found")
        return claims