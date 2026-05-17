import os
import re
import time
import csv
from typing import List, Optional, Literal
from pydantic import BaseModel, Field
from google import genai
from google.genai import types
from google.genai.errors import APIError

# =====================================================================
# 1. SCHEMAS ESTRUTURADOS CONTRA ALUCINAÇÃO
# =====================================================================
class TopicoAula(BaseModel):
    titulo: str = Field(description="Nome claro e objetivo do conceito ou tópico abordado pelo professor.")
    tempo_inicio: str = Field(description="Timestamp estimado de início do assunto no áudio (formato HH:MM:SS).")
    tempo_fim: str = Field(description="Timestamp estimado de término do assunto no áudio (formato HH:MM:SS).")
    resumo_aula: str = Field(description="Síntese precisa e didática do que o professor explicou.")
    conceitos_principais: List[str] = Field(description="Lista de palavras-chave ou termos técnicos essenciais discutidos.")
    pagina_pdf: Optional[int] = Field(
        default=None, 
        description="Número sequencial da página dentro do arquivo PDF, contando a primeira página do arquivo como 1. Não use a numeração impressa do livro."
    )
    trecho_pdf: Optional[str] = Field(default=None, description="Citação direta e exata do trecho do PDF que embase o assunto. Nulo se não houver correspondência.")
    confianca: Literal["alta", "media", "nenhuma"] = Field(description="Grau de certeza da correlação entre a fala e o material.")
    observacao: Optional[str] = Field(default=None, description="Notas adicionais sobre divergências ou comentários.")

class ResultadoAnalise(BaseModel):
    topicos: List[TopicoAula]


# =====================================================================
# 2. VALIDAÇÕES E EXPORTADORES INDEPENDENTES
# =====================================================================
def timestamp_valido(valor: str) -> bool:
    """Valida o formato HH:MM:SS e garante limites lógicos de tempo."""
    if not re.match(r"^\d{2}:\d{2}:\d{2}$", valor):
        return False

    horas, minutos, segundos = map(int, valor.split(":"))
    return minutos < 60 and segundos < 60

def timestamp_para_segundos(valor: str) -> int:
    """Converte uma string HH:MM:SS em segundos absolutos para validação matemática."""
    horas, minutos, segundos = map(int, valor.split(":"))
    return horas * 3600 + minutos * 60 + segundos

def gerar_readme_validacao(caminho_txt: str):
    """Gera o arquivo de instruções de auditoria revisado."""
    texto = (
        "📋 GUIA DE AUDITORIA DO EXPERIMENTO (POC V4.3)\n"
        "=====================================================================\n\n"
        "Este arquivo orienta a validação humana dos dados gerados pelo motor.\n\n"
        "Passo a Passo para o Auditor:\n"
        "1. Abra o arquivo de áudio de teste utilizado.\n"
        "2. Ouça os trechos delimitados e valide se os tempos gerados são fiéis.\n"
        "3. Preencha as colunas 'tempo_inicio_real' e 'tempo_fim_real' no CSV.\n"
        "4. Abra o arquivo PDF correspondente no seu leitor.\n"
        "5. Vá até a página indicada na coluna 'pagina_pdf_gerada'. ATENÇÃO: a página indicada\n"
        "   é a página sequencial do arquivo no leitor de PDF, não o número impresso no rodapé físico do livro.\n"
        "6. Verifique se o texto contido na coluna 'trecho_pdf_gerado' existe literalmente ali.\n"
        "7. Preencha as colunas de métricas analíticas no CSV:\n"
        "   - erro_inicio_segundos / erro_fim_segundos (Diferença observada)\n"
        "   - diferenca_pagina (Quantas páginas de erro o motor cometeu)\n"
        "   - trecho_existe_no_pdf (sim / nao)\n"
        "   - validacao_humana (correto / parcial / errado)\n"
        "8. Anote insights na coluna 'observacao_auditor' para refinar o motor.\n"
    )
    with open(caminho_txt, "w", encoding="utf-8") as f:
        f.write(texto)

