import json
from pathlib import Path

def carregar_configuracao(caminho: str) -> dict:
    """
    Carrega a configuração do arquivo JSON especificado.

    Args:
        caminho (str): O caminho para o arquivo de configuração JSON.

    Returns:
        dict: Um dicionário contendo as configurações carregadas.
    """
    BASE_DIR = Path(__file__).resolve().parent.parent
    caminho_arquivo = BASE_DIR / caminho
    
    if not caminho_arquivo.is_file():
        raise FileNotFoundError(f"O arquivo de configuração '{caminho}' não foi encontrado.")

    with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
        configuracao = json.load(arquivo)
        # print(f"Configuração carregada do arquivo '{caminho}': {configuracao}")

    return configuracao

def validar_configuracao(configuracao: dict):
    """
    Valida a configuração carregada.

    Args:
        configuracao (dict): O dicionário de configuração a ser validado.

    Raises:
        ValueError: Se algum campo obrigatório estiver ausente ou inválido.
    """
    campos_obrigatorios = ['diretorio_origem', 'destinos']
    
    if not isinstance(configuracao, dict):
        raise ValueError("A configuração deve ser um dicionário.")
    
    for campo in campos_obrigatorios:
        if campo not in configuracao:
            raise ValueError(f"Campo obrigatório '{campo}' ausente na configuração.")
        
    if not isinstance(configuracao['diretorio_origem'], str):
        raise ValueError("O campo 'diretorio_origem' tem tipo inválido.")
    
    if not isinstance(configuracao['destinos'], dict):
        raise ValueError("O campo 'destinos' tem tipo inválido.")
    
    if not configuracao['diretorio_origem'].strip():
        raise ValueError("O campo 'diretorio_origem' não pode estar vazio.")
    
    if not configuracao['destinos']:
        raise ValueError("O dicionário 'destinos' não pode estar vazio.")