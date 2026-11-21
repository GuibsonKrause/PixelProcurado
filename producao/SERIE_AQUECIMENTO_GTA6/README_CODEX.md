# SÉRIE DE AQUECIMENTO GTA 6 (09/11 a 19/11) — GUIA DE PRODUÇÃO CODEX

Este documento é a instrução mestre para execução e continuidade de produção autônoma via **Codex** (ou Antigravity) no canal **Pixel Procurado**.

---

## 1. Visão Geral e Arquitetura

- **Canal:** Pixel Procurado (Voz oficial: Gemini TTS `gemini-3.8-flash-tts` / ID `voice_iagtq1gnk2br`).
- **Objetivo da Série:** Aquecimento diário com alta retenção (estilo MrBeast/SunnyV2) focado no público gamer adulto, com humor ácido, zero rodeios e sincronia semântica estrita com o acervo visual local em `videosGTAVI/`.
- **Janela de Publicação:** 09/11/2026 até 19/11/2026 (11 episódios diários).
- **Diretório Mestre dos Episódios:** `c:\Users\guibson.krause\Documents\ChatGPT\GamePlay\producao\SERIE_AQUECIMENTO_GTA6\`

---

## 2. Mapa dos 11 Episódios e Checkpoint

| Dia | Data | Tema Central & Gancho | Status Roteiro | Pasta Local |
|---|---|---|---|---|
| **01** | 09/11 | Véspera do Pré-load — O Choque de Realidade nas primeiras 2h | **Concluído** | `DIA_01_2026-11-09/` |
| **02** | 10/11 | Especial Dia do Pré-Load — Os ~212 GB e o Fim do Prédio de Isopor | **Concluído** | `DIA_02_2026-11-10/` |
| **03** | 11/11 | IA Policial Implacável, 6 Estrelas e o Truque da Garagem | **Concluído** | `DIA_03_2026-11-11/` |
| **04** | 12/11 | Ecossistema Vivo e NPCs Bizarros (Only in Leonida) | **Concluído** | `DIA_04_2026-11-12/` |
| **05** | 13/11 | Vida do Crime com Lucia & Jason (Cooperação Tática e Troca) | Planejado no Mapa | `DIA_05_2026-11-13/` |
| **06** | 14/11 | Sistema de Carros, Porta-malas, Rachas e Oficinas | Planejado no Mapa | `DIA_06_2026-11-14/` |
| **07** | 15/11 | 11 Detalhes Doentios Escondidos nos Frames dos Trailers | Planejado no Mapa | `DIA_07_2026-11-15/` |
| **08** | 16/11 | PS5 Base vs PS5 Pro e Xbox Series (Sem Passar Pano) | Planejado no Mapa | `DIA_08_2026-11-16/` |
| **09** | 17/11 | Vida Noturna, Boates e Infiltração de Luxo em Vice City | Planejado no Mapa | `DIA_09_2026-11-17/` |
| **10** | 18/11 | Véspera de Lançamento: Protocolo Tático de 24 Horas | Planejado no Mapa | `DIA_10_2026-11-18/` |
| **11** | 19/11 | Especial de Lançamento: Guia Definitivo do Dia 1 (Sem Spoilers) | Planejado no Mapa | `DIA_11_2026-11-19/` |

---

## 3. Matriz de Comandos de Execução no Codex

Conforme estipulado no [`AGENTS.md`](file:///c:/Users/guibson.krause/Documents/ChatGPT/GamePlay/AGENTS.md), para economizar uso sem perder qualidade, respeite a alocação de modelos por etapa no Codex:

### Passo 1: Locução Gemini TTS (`gpt-6.1-sol` / low)
Execute a geração via powershell chamando o script automatizado do projeto:
```powershell
# Exemplo para o Dia 01
powershell -ExecutionPolicy Bypass -File .\automacao\gerar_narracao_gemini.ps1 `
  -TextoPath "producao\SERIE_AQUECIMENTO_GTA6\DIA_01_2026-11-09\03_NARRACAO_GEMINI.txt" `
  -EstiloPath "producao\SERIE_AQUECIMENTO_GTA6\DIA_01_2026-11-09\04_ESTILO_GEMINI.txt" `
  -SaidaWav "producao\SERIE_AQUECIMENTO_GTA6\DIA_01_2026-11-09\audio\narracao_gemini.wav"
```

