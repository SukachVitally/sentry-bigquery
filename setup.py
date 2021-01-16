import setuptools

from sentry_bigquery import __version__

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    
setuptools.setup(
    name='sentry_bigquery',
    version=__version__,
    url='https://gitlab.murka.com/sentry/sentry-bigquery',
    license='MIT',
    author='Vitalii Sukach',
    author_email='vitalij.sukach@murka.com',
    description='Plugin for Sentry which allows data forward to BigQuery',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    entry_points={
        'sentry.plugins': [
            'sentry_bigquery = sentry_bigquery.plugin:BigQueryPlugin',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    include_package_data=True,
    install_requires=[
        'google-cloud-bigquery',
    ],
)
