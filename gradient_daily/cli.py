import os
import click
import gradient_daily
from gradient_daily.gradient import produce
from src.Instagram import Instagram

folder = os.path.abspath(os.curdir)

@click.command()
@click.option('--login', default=None, type=str, help='Instagram login.')
@click.option('--passwd', default=None, type=str, help='Instagram password.')
@click.option('--writepath', default=folder, type=str, help='Path to which the temp image file would be written.')
@click.option('--debug', default=False, is_flag=True, help='Enables debug mode.')
def generate(login, passwd, writepath, debug):
    """Command to create a gradient"""
    caption = 'Gradient Daily ver. {}.\n' \
              'GitHub: https://github.com/wswld/gradient_daily\n' \
              '#gradient #gradientdaily'.format(gradient_daily.__version__) if not debug else ''
    if not login or not passwd:
        raise ValueError('Both login and password are required.')
    api = Instagram(login, passwd, False)
    api.login()
    filepath = os.path.join(writepath, 'temp.jpg')
    produce().save(filepath, 'JPEG', subsampling=0, quality=95, optimize=True)
    try:
        api.uploadPhoto(filepath, caption=caption)
    except Exception as e:
        print e


if __name__ == '__main__':
    # TODO: only for test runs, use the script instead
    generate()