### Passo 2: Alinhamento ASR / Transcrição (`gpt-6.1-sol` / low)
Alinhe palavra por palavra para gerar legendas sincronizadas (`.ass` e `.srt`) usando o ambiente Python 3.12:
```powershell
py -3.12 .agents/skills/pixel-procurado-video/scripts/alinhamento_whisper.py `
  --audio "producao\SERIE_AQUECIMENTO_GTA6\DIA_01_2026-11-09\audio\narracao_normalizada.wav" `
  --texto "producao\SERIE_AQUECIMENTO_GTA6\DIA_01_2026-11-09\01_NARRACAO.txt" `
  --saida "producao\SERIE_AQUECIMENTO_GTA6\DIA_01_2026-11-09\legendas\legendas.ass"
```

### Passo 3: Composição da Thumbnail (`imagegen` / `gpt-6.1-sol`)
Componha o texto oficial de até 3 palavras sobre o screenshot de base:
```powershell
py -3.12 .agents/skills/pixel-procurado-thumbnails/scripts/compose_thumbnail.py `
  --base-image "videosGTAVI\_catalogo\indices_detalhados\GTAVI_An_Extended_Look\pagina_04.jpg" `
  --text "ESCOLHA ERRADO..." `
  --output "producao\SERIE_AQUECIMENTO_GTA6\DIA_01_2026-11-09\thumbnail\thumb_dia01.jpg"
```

### Passo 4: Montagem V2 e Render Final FFmpeg (`gpt-6.1-sol` / medium)
Siga os timecodes cravados no arquivo `00_ROTEIRO_COMPLETO.md` de cada episódio, respeitando estritamente o catálogo `videosGTAVI/_catalogo/INDICE_VIDEOS.md`.
Renderize com as flags padronizadas (`blackdetect`, `ebur128` a -16 LUFS e AAC 48 kHz).

### Passo 5: Revisão Independente (QA Final) (`gpt-6-astra` / high)
Obrigatório rodar 1 subagente `high` no final para inspecionar folha de contato (`contact sheet`), decodificação sem drops e sincronia labial/semântica.

---

## 4. Instruções para Continuar a Escrita dos Dias 05 a 11

Quando pedir ao Codex para gerar os próximos episódios (ex: *"Codex, gere o Dia 05"*):
1. **Consulte a seção correspondente em [`MAPA_MESTRE_11_DIAS.md`](file:///c:/Users/guibson.krause/Documents/ChatGPT/GamePlay/producao/SERIE_AQUECIMENTO_GTA6/MAPA_MESTRE_11_DIAS.md)** para o tema, fatia de vídeo e gancho.
2. **Respeite o Tom de Voz**: sem introduções infantis ("Fala galera"), sem termos corporativos, humor ácido de bar e foco nas contradições de quem joga no automático de 2013.
3. **Respeite a Trava do Acervo**: só referencie timecodes e capturas que realmente existam em `videosGTAVI/`.
4. **Entregue a Estrutura Quádrupla**:
   - `00_ROTEIRO_COMPLETO.md`: Roteiro técnico com marcações visuais, timecodes, SFX e base editorial.
   - `01_NARRACAO.txt`: Texto limpo para leitura e legendas.
   - `03_NARRACAO_GEMINI.txt`: Texto com tags de pontuação vocal da API Gemini (`<short pause>`, `<breath>`, etc.).
   - `04_ESTILO_GEMINI.txt`: Prompt conciso para o campo `Style` do TTS.
