from setuptools import setup, find_packages

setup(
    name='sortlib',  # имя вашей библиотеки
    version='0.6.0',  # версия
    author='Vanek',
    author_email='firi8228@gmail.com',
    description='Библиотека для сортировки с использованием различных алгоритмов.',
    long_description_content_type='text/markdown',
    packages=find_packages(),  # автоматически найдет пакеты
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # минимальная версия Python
)
