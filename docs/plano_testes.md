# Plano de Testes — POC Aula Referenciada AI

## Objetivo do Teste

Validar se o motor da POC consegue processar um áudio curto de aula e um PDF de apoio, identificando tópicos relevantes, timestamps coerentes, páginas relacionadas e trechos do material que sustentem o conteúdo falado.

O teste também busca medir se o motor evita inventar referências quando determinado conteúdo da aula não estiver presente no PDF.

## Escopo do Teste Inicial

Esta etapa contempla apenas testes locais e controlados.

Será utilizado:

- 1 áudio curto de aula;
- 1 PDF de apoio;
- execução local do script `src/poc_motor_final.py`;
- validação manual dos resultados gerados.

Esta etapa não contempla:

- interface web;
- login de usuários;
- banco de dados;
- deploy em servidor;
- validação automática por professor;
- processamento de aulas longas.

## Massa de Teste Inicial

A massa de teste inicial deve ser simples e controlada.

### Áudio

- Duração aproximada: 5 minutos;
- Formato recomendado: `.mp3`;
- Conteúdo dividido em 3 tópicos principais.

### PDF

- Tamanho recomendado: 5 a 10 páginas;
- Deve conter parte dos assuntos mencionados no áudio;
- Deve ter pelo menos um conteúdo literal, um conteúdo conceitual e deixar um conteúdo propositalmente ausente.

## Estrutura Recomendada do Áudio

O áudio de teste deve seguir esta lógica:

```text
00:00 – 00:40
Abertura e apresentação do tema

00:40 – 01:50
Tópico 1: conteúdo com correspondência literal no PDF

01:50 – 03:00
Tópico 2: conteúdo com correspondência conceitual no PDF

03:00 – 04:10
Tópico 3: conteúdo ausente no PDF

04:10 – 05:00
Fechamento e revisão dos pontos principais
````

## Tipos de Correspondência Testados

### Correspondência Literal

O assunto falado no áudio aparece no PDF com texto muito próximo ou igual.

Resultado esperado:

* `pagina_pdf` preenchida;
* `trecho_pdf` preenchido;
* `confianca = "alta"`.

### Correspondência Conceitual

O assunto falado no áudio aparece no PDF com palavras diferentes, mas com sentido semelhante.

Resultado esperado:

* `pagina_pdf` pode ser preenchida;
* `trecho_pdf` pode ser preenchido se houver trecho relacionado;
* `confianca = "media"`;
* campo `observacao` deve explicar a relação conceitual.

### Conteúdo Ausente no PDF

O professor menciona um conteúdo que não está presente no material enviado.

Resultado esperado:

* `pagina_pdf = null`;
* `trecho_pdf = null`;
* `confianca = "nenhuma"`;
* campo `observacao` deve indicar que não foi encontrada correspondência no PDF.

## Critérios de Avaliação

### 1. Timestamps

Os timestamps serão avaliados comparando o tempo gerado pela IA com o tempo real identificado manualmente pelo auditor.

Classificação:

* Excelente: erro de até 10 segundos;
* Aceitável: erro entre 11 e 30 segundos;
* Ruim: erro acima de 30 segundos.

O campo `tempo_fim` deve ser sempre maior que `tempo_inicio`.

### 2. Página do PDF

A página indicada deve representar a página sequencial do arquivo PDF, considerando a primeira página do arquivo como página 1.

Classificação:

* Correto: a página indicada contém o trecho ou assunto correspondente;
* Parcial: a página indicada é próxima ou contém conteúdo relacionado, mas incompleto;
* Errado: a página indicada não contém o assunto indicado.

### 3. Trecho do PDF

O trecho citado deve existir no PDF.

Classificação:

* Correto: o trecho existe literalmente na página indicada;
* Parcial: o trecho é semelhante, mas não literal;
* Errado: o trecho não existe ou foi inventado.

### 4. Confiança

O campo `confianca` será validado conforme a relação entre a aula e o PDF.

Valores esperados:

* `alta`: correspondência direta, literal e verificável;
* `media`: correspondência conceitual, mas não literal;
* `nenhuma`: ausência de correspondência no PDF.

Erro crítico:

* O motor marcar `confianca = "alta"` quando a página ou o trecho estiverem incorretos.

## Artefatos Gerados

Após a execução da POC, o motor deve gerar os seguintes arquivos na pasta `output/`:

```text
output/
  resultado_aula.json
  resultado_aula.md
  validacao_manual.csv
  README_VALIDACAO.txt
```

### `resultado_aula.json`

Contém a saída estruturada da análise.

### `resultado_aula.md`

Contém um relatório legível para revisão rápida.

### `validacao_manual.csv`

Arquivo usado para auditoria humana dos resultados.

### `README_VALIDACAO.txt`

Arquivo com instruções para orientar o preenchimento da auditoria.

## Preenchimento da Auditoria Manual

O arquivo `output/validacao_manual.csv` deve ser preenchido manualmente com:

* tempo real de início;
* tempo real de fim;
* página real correta;
* erro de início em segundos;
* erro de fim em segundos;
* diferença de página;
* confirmação se o trecho existe no PDF;
* validação humana: `correto`, `parcial` ou `errado`;
* observações do auditor.

## Métricas do Teste

Após o preenchimento da planilha, devem ser observadas as seguintes métricas:

* percentual de tópicos identificados corretamente;
* percentual de timestamps aceitáveis;
* percentual de páginas corretas;
* percentual de trechos reais encontrados no PDF;
* percentual de erros com `confianca = "alta"`;
* quantidade de referências inventadas;
* quantidade de conteúdos ausentes corretamente marcados como `nenhuma`.

## Critério de Sucesso da POC

A POC será considerada promissora se:

* os principais tópicos da aula forem identificados corretamente;
* a maioria dos timestamps estiver dentro da faixa aceitável;
* a maioria das páginas indicadas estiver correta;
* os trechos citados existirem no PDF;
* conteúdos ausentes forem marcados com `confianca = "nenhuma"`;
* o motor não apresentar alucinações graves com `confianca = "alta"`.

## Critério de Falha da POC

A POC será considerada problemática se:

* o motor inventar páginas com frequência;
* o motor citar trechos inexistentes;
* conteúdos ausentes forem tratados como encontrados;
* timestamps ficarem muito distantes do tempo real;
* `confianca = "alta"` aparecer em respostas incorretas.

## Decisão Após o Teste

Após a auditoria, a equipe deverá decidir entre:

1. Manter o fluxo atual e testar com uma aula maior;
2. Ajustar o prompt e repetir o teste curto;
3. Migrar para uma abordagem mais controlada, extraindo o PDF por página antes de enviar para a IA;
4. Iniciar uma arquitetura com busca semântica e RAG.

