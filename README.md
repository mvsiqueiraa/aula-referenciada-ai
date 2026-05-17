# Aula Referenciada AI

POC de um motor de inteligência artificial para processar aulas gravadas e materiais em PDF.

## Objetivo

Criar um motor capaz de receber um áudio de aula e um PDF de apoio, gerar tópicos da aula, indicar timestamps, resumir os assuntos e relacionar o conteúdo falado com páginas e trechos do material enviado.

## Status do Projeto

POC local em fase de teste controlado.

## Requisitos

- Python 3.9+
- Chave de API do Google Gemini (`GEMINI_API_KEY`)

## Instalação

1. Clone o repositório ou baixe os arquivos.
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure sua chave de API do Gemini como variável de ambiente. 
   - No Windows: `set GEMINI_API_KEY=sua_chave_aqui` (ou configure nas variáveis de ambiente do sistema)
   - No Linux/Mac: `export GEMINI_API_KEY=sua_chave_aqui`

## Como Executar

1. Coloque o arquivo de áudio da aula (ex: `aula_teste.mp3`) e o PDF de apoio (ex: `material_teste.pdf`) na pasta `input/`.
2. Execute o script principal:
   ```bash
   python src/poc_motor_final.py
   ```
3. Os resultados serão gerados na pasta `output/`, incluindo o JSON estruturado, relatório em Markdown e a planilha para validação manual.

## Estrutura de Diretórios

```text
src/
  poc_motor_final.py       # Script principal de execução

input/
  aula_teste.mp3           # Arquivo de áudio de exemplo
  material_teste.pdf       # Arquivo PDF de exemplo

output/
  resultado_aula.json      # Saída estruturada bruta
  resultado_aula.md        # Relatório legível gerado
  validacao_manual.csv     # Planilha para auditoria humana
  README_VALIDACAO.txt     # Instruções para validação

docs/
  visao_produto.md         # Visão geral do produto e objetivos
  plano_testes.md          # Estratégia de testes da POC
  arquitetura.md           # Documentação arquitetural e de fluxo
```