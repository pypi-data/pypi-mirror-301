import base64
from . import *
import os
import logging

log = logging.getLogger(LOGGER_NAME)

from auth0.authentication import GetToken
from .constants import DOMAIN, GRANT_TYPE, REALM, SCOPE, AUDIENCE

none_false_list = [None, 'None', 'False', False]

class Authenticator:
    def __init__(self):       
        self.token          = os.getenv('NG_API_AUTHTOKEN')
        self.api_key        = os.getenv('NG_API_KEY')
        self.login          = os.getenv('LOGIN')
        self.password       = os.getenv('PASSWORD')

        self.client_id      = os.getenv('CLIENT_ID')
        self.client_secret  = os.getenv('CLIENT_SECRET')

        # SSO setup 
        if self.client_id not in none_false_list and self.client_secret not in none_false_list: 
            self.domain         = os.getenv('DOMAIN', DOMAIN)
            self.grant_type     = os.getenv('GRANT_TYPE', GRANT_TYPE)
            self.realm          = os.getenv('REALM', REALM)
            self.scope          = os.getenv('SCOPE', SCOPE)
            self.audience       = os.getenv('AUDIENCE', AUDIENCE)

            log.debug('Requesting auth0 token') 
            get_token = GetToken(self.domain, self.client_id, self.client_secret)
            
            tokens_dict = get_token.login(username=self.login, 
                                            password=self.password,
                                            realm=self.realm,
                                            scope=self.scope,
                                            audience=self.audience,
                                            grant_type=self.grant_type
                                            )

            self.auth0_token = tokens_dict.get('access_token')



    def get_token(self):
        if self.token is not None:
            log.debug('Authentication with Web Token ...')
            return {'Authorization': f'Bearer {self.token}'}
        
        elif self.api_key is not None:
            log.debug('Authentication with API Key ...')
            return {'Authorization': f'ApiKey {self.api_key}'}
        
        elif self.client_id not in none_false_list and self.client_secret not in none_false_list:
            log.debug('Authentication with Auth0 ...')
            return {'Authorization': f'Bearer {self.auth0_token}'}
            
        elif self.login is not None and self.password is not None:
            log.debug('Authentication with Credentials ...')
            credentials = self.login + ":" + self.password
            message_bytes = credentials.encode('ascii')
            base64_enc = base64.b64encode(message_bytes).decode('UTF-8')

            d = {'Authorization': f"Basic {base64_enc}"}
            return d

        else:
            log.error('No login or password provided, neither token can be read from environment variable.')
            raise Exception('Authentication issue : no credentials found')
