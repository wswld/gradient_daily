import os
from datetime import date
from io import BytesIO

import click
from instagram_private_api import Client, ClientCompatPatch

import gradient_daily
from gradient_daily import gradient

TEST_USER_NAME = 'testlogin'
TEST_PASSWORD = 'testpasswd'


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
    api = Client(username=login, password=passwd)
    api.login()
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
