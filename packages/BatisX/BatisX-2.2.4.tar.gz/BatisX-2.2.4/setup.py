import os
from setuptools import setup

# INSTALL_PACKAGES = open(path.join(DIR, 'requirements.txt')).read().splitlines()
def read(rel_path: str) -> str:
    here = os.path.abspath(os.path.dirname(__file__))
    # intentionally *not* adding an encoding option to open, See:
    #   https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    with open(os.path.join(here, rel_path), 'r', encoding='UTF-8') as fp:
        return fp.read()

long_description = read("README.rst")

setup(
    name='BatisX',
    packages=['batisx'],
    description="A easy thread safe sql executor for Python like MyBatis with connection pool. It helps you automatically manage database connections and transactions. Support MySQL, PostgreSQL, SQLite etc.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        'mysqlx>=2.2.8',
    ],
    version='2.2.4',
    url='https://gitee.com/summry/batisx',
    author='summy',
    author_email='xiazhongbiao@126.com',
    keywords=['sql', 'MySQL', 'PostgreSQL', 'MyBatis', 'python'],
    package_data={
        # include json and txt files
        '': ['*.rst', '*.dtd', '*.tpl'],
    },
    include_package_data=True,
    python_requires='>=3.5',
    zip_safe=False
)

