# Visão do Produto — Aula Referenciada AI

## 1. Contexto

A rotina acadêmica, especialmente em cursos com alta carga teórica e grande volume de leitura, exige que o aluno consiga transformar aulas expositivas, gravações e materiais de apoio em conhecimento organizado para estudo e revisão.

No entanto, muitas vezes o conteúdo da aula fica separado dos materiais oficiais disponibilizados pelo professor. O aluno pode ter acesso ao áudio, aos slides ou ao PDF, mas precisa fazer manualmente o trabalho de identificar os pontos principais, localizar referências, revisar páginas importantes e organizar anotações.

A proposta da POC é validar se a inteligência artificial pode apoiar esse processo, transformando uma aula gravada em um relatório estruturado, com tópicos, timestamps, resumo e relação com o material em PDF.

## 2. Problema

Alunos têm dificuldade em transformar aulas gravadas em material de estudo organizado, confiável e conectado ao conteúdo oficial disponibilizado pelo professor.

Além disso, o processo manual de revisar uma aula longa, localizar trechos importantes no material de apoio e criar anotações úteis pode consumir muito tempo e gerar inconsistências.

Também existe o risco de o aluno estudar por resumos desconectados do conteúdo validado pelo professor, o que pode comprometer a qualidade da revisão.

## 3. Solução Proposta

Criar um motor de inteligência artificial capaz de receber:

- um áudio de aula;
- um PDF de apoio;
- regras de validação;
- um schema estruturado de saída.

A partir desses arquivos, o motor deverá:

- identificar os principais tópicos abordados na aula;
- estimar os timestamps de início e fim de cada tópico;
- gerar um resumo objetivo do que foi falado;
- listar os conceitos principais;
- relacionar cada tópico com páginas e trechos do PDF;
- indicar o grau de confiança da correspondência;
- apontar quando não houver referência encontrada no material.

## 4. Objetivo da POC

Validar se é tecnicamente possível cruzar uma aula gravada com um PDF de apoio e gerar um relatório estruturado que auxilie na revisão do conteúdo.

A POC não tem como objetivo criar uma plataforma completa neste primeiro momento. O foco é testar o núcleo do produto: o motor de análise e correlação entre áudio e material didático.

## 5. Hipótese do Produto

A hipótese principal é que um motor de IA pode reduzir o esforço manual de organização da aula, ajudando o aluno e o professor a transformar uma gravação em um material de estudo mais estruturado, rastreável e auditável.

A POC será considerada promissora se o motor conseguir:

- identificar os tópicos principais da aula;
- gerar timestamps minimamente coerentes;
- relacionar tópicos com páginas corretas do PDF;
- citar trechos reais do material;
- não inventar referências quando não houver correspondência;
- gerar artefatos úteis para validação humana.

## 6. Público-Alvo Futuro

Embora esta POC seja apenas técnica, o produto final poderá atender:

- alunos que precisam revisar aulas;
- professores que desejam disponibilizar material de apoio validado;
- instituições de ensino que desejam organizar melhor o conteúdo acadêmico;
- coordenações pedagógicas interessadas em acompanhar a qualidade do estudo e da revisão.

## 7. Escopo Inicial da POC

A primeira versão contempla:

- processamento de um áudio curto de aula;
- processamento de um PDF de apoio;
- análise multimodal com IA;
- retorno estruturado por schema Pydantic;
- geração de tópicos da aula;
- geração de timestamps estimados;
- geração de resumo por tópico;
- identificação de conceitos principais;
- associação com páginas e trechos do PDF;
- classificação de confiança: `alta`, `media` ou `nenhuma`;
- geração de JSON estruturado;
- geração de relatório em Markdown;
- geração de CSV para auditoria humana;
- geração de README de validação.

## 8. Fora do Escopo Inicial

Nesta fase, não serão implementados:

- login;
- tela web;
- aplicativo mobile;
- cadastro de professor;
- cadastro de aluno;
- banco de dados;
- deploy em servidor;
- dashboard administrativo;
- chat entre alunos;
- validação automática de presença;
- banco de questões;
- flashcards;
- revisão espaçada;
- integração com sistema acadêmico;
- armazenamento permanente dos arquivos;
- revisão automática sem validação humana.

## 9. Critérios de Valor

O motor terá valor inicial se conseguir gerar uma saída que possa ser revisada por uma pessoa e usada como base para estudo.

Os principais sinais de valor são:

- economia de tempo na organização da aula;
- identificação clara dos tópicos abordados;
- relação útil entre fala do professor e material de apoio;
- saída estruturada e fácil de auditar;
- redução de referências inventadas;
- possibilidade futura de validação pelo professor.

## 10. Riscos Conhecidos

A POC possui riscos técnicos importantes:

- a IA pode gerar timestamps aproximados;
- a IA pode indicar páginas incorretas;
- a IA pode confundir página sequencial do PDF com página impressa do livro;
- a IA pode citar trechos de forma imprecisa;
- a IA pode tratar uma correspondência conceitual como literal;
- a IA pode inventar referência caso o prompt não seja rígido;
- arquivos longos podem gerar resultados menos confiáveis.

Por isso, nesta fase, todo resultado gerado pelo motor deve passar por auditoria humana.

## 11. Restrições da POC

A POC será executada localmente, por meio de script Python.

Os arquivos de entrada deverão ser colocados manualmente na pasta `input/`, e os resultados serão salvos na pasta `output/`.

A POC utilizará a Gemini API para análise multimodal, mas o objetivo é testar a viabilidade do fluxo, não definir ainda a arquitetura definitiva do produto.

## 12. Próximos Passos

Após a execução dos primeiros testes, a equipe deverá analisar os resultados e decidir se o motor deve evoluir para:

- melhoria de prompt;
- extração do PDF por página antes do envio à IA;
- uso de embeddings e busca semântica;
- arquitetura RAG;
- criação de uma API;
- criação de interface web simples;
- fluxo de validação pelo professor;
- persistência em banco de dados.

## 13. Definição de Sucesso da POC

A POC será considerada bem-sucedida se demonstrar que o motor consegue transformar um áudio curto e um PDF em uma saída organizada, auditável e minimamente confiável para orientar a continuidade do desenvolvimento.

O objetivo não é atingir perfeição nesta etapa, mas obter evidências suficientes para decidir se vale avançar para uma versão mais estruturada do produto.