# Aula Referenciada AI

POC de um motor de inteligência artificial para processar aulas gravadas e materiais em PDF.

## Objetivo

Criar um motor capaz de receber um áudio de aula e um PDF de apoio, gerar tópicos da aula, indicar timestamps, resumir os assuntos e relacionar o conteúdo falado com páginas e trechos do material enviado.

## Status do Projeto

POC local em fase de teste controlado.

## Estrutura

```text
src/
  poc_motor_final.py

input/
  aula_teste.mp3
  material_teste.pdf

output/
  resultado_aula.json
  resultado_aula.md
  validacao_manual.csv
  README_VALIDACAO.txt

docs/
  visao_produto.md
  plano_testes.md
  arquitetura.md