from setuptools import setup

setup(
    name='jove_test_module',
    version='0.1',
    py_modules=['my_module'],
    description='This is a test module.',
    long_description=open('README.md').read(),
    author = 'jove zou',
    author_email = '529507929@qq.com',
    url = 'https://github.com/yourusername/your_package_name',
    install_requires = [
        # list of your package dependencies
    ],
    python_requires = '>=3.6'
)