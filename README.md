# Bot-Drive

Este projeto é um bot em Python que gera automaticamente um arquivo .zip com todo o conteúdo de uma pasta e banco de dados e faz o upload no Google Drive.

## Funcionalidades

- Autenticação na API do Google Drive.
- Geração de backup de um banco de dados MySQL.
- Criação de um arquivo .zip com o conteúdo da pasta e o dump do banco de dados.
- Upload automático do arquivo .zip para uma pasta específica no Google Drive.
- Exclusão de backups antigos no Google Drive para economizar espaço.

## Requisitos

- Python 3.x
- Pip
- Pacotes Python: `google-api-python-client`, `google-auth-httplib2`, `google-auth-oauthlib`
- Credenciais da API do Google Drive (arquivo JSON da conta de serviço, caso não saiba como [confira esse tutorial](https://rclone.org/drive/#making-your-own-client-id)), ou siga esses passos a passos:

### Configurar uma conta de serviço

1. Vá para o Google Cloud Console.
2. Ative a API do Google Drive para o seu projeto.
3. Crie uma conta de serviço e baixe o arquivo de credenciais JSON.
4. Compartilhar a pasta do Google Drive:
No Google Drive, compartilhe a pasta de destino do backup com o e-mail da conta de serviço (algo como <service-account-name@project-id.iam.gserviceaccount.com>)

- Acesso ao banco de dados MySQL

## Instalação

1. Clone este repositório:

   ```sh
   git clone https://github.com/Vini-Paixao/Bot-Drive.git
   cd Bot-Drive
   ```

2. Instale os pacotes Python necessários:

    ```sh
    pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
    ```

3. Coloque suas credenciais da conta de serviço no arquivo service_account.json.

4. Configure o script com o caminho correto para a pasta a ser feita o backup, o nome do arquivo, e o ID da pasta do Google Drive onde os backups serão armazenados.

## Uso

Execute o script Bot-Drive.py:

```sh
python Bot-Drive.py
```

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir um problema ou enviar um pull request.

## Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo ```LICENSE``` para mais detalhes.
