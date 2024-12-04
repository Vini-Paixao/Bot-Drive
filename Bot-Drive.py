import os
import subprocess
from datetime import datetime
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials

# Caminho para as credenciais da API do Google Drive
CREDENTIALS_FILE = 'caminho_para_seu_arquivo'

# Pasta no Google Drive onde os backups serão armazenados
DRIVE_FOLDER_ID = 'ID_da_sua_pasta'

def authenticate_drive():
    """Autentica na API do Google Drive usando uma conta de serviço."""
    SCOPES = ['https://www.googleapis.com/auth/drive.file']
    credentials = Credentials.from_service_account_file(
        'service_account.json', scopes=SCOPES
    )
    return build('drive', 'v3', credentials=credentials)

def list_files(service, folder_id, query):
    """Lista arquivos em uma pasta específica do Google Drive que correspondem a uma consulta."""
    try:
        results = service.files().list(
            q=f"'{folder_id}' in parents and {query}",
            fields="files(id, name)"
        ).execute()
        return results.get('files', [])
    except HttpError as error:
        print(f"Erro ao listar arquivos: {error}")
        return []

def delete_file(service, file_id):
    """Exclui um arquivo do Google Drive."""
    try:
        service.files().delete(fileId=file_id).execute()
        print(f"Arquivo com ID {file_id} excluído com sucesso.")
    except HttpError as error:
        print(f"Erro ao excluir arquivo com ID {file_id}: {error}")

def create_zip(target_folder, zip_name):
    """Cria um arquivo .zip usando o comando do Linux."""
    if not os.path.exists(target_folder):
        raise FileNotFoundError(f"A pasta {target_folder} não existe.")

    # Obter a data atual no formato desejado
    current_date = datetime.now().strftime("%d-%m-%Y")

    zip_path = f"{zip_name}_{current_date}.zip"

    # Criar dump do banco de dados
    dump_file = "bkp_banco.sql"
    with open(dump_file, 'w') as f:
        subprocess.run(
            ["mysqldump", "-u", "user", "-psenha", "nome do banco de dados"],
            stdout=f,
            check=True
        )
    # Adicionar o dump e a pasta alvo ao arquivo ZIP em uma única chamada
    subprocess.run(["zip", "-r", zip_path, dump_file, target_folder], check=True)

    # Remover o arquivo dump após adicioná-lo ao ZIP
    os.remove(dump_file)
    return zip_path

def upload_to_drive(service, file_path):
    """Faz upload do arquivo para a pasta especificada no Google Drive."""
    file_metadata = {
        'name': os.path.basename(file_path),
        'parents': [DRIVE_FOLDER_ID]
    }
    media = MediaFileUpload(file_path, mimetype='application/zip')
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f"Arquivo enviado para o Google Drive com ID: {file.get('id')}")

def main():
    # Caminho da pasta a ser compactada
    target_folder = "Caminha para a pasta a ser feita o backup"
    zip_name = "nome do arquivo"

    # Prefixo do nome dos arquivos de backup antigos a serem excluídos
    backup_prefix = 'sufixo do arquivo sem a data'

    try:
        # Passo 1: Autenticar e fazer upload para o Google Drive
        print("Autenticando no Google Drive...")
        service = authenticate_drive()

        # Passo 2: Lista arquivos antigos que correspondem ao prefixo
        files_to_delete = list_files(service, DRIVE_FOLDER_ID, f"name contains '{backup_prefix}'")
        
        # Exclui arquivos antigos
        for file in files_to_delete:
            delete_file(service, file['id'])
        
        # Passo 3: Criar o backup em .zip
        print("Gerando arquivo .zip...")
        zip_path = create_zip(target_folder, zip_name)
        print(f"Arquivo {zip_path} criado com sucesso!")

        # Passo 4: Fazer upload do novo arquivo de backup
        print("Fazendo upload para o Google Drive...")
        upload_to_drive(service, zip_path)

        # Passo 5: Limpeza opcional
        os.remove(zip_path)
        print(f"Arquivo local {zip_path} removido após upload.")
    except Exception as e:
        print(f"Erro durante a execução: {e}")

if __name__ == '__main__':
    main()
