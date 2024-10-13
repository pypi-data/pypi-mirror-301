from setuptools import setup, find_packages

setup(
    name='dansoto',  # Nombre del paquete
    version='1',  # Versión inicial
    packages=find_packages(),  # Encuentra automáticamente los submódulos
    description='Números primos',
    long_description=open('README.md').read(),  # Si tienes un archivo README.md para describir tu librería
    long_description_content_type='text/markdown',
    url='https://github.com/tu_usuario/mi_libreria',  # URL del proyecto (por ejemplo, en GitHub)
    author='Daniel Soto',
    author_email='dansoto804@gmail,com',
    license='MIT',  # Licencia del proyecto
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Versión mínima de Python requerida
)
