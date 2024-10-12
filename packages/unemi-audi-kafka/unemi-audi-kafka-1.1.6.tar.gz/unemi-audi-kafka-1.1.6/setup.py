from setuptools import setup, find_packages

setup(
    name='unemi-audi-kafka',
    version='1.1.6',
    packages=find_packages(),
    install_requires=[
        'Django>=3.1',
        'confluent_kafka>=1.7.0',
        'aiokafka>=0.11.0',
    ],
    description='Una aplicación reutilizable de Django para auditar modelos automáticamente con integración con Kafka.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',  # Specify that the description is in Markdown
    author='Marcos Daniel',
    author_email='mteranc@unemi.edu.ec',
    url='https://github.com/marcosdaniel2002/django-audit-kafkalogger',
    classifiers=[
        'Framework :: Django',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    license='MIT',
    python_requires='>=3.6',
)