def salvar_csv_validacao(dados: ResultadoAnalise, caminho_csv: str):
    colunas = [
        "id_topico", "topico_gerado", "tempo_inicio_gerado", "tempo_fim_gerado",
        "pagina_pdf_gerada", "trecho_pdf_gerado", "confianca_gerada",
        "tempo_inicio_real", "tempo_fim_real", "pagina_real",
        "erro_inicio_segundos", "erro_fim_segundos", "diferenca_pagina",
        "trecho_existe_no_pdf", "validacao_humana", "observacao_auditor"
    ]

    with open(caminho_csv, "w", newline="", encoding="utf-8-sig") as f:
        escritor = csv.writer(f, delimiter=";")
        escritor.writerow(colunas)

        for i, t in enumerate(dados.topicos, 1):
            escritor.writerow([
                i,
                t.titulo,
                t.tempo_inicio,
                t.tempo_fim,
                t.pagina_pdf if t.pagina_pdf is not None else "null",
                t.trecho_pdf if t.trecho_pdf is not None else "null",
                t.confianca,
                "", "", "", "", "", "", "", "", "" 
            ])

def salvar_relatorio_markdown(dados: ResultadoAnalise, caminho_md: str):
    md = "# 📚 Relatório de Aula Referenciada (Instrumentado para Auditoria)\n\n"
    for i, t in enumerate(dados.topicos, 1):
        md += f"## 📍 [{i}] Tópico: {t.titulo}\n"
        md += f"- **⏱️ Tempo Estimado:** `{t.tempo_inicio}` até `{t.tempo_fim}`\n"
        md += f"- **🧠 Conceitos:** {', '.join(t.conceitos_principais)}\n"
        md += f"- **📝 Resumo:** {t.resumo_aula}\n"
        md += f"- **📖 Referência PDF (Arquivo):** Página {t.pagina_pdf if t.pagina_pdf is not None else 'Não encontrada'}\n"
        if t.trecho_pdf: md += f"  > *\"{t.trecho_pdf}\"*\n"
        md += f"- **🎯 Confiança:** `{t.confianca.upper()}`\n\n---\n\n"
    with open(caminho_md, "w", encoding="utf-8") as f: f.write(md)


# =====================================================================
# 3. MOTOR DE EXECUÇÃO DA PLATAFORMA
# =====================================================================
def aguardar_processamento(client: genai.Client, arquivo_upload, timeout_segundos: int = 300):
    print(f"⏳ Verificando processamento de: {arquivo_upload.name}...")
    inicio = time.time()

    while True:
        status_atual = client.files.get(name=arquivo_upload.name)
        estado = str(status_atual.state)

        if "ACTIVE" in estado:
            print(f"   [Ativo] {arquivo_upload.name}")
            return status_atual

        if "FAILED" in estado:
            raise RuntimeError(f"❌ Falha crítica no arquivo {arquivo_upload.name} no servidor.")

        if time.time() - inicio > timeout_segundos:
            raise TimeoutError(f"⏰ Tempo limite excedido ({timeout_segundos}s) ao processar {arquivo_upload.name}.")

        time.sleep(5)

