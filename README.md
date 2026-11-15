# Organizador Automático de Arquivos

Aplicação CLI em Python para organizar arquivos da pasta Downloads conforme suas extensões, utilizando um arquivo JSON para definir os diretórios de destino. Arquivos sem regras de classificação permanecem na origem e serão informados em um relatório.

> **Status:** em desenvolvimento — etapa 03 (estrutura e configuração da aplicação). A movimentação de arquivos ainda não foi implementada.

## Funcionalidades previstas (v1.0)

- Execução manual no Windows, processando apenas arquivos do primeiro nível da pasta de origem.
- Classificação por extensão, sem diferenciar letras maiúsculas e minúsculas.
- Configuração de origem e destinos em `config/config.json`.
- Preservação de arquivos com extensões não configuradas, arquivos temporários e subpastas.
- Manutenção do arquivo na origem quando o diretório de destino não existir.
- Prevenção de sobrescrita em caso de nomes de arquivo conflitantes.
- Relatório final de arquivos movidos, ignorados, conflitos e erros.
- Continuidade do processamento quando ocorrer erro em um arquivo.

## Progresso

| Etapa | Situação |
| --- | --- |
| 01 — Modelagem e especificação | Concluída |
| 02 — Ambiente Python, Poetry e Git | Concluída |
| 03 — Estrutura e configuração | Em andamento |
| 04 — Implementação do organizador | Pendente |
| 05 — Testes e finalização | Pendente |

**Já implementado:** leitura do JSON em `carregar_configuracao()` e validação inicial em `validar_configuracao()`, incluindo tipo do objeto, chaves obrigatórias, tipos de `diretorio_origem` e `destinos` e valores vazios. Os testes manuais realizados até aqui confirmaram os comportamentos avaliados.

**Pendente na etapa 03:** validar extensões e caminhos configurados, concluir a documentação e consolidar o versionamento.

## Estrutura do projeto

```text
organizador_de_arquivos/
├── config/
│   └── config.json
├── docs/
│   └── especificacao_tecnica.md
├── src/
│   ├── __init__.py
│   ├── configuracao.py
│   ├── organizador.py
│   └── relatorio.py
├── tests/
├── main.py
├── pyproject.toml
├── poetry.lock
├── .gitignore
└── README.md
```

Os módulos `organizador.py`, `relatorio.py` e o ponto de entrada `main.py` estão preparados estruturalmente, mas ainda não possuem a lógica de execução. A pasta `tests/` está reservada para testes futuros.

## Tecnologias

- **Python 3.11.3**
- **Poetry** para gerenciamento do ambiente e das dependências
- **Git e GitHub** para versionamento
- Bibliotecas padrão do Python: `json` e `pathlib` (em uso); `os` e `shutil` (previstas para a organização dos arquivos)

## Configuração

O arquivo `config/config.json` associa extensões aos diretórios de destino:

```json
{
  "diretorio_origem": "C:/Users/usuario/Downloads",
  "destinos": {
    ".pdf": "C:/Arquivos/Documentos",
    ".jpg": "C:/Arquivos/Imagens"
  }
}
```

Os caminhos acima são ilustrativos. Os diretórios devem ser ajustados para cada computador; a aplicação não criará automaticamente destinos inexistentes.

Para verificar a sintaxe do JSON no ambiente Poetry:

```bash
poetry run python -m json.tool config/config.json
```

Esse comando valida apenas a sintaxe do arquivo, **não executa a organização**.

## Documentação

- [Especificação técnica](docs/especificacao_tecnica.md)

## Próximos passos

Concluir a validação dos valores internos de `destinos` e dos caminhos configurados; em seguida, implementar a identificação, classificação, movimentação segura e geração de relatórios.
