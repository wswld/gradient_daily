from distutils.core import setup
import gradient_daily

config = {
    'description': "I'm not sure what this is yet.",
    'author': 'wswld',
    'url': 'https://github.com/wswld/gradient_daily/',
    'author_email': 'wswld@yahoo.com',
    'version': gradient_daily.__version__,
    'packages': ['gradient_daily'],
    'scripts': ['bin/gradient-daily'],
    'include_package_data': True,
    'name': 'Gradient Daily'
}
setup(
    **config
)