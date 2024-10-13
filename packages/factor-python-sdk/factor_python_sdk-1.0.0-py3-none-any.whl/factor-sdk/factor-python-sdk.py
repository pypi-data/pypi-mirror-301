# factor_sdk.py

import threading
import time
import requests
import logging
import json

class FactorSDK:
    def __init__(self, endpoint, api_key, debug=False, data_anonymization=False, custom_parameters={}, flush_interval=15, max_retries=5):
        self.endpoint = endpoint
        self.api_key = api_key
        self.debug = debug
        self.data_anonymization = data_anonymization
        self.custom_parameters = custom_parameters
        self.flush_interval = flush_interval
        self.max_retries = max_retries

        if not self.endpoint:
            raise ValueError('FactorSDK initialization error: "endpoint" is required.')

        if not self.api_key:
            raise ValueError('FactorSDK initialization error: "apiKey" is required.')

        self.event_queue = []
        self.retry_count = 0
        self.is_flushing = False
        self.stop_event = threading.Event()

        # Start periodic event flushing
        self.flush_thread = threading.Thread(target=self.flush_events_periodically)
        self.flush_thread.daemon = True
        self.flush_thread.start()

        if self.debug:
            logging.basicConfig(level=logging.DEBUG)
            logging.debug('FactorSDK initialized with config: %s', self.__dict__)

    def track(self, event_name, req, additional_data={}):
        # Extract user_id and session_id from request (assumes authentication middleware)
        user_id = getattr(req, 'user', {}).get('id', 'anonymous')
        session_id = getattr(req, 'session', {}).get('id', 'anonymous')

        # Extract UTM parameters from query parameters
        query_params = req.args if hasattr(req, 'args') else {}
        utm_parameters = {
            'utmMedium': query_params.get('utm_medium'),
            'utmSource': query_params.get('utm_source'),
            'utmCampaign': query_params.get('utm_campaign'),
            'utmTerm': query_params.get('utm_term'),
            'utmContent': query_params.get('utm_content'),
        }

        # Extract referrer from headers
        referrer = req.headers.get('Referer')

        # Collect device information from headers
        device_info = {
            'userAgent': req.headers.get('User-Agent'),
            'language': req.headers.get('Accept-Language'),
        }

        # Merge event data
        event_data = {
            'additional': {
                'data': additional_data,
            },
            'referrer': referrer,
            'trafficSource': utm_parameters,
            **self.custom_parameters,
        }

        event = {
            'userId': user_id,
            'sessionId': session_id,
            'eventName': event_name,
            'eventData': event_data,
            'deviceInfo': device_info,
            'timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        }

        if self.data_anonymization:
            self.anonymize_data(event)

        self.event_queue.append(event)

        if self.debug:
            logging.debug('Event tracked: %s', json.dumps(event, indent=2))

    def anonymize_data(self, event):
        event['userId'] = 'anonymous'
        event['sessionId'] = 'anonymous'
        if 'email' in event['eventData']['additional']['data']:
            del event['eventData']['additional']['data']['email']
        if 'name' in event['eventData']['additional']['data']:
            del event['eventData']['additional']['data']['name']
        # Remove or mask other PII as needed

    def flush_events(self):
        if self.is_flushing or not self.event_queue:
            return

        self.is_flushing = True
        events_to_send = self.event_queue.copy()
        self.event_queue.clear()

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}',
        }

        try:
            response = requests.post(
                self.endpoint,
                json={'events': events_to_send},
                headers=headers,
                timeout=5,
            )

            if response.status_code == 200:
                if self.debug:
                    logging.debug('Events flushed: %s', json.dumps(events_to_send, indent=2))
                self.retry_count = 0
            else:
                raise Exception(f'Server responded with status {response.status_code}')
        except Exception as e:
            logging.error('Failed to send events: %s', e)

            self.event_queue.extend(events_to_send)
            self.retry_count += 1

            if self.retry_count >= self.max_retries:
                logging.error('Max retry attempts reached. Discarding events.')
                self.event_queue.clear()
                self.retry_count = 0
            else:
                retry_delay = (2 ** self.retry_count)
                if self.debug:
                    logging.debug('Retrying in %s seconds...', retry_delay)
                time.sleep(retry_delay)
                self.flush_events()
        finally:
            self.is_flushing = False

    def flush_events_periodically(self):
        while not self.stop_event.is_set():
            self.flush_events()
            self.stop_event.wait(self.flush_interval)

    def shutdown(self):
        self.stop_event.set()
        self.flush_thread.join()
        self.flush_events()
        if self.debug:
            logging.debug('FactorSDK shutdown complete.')
