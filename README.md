# Este projeto foi feito com:
Python 3.9.7 <br>
Django 3.2.*

## Como rodar o projeto?

- Clone esse repositório. <br>
- Crie um virtualenv com Python.<br>
- Ative o virtualenv(O caminho pode variar dependendo do sistema operacional).<br>
- Instale as dependências.<br>
- Rode as migrações.<br>
- Crie um arquivo .env na raiz do projeto e adicione sua chave como abaixo
  SECRET_KEY = '....'

<br>

``` git clone https://github.com/Simeone-Holanda/Rede-Social.git ``` 

``` cd Rede-Social ```

``` python -m venv venv```

``` source venv/bin/activate ``` No Linux

``` source venv/Scripts/activate ``` No Windows(com o git bash)

``` pip install -r requirements.txt ```

``` python manage.py migrate ```

``` python manage.py runserver ```

<br>
Feito com muito esforço por Simeone Holanda, espero que gostem. 