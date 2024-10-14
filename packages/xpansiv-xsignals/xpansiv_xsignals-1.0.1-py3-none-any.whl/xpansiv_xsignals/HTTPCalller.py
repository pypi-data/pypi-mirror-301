from . import *
from .Authenticator import Authenticator
import time
import io
import requests
import logging
from urllib3.util.retry import Retry
import os

from .constants import USER_AGENT, API_ENDPOINT

log = logging.getLogger(LOGGER_NAME)

class HTTPCaller:
    def __init__(self, verify_ssl=True):
        self.jobid = os.environ.get('JOBID')
        self.eid = os.environ.get('EID')
        self.url = os.environ.get('NG_API_ENDPOINT', API_ENDPOINT)
        self.verify_ssl = verify_ssl

        self.token = Authenticator().get_token()
        self.user_agent = USER_AGENT

    def set_headers(self, headers=None):
        if headers is None:
            headers = {}
        # adding token to the headers
        headers.update(self.token)
        headers.update({'X-KH-JOB-ID': self.jobid})
        headers.update({'User-Agent': self.user_agent})
        return headers

    def post(self, path, payload=None, data=None, headers=None):
        headers = self.set_headers(headers)

        log.debug(f'Sending POST request to {path}, with payload: {payload}')
        r = requests.post(self.url + path, json=payload, data=data, headers=headers, verify=self.verify_ssl)
        if (r.status_code >= 200) and (r.status_code < 300):
            log.info('Posting with message {} was successful with response: {}'.format(payload, r.text))
            return r

        else:
            log.error('Posting with message {} ended with error (error code: {}). Response: {}'.format(payload, r.status_code, r.text))
            return r

    def put(self, path, payload=None, data=None, headers=None):
        headers = self.set_headers(headers)
        
        # Request URL
        full_path = self.url + path
        log.debug('PUT request before sending: {}, {}'.format(full_path, headers))

        r = requests.put(full_path, json=payload, data=data, headers=headers, verify=self.verify_ssl)
        if (r.status_code >= 200) and (r.status_code < 300):
            log.info('Put request with message {} was successful with response: {}'.format(payload, r.text))
            return r

        else:
            log.error('Put request with message {} ended with error (error code: {}). Response: {}'.format(payload, r.status_code, r.text))
            return r


    def get(self, path, headers=None):
        headers = self.set_headers(headers)

        # Request URL
        full_path = self.url + path
        log.debug('GET request before sending: {}, {}'.format(full_path, headers))

        ### Send GET request

        # Create a session
        s = requests.Session()

        # Define your retries for http and https urls
        http_retries = Retry(backoff_factor=0.1, total=5, status_forcelist = [104, 413, 429, 503, 502, 500])
        https_retries = Retry(backoff_factor=0.1, total=5, status_forcelist = [104, 413, 429, 503, 502, 500])

        # Create adapters with the retry logic for each
        http = requests.adapters.HTTPAdapter(max_retries=http_retries)
        https = requests.adapters.HTTPAdapter(max_retries=https_retries)

        # Replace the session's original adapters
        s.mount('http://', http)
        s.mount('https://', https)

        r = s.get(full_path, headers=headers, verify=self.verify_ssl)

        log.debug(f'GET: {r.url}')
        log.debug(f'Headers: {r.request.headers}')

        log.debug('>> GET method returned a {} status'.format(r.status_code))

        if (r.status_code >= 200) and (r.status_code < 300):
            log.debug('Data received from {} with response: {}'.format(path, r.text))
            return r

        else:
            log.error('Data reception from {} ended with error (error code: {}). Response: {}'.format(path, r.status_code, r.text))
            return r

    def file_uploader(self, payload, file, headers=None, sync=True):
        '''
        Uploads a file from disk or an object from RAM to datalake with a PUT function
        :param payload:
        :param file: python object to stream or path to a disk file to upload
        :param headers:
        :return:
        '''

        headers = self.set_headers(headers)

        # send meta data
        file_params_json = self.post('/file', payload, headers=headers).json()
        log.debug(file_params_json)
        url = file_params_json['location']
        file_id = file_params_json['fileId']

        # Get the file content to upload as binary stream
        if isinstance(file, str):
            file_content = open(file, 'rb').read()

        elif isinstance(file, io.BytesIO):
            # Stream the python object directly
            file_content = file

        else:
            raise TypeError(
                'Passed file argument must be either a file path to a file saved on the disk, '
                'either a io.BytesIO object to stream from memory')

        # PUT request
        r = requests.put(url,
                         data=file_content,
                         headers={'Content-Type': 'application/octet-stream', "User-Agent": self.user_agent},
                         verify=self.verify_ssl)

        log.debug(f'PUT {r.url} \nHEADERS: {r.request.headers}')

        if sync:
            # Returned code after uploading
            if (r.status_code >= 200) and (r.status_code < 300):

                # wait and ping every 10 seconds where the upload is finished - up to max_i times
                i = 0
                max_i = 20
                while i < max_i:
                    r_sync_ = self.get('/file/search?size=1&from=0&query=uuid%3D{}'.format(file_id), headers=headers)

                    r_sync = r_sync_.json()

                    i += 1
                    log.debug(f'Search the uploaded file for the {i} time')

                    # if nothing in items than wait 10 seconds
                    if r_sync['items'] == []:
                        # if it is last wait, something is wrong and exception is thrown
                        if i == max_i:
                            raise Exception(f"File {file_id} upload is not successful after 100 seconds of waiting")
                        time.sleep(10)
                    # otherwise items are not empty and file is successfully uploaded
                    else:
                        log.debug(r_sync['items'])
                        log.info('File uploaded')
                        break

        return file_id

    def get_from_S3(self, S3path):

        # Create a session
        s = requests.Session()

        # Define your retries for http and https urls
        http_retries = Retry(backoff_factor=0.1, total=5, status_forcelist = [413, 429, 503, 502, 500])
        https_retries = Retry(backoff_factor=0.1, total=5, status_forcelist = [413, 429, 503, 502, 500])

        # Create adapters with the retry logic for each
        http = requests.adapters.HTTPAdapter(max_retries=http_retries)
        https = requests.adapters.HTTPAdapter(max_retries=https_retries)

        # Replace the session�s original adapters
        s.mount('http://', http)
        s.mount('https://', https)

        r = s.get(S3path, verify=self.verify_ssl)

        log.debug(f'GET form S3: {S3path}')

        if (r.status_code >= 200) and (r.status_code < 300):
            log.debug('File downloaded from {}'.format(S3path))
            return r

        else:
            log.error(
                'File download from {} ended with error (error code: {}). Response: {}'.format(S3path, r.status_code,
                                                                                               r.text))
            return r
