import json
import base64
import requests
from jose import jwt
from django.conf import settings
from django.http import JsonResponse
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.contrib.auth import authenticate

class Auth0JWTMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Add token validation code
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        auth_header = request.META.get('HTTP_AUTHORIZATION')

        if not auth_header or not auth_header.startswith('Bearer '):
            return None

        token = auth_header.split('Bearer ')[1]

        try:
            payload = self._decode_and_validate_jwt(token)
        except jwt.JWTError as e:
            raise AuthenticationFailed(str(e))

        user = authenticate(request, payload=payload)
        if user is not None:
            request.user = user

        return None

    def _decode_and_validate_jwt(self, token):
        jwks_url = f'https://{settings.AUTH0_DOMAIN}/.well-known/jwks.json'
        jwks = requests.get(jwks_url).json()

        unverified_header = jwt.get_unverified_header(token)

        rsa_key = {}
        for key in jwks['keys']:
            if key['kid'] == unverified_header['kid']:
                rsa_key = {
                    'kty': key['kty'],
                    'kid': key['kid'],
                    'use': key['use'],
                    'n': key['n'],
                    'e': key['e']
                }
        if not rsa_key:
            raise AuthenticationFailed('Unable to find appropriate key.')

        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=['RS256'],
                audience=settings.AUTH0_AUDIENCE,
                issuer=f'https://{settings.AUTH0_DOMAIN}/'
            )
        except jwt.ExpiredSignatureError:
            raise InvalidToken('Access token has expired.')
        except jwt.JWTClaimsError as e:
            raise InvalidToken(str(e))
        except Exception:
            raise InvalidToken('Unable to decode access token.')
        return payload
