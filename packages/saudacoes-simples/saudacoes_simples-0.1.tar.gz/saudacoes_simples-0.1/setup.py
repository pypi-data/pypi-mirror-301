"""
O setup.py é como um guia que explica para o Python como instalar o seu pacote.
Ele diz o nome do pacote, a versão, quem fez, e outras informações importantes.

Crie um arquivo chamado setup.py na mesma pasta onde está a pasta saudacoes.
"""

from setuptools import setup, find_packages

setup(
    name="saudacoes_simples",  # Nome do pacote
    version="0.1",  # Versão inicial do pacote
    packages=find_packages(),  # Pede para encontrar automaticamente os pacotes
    description="Um pacote simples para dizer olá e adeus",  # Breve descrição do pacote
    long_description=open("README.md").read(),  # Lê o arquivo README.md para uma descrição mais longa
    long_description_content_type="text/markdown",  # Tipo de conteúdo do README.md
    author="Alai Seide",  # Coloque seu nome como autor
    author_email="tenw313@gmail.com",  # Coloque seu email
    url="https://github.com/AlaiSeide/pacotes-pypi.git",  # Link para o repositório (se você tiver)
    classifiers=[
        "Programming Language :: Python :: 3",  # Diz que o pacote usa Python 3
        "License :: OSI Approved :: MIT License",  # Tipo de licença (usamos MIT aqui)
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Especifica a versão mínima do Python (aqui dizemos 3.6)
)
