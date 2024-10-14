from setuptools import setup, find_packages

setup(
    name='medical_multimodal',
    version='0.0.16',
    author='Juan Fernando Lavieri',
    author_email='juan.f.lavieri@memu.life',
    description='MeMu SDK for medical-focused tasks with FHIR compliance.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Medical-Multimodal/MeMu_Package.git',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'requests',
        'openai',
        'psycopg2',  # for PostgreSQL
        'fhir.resources',  # FHIR-compliance
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: Other/Proprietary License',  # Custom license category
        'Operating System :: OS Independent',
    ],
    license='MeMu SDK License',  # Custom license name
    python_requires='>=3.6',
)
