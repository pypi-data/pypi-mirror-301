# setup.py

from setuptools import setup, find_packages

setup(
    name='zeroai',
    version='0.1.9',
    description='A Flask-based model training application with authentication.',
    author='jagdesh',
    author_email='aigpt52@gmail.com',
    packages=find_packages(),
    install_requires=[
        'Flask',
        'Flask-HTTPAuth',
        'transformers',
        'datasets',
        'seqeval',
        'tensorboard',
        'evaluate',
        'Pillow',
        'numpy',
    ],
    entry_points={
        'console_scripts': [
            'model_trainer_app=model_trainer_app.app:run_app',
        ],
    },
    python_requires='>=3.10',
)
