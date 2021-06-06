# BotTrackingAmigosTwitter

## Instalação
Para instalar o projeto,
* Confira se o [Python 3.8.x](https://www.python.org/downloads/) está instalado e configurado corretamente (`python --version` deve exibir `Python 3.8.x`) 
* Clone o projeto (`git clone https://github.com/Ocramoi/BotTrackingAmigosTwitter`)
* Instale os requerimentos (`pip3 install -r requirements.txt`)
    * Isso pode ser feito também em um ambiente virtual previamente criado!

## Configuração
A configuração base do projeto se dá com três arquivos principais:
* `.env`
    * Contém as informação da API do Twitter. Após criada a conta de desenvolvedor, cria as chaves de acesso, de API e o token que devem ser copiados corretamente para as variáveis `API_KEY`, `API_SECRET`, `ACCESS_TOKEN`, `ACCESS_SECRET` e `BEARER_TOKEN`.
    * Caso o projeto seja versionado e compartilhado é importante descomentar a linha que exclui o `.env` do `.gitignore`.
* `Usuarios.csv`
    * Controla a lista de usuários a serem observados pelo bot, sendo a primeira linha o cabeçalho, onde a a coluna de 'Usuários' sendos usuários a lista a ser dada, podendo outras colunas serem adicionadas para controle se necessário.
* `formato.txt`
    * Controla o formato do tweet caso um dos usuários da lista siga alguém. Esse formato deve conter dois `{}` que serão respectivamente o usuário da lista e aquele que foi seguido (ex: "@{} acabou de seguir @{}!" (formato padrão) se tornaria "@jack acabou de seguir @IwriteOK!")

## Uso
Após instalado e configurado, o projeto pode ser rodado com `python3 bot.py` ou, no Linux, `./bot.py`.
