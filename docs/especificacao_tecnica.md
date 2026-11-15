# Especificação técnica — Organizador Automático de Arquivos

**Versão da especificação:** 0.1 · **Status:** proposta para validação · **Release alvo:** 1.0

## 1. Objetivo
Organizar arquivos diretamente na pasta de origem, identificando a extensão e movendo somente aqueles com destinos explicitamente configurados. Preservar na origem arquivos não reconhecidos e fornecer relatório ao usuário.

## 2. Premissas
- Windows, execução manual por terminal, Python 3.12 e Poetry.
- Apenas arquivos regulares do primeiro nível; sem recursão.
- Caminhos locais configuráveis; não presumir a localização exata de Downloads.
- Nenhuma interface gráfica, agendamento ou monitoramento contínuo na versão 1.0.

## 3. Fluxo funcional
1. Carregar e validar JSON (estrutura, extensões, origem, destinos).
2. Ler entradas da pasta de origem sem percorrer subpastas.
3. Para cada arquivo: identificar extensão normalizada e aplicar exclusões temporárias.
4. Se extensão não configurada: manter arquivo e registrar `ignorado`.
5. Se configurada: validar origem/destino, colisão e condições mínimas de segurança.
6. Se seguro: mover com `shutil.move`; registrar `movido` ou `erro`.
7. Emitir resumo e log ao término.

## 4. Regras de negócio
| ID | Regra | Resultado esperado |
|---|---|---|
| RN01 | Origem configurável | Ler somente o diretório informado |
| RN02 | Extensões case-insensitive | `.PDF` equivale a `.pdf` |
| RN03 | Mapeamento explícito | Somente extensões configuradas podem ser movidas |
| RN04 | Desconhecidos | Permanecem na origem; constam no relatório |
| RN05 | Colisão de nomes | Não sobrescrever; registrar conflito |
| RN06 | Falha por arquivo | Registrar erro e prosseguir com os demais |
| RN07 | Subpastas | Ignoradas |
| RN08 | Relatório | Totais e nomes por status |
| RN09 | Download em andamento | Ignorar extensões temporárias; verificar estabilidade antes de mover (estratégia a definir na implementação) |
| RN10 | Destino inválido | Não mover; registrar erro |
| RN11 | Configuração inválida | Interromper antes de qualquer movimentação |
| RN12 | Segurança dos caminhos | Impedir que origem e destino coincidam; validar caminhos antes de executar |

## 5. Contrato proposto de configuração JSON
O arquivo `config/destinos.json` será editável pelo usuário e deverá conter:
- `origem`: caminho absoluto da pasta a examinar;
- `destinos`: objeto com chaves de extensão (por exemplo, `.pdf`) e valores de diretório absoluto;
- `extensoes_temporarias`: lista de extensões que não devem ser movidas.

Exemplos de categorias: `.pdf` → Documentos/PDF, `.docx` → Documentos/Word, `.xlsx` → Documentos/Planilhas, `.jpg` e `.png` → Imagens, `.zip` → Compactados.

**Nota:** caminhos do exemplo de configuração são fictícios; substituí-los pelos caminhos reais antes de executar. Não habilitar movimentação enquanto os caminhos não forem validados.

## 6. Módulos
| Módulo | Responsabilidade |
|---|---|
| `src/main.py` | Orquestrar execução e resultado |
| `src/scanner.py` | Listar somente arquivos elegíveis na origem |
| `src/classifier.py` | Normalizar extensões e resolver destinos |
| `src/organizer.py` | Validar e mover sem sobrescrever |
| `src/reporter.py` | Consolidar resultados e registrar logs |

## 7. Estados de processamento
- `movido`: operação concluída com sucesso;
- `ignorado`: extensão desconhecida, arquivo temporário ou item fora do escopo;
- `conflito`: arquivo de mesmo nome já existe no destino;
- `erro`: falha de configuração operacional, permissão, acesso ou movimentação.

O relatório deve conter pelo menos nome do arquivo, status, motivo e destino (quando aplicável), além dos totais.

## 8. Riscos e decisões de implementação
- **Arquivos em gravação:** extensões temporárias não são proteção suficiente. Definir teste de estabilidade e comportamento quando o arquivo estiver bloqueado.
- **Movimentação entre volumes:** `shutil.move` pode efetuar cópia seguida de exclusão; validar em testes antes de usar dados reais.
- **Conflitos e concorrência:** checagem prévia de existência não garante ausência de corrida. Versão inicial será para execução única e manual; implementar estratégia segura e testar.
- **Diretórios inexistentes:** proposta inicial é registrar erro sem criar diretórios automaticamente; decisão revisável.
- **Extensões compostas ou arquivos sem extensão:** permanecem ignorados até regra explícita.

## 9. Critérios de aceitação
1. Arquivo reconhecido é movido ao destino configurado.
2. Extensão desconhecida permanece na origem e aparece no relatório.
3. `.PDF` e `.pdf` seguem a mesma regra.
4. Colisão não sobrescreve arquivo existente.
5. Falha individual não interrompe os outros arquivos.
6. Subpastas e temporários permanecem na origem.
7. Configuração inválida impede qualquer movimentação.
8. Relatório final distingue movidos, ignorados, conflitos e erros.
9. Testes são executados com diretórios e arquivos fictícios antes de usar Downloads real.

## 10. Fora do escopo
Interface gráfica, execução agendada, monitoramento contínuo, organização por data/conteúdo e processamento recursivo.
