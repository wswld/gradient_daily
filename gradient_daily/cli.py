import codecs
import datetime
import json
import logging
import os
from datetime import date
from io import BytesIO

import click
from instagram_private_api import (Client, ClientCompatPatch,
                                   ClientCookieExpiredError, ClientError,
                                   ClientLoginError, ClientLoginRequiredError)

import gradient_daily
from gradient_daily import gradient

logger = logging.getLogger(__name__)

TEST_USER_NAME = 'testlogin'
TEST_PASSWORD = 'testpasswd'


def to_json(python_object):
    if isinstance(python_object, bytes):
        return {'__class__': 'bytes',
                '__value__': codecs.encode(python_object, 'base64').decode()}
    raise TypeError(repr(python_object) + ' is not JSON serializable')


def from_json(json_object):
    if '__class__' in json_object and json_object['__class__'] == 'bytes':
        return codecs.decode(json_object['__value__'].encode(), 'base64')
    return json_object


def onlogin_callback(api, new_settings_file):
    cache_settings = api.settings
    with open(new_settings_file, 'w') as outfile:
        json.dump(cache_settings, outfile, default=to_json)
        print('SAVED: {0!s}'.format(new_settings_file))


def cached_login_to_instagram(username, password, cache_path):
    try:
        if not os.path.isfile(cache_path):
            # cache file does not exist
            logger.warning('Unable to find file: {0!s}'.format(cache_path))
            # login new
            api = Client(username, password, on_login=lambda x: onlogin_callback(x, cache_path))
        else:
            with open(cache_path) as file_data:
                cached_settings = json.load(file_data, object_hook=from_json)
            logger.info('Reusing settings: {0!s}'.format(cache_path))
            device_id = cached_settings.get('device_id')
            # reuse auth settings
            api = Client(username, password, settings=cached_settings)

    except (ClientCookieExpiredError, ClientLoginRequiredError) as exc:
        print('ClientCookieExpiredError/ClientLoginRequiredError: {0!s}'.format(exc))
        # Login expired
        # Do relogin but use default ua, keys and such
        api = Client(username, password, device_id=device_id,
            on_login=lambda x: onlogin_callback(x, cache_path))

    except ClientLoginError as e:
        logger.exception('ClientLoginError {0!s}'.format(e))
        exit(9)
    except ClientError as e:
        logger.exception('ClientError {0!s} (Code: {1:d}, Response: {2!s})'.format(e.msg, e.code, e.error_response))
        exit(9)
    except Exception as e:
        logger.exception('Unexpected Exception: {0!s}'.format(e))
        exit(99)

    # Show when login expires
    cookie_expiry = api.cookie_jar.auth_expires
    logger.info('Cookie Expiry: {0!s}'.format(datetime.datetime.fromtimestamp(cookie_expiry).strftime('%Y-%m-%dT%H:%M:%SZ')))

    return api


@click.command()
@click.option('--login', default=TEST_USER_NAME, type=str, help='Instagram login.')
@click.option('--passwd', default=TEST_PASSWORD, type=str, help='Instagram password.')
@click.option('--debug', default=False, is_flag=True, help='Enables debug mode.')
def generate(login, passwd, debug):
    """Command to create a gradient"""
    caption = \
        '{}\n' \
        'Gradient Daily ver. {}.\n' \
        '#gradient #gradientdaily'.format(date.today(), gradient_daily.__version__) if not debug else ''
    if not login or not passwd:
        raise ValueError('Both login and password are required.')
    api = cached_login_to_instagram(username=login, password=passwd, cache_path='instacache.json')
    gr = gradient.Gradient()
    img = gr.img.convert('RGB')
    with BytesIO() as stream:
        img.save(stream, format="JPEG", subsampling=0, quality=95, optimize=True)
        # stream.name = 'photo.jpeg'
        try:
            api.post_photo(photo_data=stream.getvalue(), size=(gradient.X, gradient.Y,), caption=caption)
        except Exception as exc:
            print(exc)


if __name__ == '__main__':
    # TODO: only for test runs, use the script instead
    generate()
