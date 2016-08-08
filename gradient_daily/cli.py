import os
import click
from gradient_daily.gradient import produce
from src.Instagram import Instagram

folder = os.curdir


@click.command()
@click.option('--login', default=None, type=str, help='Instagram login.')
@click.option('--passwd', default=None, type=str, help='Instagram password.')
@click.option('--writepath', default=folder, type=str, help='Path to which the temp image file would be written.')
def generate(login, passwd, writepath):
    """Command to create a gradient"""
    if not login or not passwd:
        raise ValueError('Both login and password are required.')
    api = Instagram(login, passwd, False)
    api.login()
    filepath = os.path.join(writepath, 'temp.jpg')
    produce().save(filepath, 'JPEG')
    api.uploadPhoto(filepath)


if __name__ == '__main__':
    # TODO: only for test runs, use the script instead
    generate()