def executar_motor_final(caminho_audio: str, caminho_pdf: str) -> ResultadoAnalise:
    if not os.environ.get("GEMINI_API_KEY"):
        raise ValueError("❌ Erro: A variável de ambiente GEMINI_API_KEY não está configurada.")
    
    client = genai.Client()
    MODELO = os.environ.get("GEMINI_MODEL", "gemini-2.0-flash")
    print(f"🚀 Plataforma com motor ativo: {MODELO}")

    arquivo_audio, arquivo_pdf = None, None

    try:
        print("📤 1/4 - Fazendo upload dos arquivos de laboratório...")
        arquivo_audio = client.files.upload(file=caminho_audio)
        arquivo_pdf = client.files.upload(file=caminho_pdf)

        arquivo_audio = aguardar_processamento(client, arquivo_audio)
        arquivo_pdf = aguardar_processamento(client, arquivo_pdf)

        print("🤖 2/4 - Solicitando mapeamento estruturado para auditoria...")
        
        prompt_instrucao = (
            "Você é o núcleo de inteligência de uma plataforma médica. "
            "Sua missão é cruzar a aula gravada em áudio com o material de leitura em PDF.\n\n"
            "Regras rígidas:\n"
            "- Identifique os blocos de tempo de início e fim no formato HH:MM:SS.\n"
            "- Use como pagina_pdf o número sequencial da página dentro do arquivo PDF, contando a primeira página do arquivo como 1.\n"
            "- Só preencha trecho_pdf se o trecho existir literalmente no PDF enviado.\n"
            "- Se não encontrar correspondência direta no PDF, use pagina_pdf=null, trecho_pdf=null e confianca='nenhuma'.\n"
            "- Não invente páginas, trechos ou referências.\n"
            "- Se a correspondência for conceitual, mas não literal, use confianca='media' e explique na observacao."
        )

        configuracao = types.GenerateContentConfig(
            system_instruction=prompt_instrucao,
            response_mime_type="application/json",
            response_schema=ResultadoAnalise,
            temperature=0.1
        )

        resposta = client.models.generate_content(
            model=MODELO,
            contents=[arquivo_audio, arquivo_pdf, "Execute o cruzamento estruturado com base nos arquivos anexados."],
            config=configuracao
        )

        return resposta.parsed

    except APIError as e:
        print(f"❌ Erro de API: {e}")
        raise
    finally:
        print("🧹 3/4 - Executando rotina isolada de limpeza de arquivos...")
        for arq in [arquivo_audio, arquivo_pdf]:
            if arq:
                try:
                    client.files.delete(name=arq.name)
                    print(f"     Removido: {arq.name}")
                except Exception as e:
                    print(f"     ⚠️ Falha segura ao remover {arq.name}: {e}")


# =====================================================================
# 4. RUNNER DO EXPERIMENTO COM TESTE CRONOLÓGICO SEGURO
# =====================================================================
if __name__ == "__main__":
    CAMINHO_AUDIO = "input/aula_teste.mp3"
    CAMINHO_PDF = "input/material_teste.pdf"

    if not os.path.exists(CAMINHO_AUDIO) or not os.path.exists(CAMINHO_PDF):
        print("⚠️ Insira os arquivos 'aula_teste.mp3' e 'material_teste.pdf' em 'input/' antes de rodar.")
    else:
        cronometro = time.time()
        try:
            # 🚨 CORREÇÃO: Linha corrompida removida e limpa para execução estável
            resultado_objeto = executar_motor_final(CAMINHO_AUDIO, CAMINHO_PDF)
            
            if resultado_objeto is None:
                raise RuntimeError("❌ O modelo falhou em popular o schema estruturado de forma válida.")
            
            # Validação matemática estrita dos timestamps e da ordem linear
            for idx, topico in enumerate(resultado_objeto.topicos, 1):
                if not timestamp_valido(topico.tempo_inicio):
                    raise ValueError(f"❌ Erro no Tópico {idx}: Formato ou valores de tempo_inicio inválidos ('{topico.tempo_inicio}').")
                if not timestamp_valido(topico.tempo_fim):
                    raise ValueError(f"❌ Erro no Tópico {idx}: Formato ou valores de tempo_fim inválidos ('{topico.tempo_fim}').")
                
                # Validação da ordem sequencial do tempo (Garante que o fim não precede o início)
                inicio_segundos = timestamp_para_segundos(topico.tempo_inicio)
                fim_segundos = timestamp_para_segundos(topico.tempo_fim)
                
                if fim_segundos <= inicio_segundos:
                    raise ValueError(f"❌ Erro no Tópico {idx}: tempo_fim ({topico.tempo_fim}) deve ser maior que tempo_inicio ({topico.tempo_inicio}).")

            os.makedirs("output", exist_ok=True)
            
            # Exportação estável dos artefatos
            with open("output/resultado_aula.json", "w", encoding="utf-8") as f:
                f.write(resultado_objeto.model_dump_json(indent=2))
                
            salvar_relatorio_markdown(resultado_objeto, "output/resultado_aula.md")
            salvar_csv_validacao(resultado_objeto, "output/validacao_manual.csv")
            gerar_readme_validacao("output/README_VALIDACAO.txt")
            
            print(f"\n✅ 4/4 - Motor instrumentado com sucesso em {round(time.time() - cronometro, 2)}s.")
            print("💾 Todos os artefatos de auditoria gerados com sucesso na pasta '/output'.")
            
        except Exception as e:
            print(f"\n❌ A POC falhou nos critérios de validação: {e}")