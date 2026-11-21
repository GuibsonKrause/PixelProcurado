# Pixel Procurado — Regras do Projeto e Pipeline End-to-End

## 1. Skills do Projeto (fonte em `.agents/skills/`; cópias em `~/.codex/skills/` e `~/.gemini/config/skills/`; atalhos em `.claude/skills/`)

- **`pixel-procurado-roteiro`**: Criação ou revisão de roteiros narrados (longos e Shorts) com humor ácido brasileiro (`producao/editorial/PERFIL_NARRACAO.md`), retenção (`producao/GUIA_ROTEIROS_RETENCAO.md`), gancho de 3 segundos (5–6 palavras sem vinheta/evento antes) e direção visual orientada pelo acervo (`videosGTAVI/_catalogo/`).
- **`pixel-procurado-gemini-tts`**: Geração, validação e normalização de locução via Gemini TTS (`gemini-3.8-flash-tts`, voz `voice_iagtq1gnk2br`) usando `.venv-gemini` e `automacao/gerar_narracao_gemini.ps1`.
- **`pixel-procurado-video`**: Alinhamento palavra por palavra (`faster-whisper` via `py -3.12`), montagem V2 com cards animados breves em **Hyperframes** (`hyperframes.cmd`) ou **Remotion**, composição **FFmpeg**, legendas sincronizadas (`.ass` e `.srt`) e validação técnica determinística (`blackdetect`, `ebur128`, decodificação integral e folhas de contato).
- **`pixel-procurado-thumbnails`**: Geração de arte-base sem texto/logo (via `automacao/gerar_arte_thumbnail.ps1` em qualquer IA; `image-generator`/`imagegen` só como alternativa) e composição determinística de texto/identidade/logo oficial via `py -3.12 .agents/skills/pixel-procurado-thumbnails/scripts/compose_thumbnail.py`.
- **`pixel-procurado-publicacao`**: Pacote completo de publicação (título, descrição, capítulos, tags, comentário fixado, capas) e distribuição multicanal via **Postiz** (`http://localhost:4007`) + **Cloudflare R2** (`automacao/r2_media.py`).
- **`pixel-procurado-producao-completa`**: Orquestração fim a fim do episódio com checkpoint em `producao.json` e revisão independente.

## 2. Ambiente Técnico e Binários Locais

- **Python Audiovisual / Automação / Postiz / R2**: usar sempre `py -3.12` (pacotes compilados em `.course-tools` e `.production-tools/python`: `av`, `PIL`, `faster_whisper`, `numpy`, `imageio_ffmpeg`, `boto3`). Não usar Python 3.14 para scripts que dependem de extensões binárias de `.course-tools`.
- **Python Gemini TTS**: usar `.venv-gemini\Scripts\python.exe` (ou `.\automacao\gerar_narracao_gemini.ps1`), que contém `google-genai` e lê `GEMINI_API_KEY` do ambiente do usuário do Windows.
- **FFmpeg / FFprobe**: disponíveis no `PATH` e em `.production-tools/python/imageio_ffmpeg/binaries/`.
- **Hyperframes CLI**: `hyperframes.cmd` (usado para renderizar camadas transparentes `paineis_v2.mov` dos cards V2).
- **Postiz CLI & API**: `postiz.cmd` conectado a `http://localhost:4007/api` (`POSTIZ_API_KEY` e `POSTIZ_API_URL` nas variáveis de usuário do Windows).
- **Cloudflare R2 (Meta — Instagram e Facebook)**: configurado via `%LOCALAPPDATA%\PixelProcurado\r2.xml` e `.production-tools/postiz-r2.json`, operado por `automacao/r2_media.py`.
- **Armazenamento (Google Drive)**: mídia pesada (vídeo/áudio) mora em `gdrive:GamePlay/<mesmo caminho>`; no projeto fica um link simbólico para `P:\<caminho>` (montagem `rclone` + WinFsp com cache local limitado, iniciada no login por `automacao/montar_drive.ps1`). Os caminhos não mudam: abrir o arquivo baixa sob demanda. Antes de trabalhar, `py -3.12 automacao/armazenamento.py status` (montagem OK?). Para edição pesada de um trecho, `armazenamento.py trazer <pasta> --executar`. Não abrir em lote arquivos do acervo/lives sem necessidade (cada leitura baixa o vídeo) e não fazer busca de texto dentro de `videosGTAVI/_live` ou de mídia.
- **Lives no acervo**: `videosGTAVI/_live/<AAAA-MM-DD>/<canal>/<clipe>/` (helpers `captura_live.pasta_acervo()` e `metas_acervo()`); compilações em `videosGTAVI/_live/_longos/`.
- **Git (GitHub gratuito)**: versiona só código, configuração, skills, textos editoriais e o site do GitHub Pages (raiz: `index.html`, `privacy.html`, `terms.html`, `deletion.html`, arquivos de verificação do TikTok). Mídia, renders, estado de execução, ambientes e segredos ficam no `.gitignore`. O hook `.githooks/pre-commit` (`core.hooksPath`) barra mídia, arquivo > 5 MB e repositório > 100 MB. Ao criar qualquer arquivo novo, decidir se vai para o `.gitignore`; nunca usar `--no-verify` sem autorização. Histórico antigo em `gdrive:GamePlay/_backup/git`.

## 3. Regras Editoriais e de Produção

1. **Roteiros e Voz**:
   - Todo roteiro possui versão limpa (`01_NARRACAO.txt` ou `<ID>_NARRACAO.txt`) e versão anotada (`03_NARRACAO_GEMINI.txt` ou `<ID>_GEMINI.txt`) com as mesmas palavras mais tags pontuais de `producao/editorial/EXPRESSOES_GEMINI.md`.
   - Estilo base em `producao/editorial/ESTILO_NARRACAO_HUMOR_BR.txt` (longos) e `producao/cortes/00_ESTILO_GEMINI_SHORTS.txt` (Shorts).
   - Gancho dos primeiros 3 segundos: 5 a 6 palavras entregando descoberta, contraste ou pergunta concreta no primeiro quadro, sem vinheta ou efeito antes.
2. **Montagem V2 (Padrão `producao/ESPECIAL_PRE_LANCAMENTO_2026-11-06/REVISAO_V2.md`)**:
   - Vídeo pertinente do acervo (`videosGTAVI/_catalogo/`) primeiro; imagens estáticas quando necessárias; cards compactos (720 px no horizontal, 780 px no vertical) que entram na âncora, permanecem apenas pelo tempo de leitura e têm saída animada completa, deixando a cena livre.
3. **Publicação no Postiz (YouTube, Instagram e Facebook)**:
   - Canais ativos no Postiz:
     - YouTube: `cmvsctfgl0001jncj932ovibv` (usa `postiz.upload(path)` local)
     - Facebook: `cmvzyur290001pddwolrt33em` (usa `R2Media().stage(path)` via Worker R2)
     - Instagram: `cmvzyw7vj0003pddwkgtivv8i` (usa `R2Media().stage(path)` via Worker R2)
   - Quando publicar episódio longo no Instagram, incluir as peças compatíveis (vídeo integral verticalizado leve, corte curto como Reel, Story e/ou Carrossel conforme o pacote do episódio).
   - Registrar estado e IDs em `POSTIZ_ESTADO.json` e remover objetos do R2 somente após confirmação `PUBLISHED` com `releaseURL`.

## 3.1. Ferramentas padrão (iguais em Claude, Codex e Antigravity)

Não criar scripts por episódio. O agente preenche dados e roda as ferramentas abaixo (`py -3.12` a partir da raiz):

| Etapa | Ferramenta |
|---|---|
| Armazenamento e cotas (sempre no início de cada produção; também roda diariamente) | `automacao/armazenamento.py automatico --excluir <pasta atual> [--executar]` (simulação por padrão): arquiva no Drive lives de dias anteriores e episódios sem mídia alterada há 48 h, remove intermediários de publicados há 7 dias e aplica cotas no Drive (lives 400 GB, publicados 500 GB; acima de 100% apaga até 85%, menor valor/GB primeiro, degradando antes de apagar). Regras em `automacao/armazenamento.json`. Antes rode `distribuir_postiz.py --status` |
| Checkpoint `producao.json` | `automacao/checkpoint.py novo / etapa / validar / migrar` (formato em `automacao/schemas/producao.schema.json`; nunca editar à mão) |
| Montagem V2, amostra e render | `automacao/pipeline/produzir_v2.py --episodio <pasta>` lendo `<pasta>/episodio.json` (modelo em `automacao/pipeline/episodio.modelo.json`, guia em `automacao/pipeline/README.md`) |
| Pré-voo da direção (antes de renderizar) | `automacao/pipeline/prevoo_v2.py --episodio <pasta>` (pretos nas janelas, timeline x narração, rótulos obrigatórios, folhas de contato em `montagem/prevoo/`) |
| QA técnico | `automacao/pipeline/validar_v2.py --episodio <pasta>` |
| Arte-base da thumbnail | `.\automacao\gerar_arte_thumbnail.ps1` (Gemini, cobrado por imagem); composição continua em `compose_thumbnail.py` |
| Distribuição Postiz + R2 | `automacao/pipeline/distribuir_postiz.py --episodio <pasta>` (plano); `--publicar` só com autorização explícita |
| Cobertura de live (Twitch/YouTube) | Skill `pixel-procurado-live` (exemplo de prompt em `.agents/skills/pixel-procurado-live/references/PROMPT_EXEMPLO.md`): `automacao/live_multi.py iniciar <urls> [--publicar] [--narrar] --imagem auto\|prompt` (varias lives), `status`, `parar`; núcleo em `captura_live.py` (`gravar`, `auto`, `marcar`, `parar`, `recortar`); `live_publicar.py` (empacotar/publicar), `live_narrar.py` (TTS faturável), `live_thumb.py` (imagem: `auto` = API em Codex/Antigravity; `prompt` = só o prompt no Claude, sem gastar API de imagem), `live_longo.py` (compilação), `live_metricas.py` (métricas/calibragem), `live_aviso.py`. Clipes em `videosGTAVI/_live/` (índice `INDICE_LIVE.md`). Requer `streamlink`. Publicação só de clipes aprovados pelo filtro e após o usuário aprovar no chat (arquivo `videosGTAVI/_live/<nome>/APROVADO`). Respeitar a política da Rockstar (sem vazamentos, spoilers ou cinemáticas isoladas) |
| Revisão final independente | `automacao/validar_revisao.py <pasta> --modelo <mp4>` gera o modelo; aprovação só vale se `automacao/validar_revisao.py <pasta>` sair com código 0 (`REVISAO_FINAL.json` com evidências e sha256 dos artefatos atuais) |

**Ordem que evita retrabalho**: (1) conferir no quadro do acervo cada afirmação visual do roteiro ANTES da voz; (2) revisão independente nas folhas do pré-voo, vídeo só em `--amostra`; (3) segunda revisão só nos trechos alterados; (4) um processo pesado por vez; (5) `"limite_mb"` no formato para peças com teto de tamanho (Instagram 300 MB). Detalhes em `automacao/pipeline/README.md` e na skill `pixel-procurado-producao-completa`.

Se faltar um recurso (ex.: matriz 4K por rede, TikTok), estender a ferramenta genérica com opção configurável, em vez de copiar um script para o episódio.

**Skills**: a fonte única é `.agents/skills/`. Depois de editar qualquer skill, rodar `.\automacao\sincronizar_skills.ps1` (copia para `~/.codex/skills` e `~/.gemini/config/skills`, com backup, e confere os atalhos de `.claude/skills/`). `.\automacao\sincronizar_skills.ps1 -Verificar` só confere.

## 4. Política Estrita de Economia de Usage e Roteamento de Modelos

Para preservar a cota (usage) sem perder qualidade editorial ou técnica, **NUNCA use o modelo mais caro (`pro` / `high`) para trabalho rotineiro, execução de scripts, transcrição, renderização ou empacotamento**.

1. **Coordenador Leve**:
   - Se a conversa principal estiver em um modelo avançado (`pro`), o agente principal atua apenas como **coordenador leve** (gerencia `producao.json`, toma decisões críticas e delega o trabalho operacional via `invoke_subagent` especificando explicitamente `Model="flash"` ou `Model="flash_lite"`, nunca deixando o default `Model="inherit"` para tarefas operacionais).
   - Agrupe etapas compatíveis do mesmo nível (`flash` ou `flash_lite`) no mesmo subagente executor para não recriar contexto sem necessidade.

2. **Matriz de Modelos por Etapa da Produção**:

| Etapa do Pipeline | Antigravity (`invoke_subagent`) | Codex (`spawn_agent`) | Justificativa de Usage |
|---|---|---|---|
| **1. Descoberta e inventário de arquivos** | `Model="flash_lite"` | `gpt-6.1-sol` (`low`) | Leitura rápida de caminhos e checkpoints. |
| **2. Anotação do roteiro para Gemini TTS** | `Model="flash"` | `gpt-6.1-sol` (`medium`) | Inserção de tags expressivas sem alterar palavras. |
| **3. Geração TTS, normalização e alinhamento ASR** | `Model="flash_lite"` | `gpt-6.1-sol` (`low`) | Execução determinística de `gerar_narracao_gemini.ps1` e `faster-whisper`. |
| **4a. Direção da montagem (padrão V2 / Shorts)** | `Model="flash"` | `gpt-6.1-sol` (`medium`) | Segue catálogo `videosGTAVI/_catalogo/` e padrão V2 já estabelecido. |
| **4b. Direção da montagem (apenas casos inéditos/complexos)** | `Model="pro"` | `gpt-6-astra` (`high`) | **Uso restrito**: somente quando não houver direção prévia e houver ambiguidade visual complexa. |
| **5. Implementação da edição (Timeline, Hyperframes, Legendas)** | `Model="flash"` | `gpt-6.1-sol` (`medium`) | Montagem de código/JSON, geração `.ass`/`.srt` e render de amostra. |
| **6. Render final FFmpeg e QA técnico determinístico** | `Model="flash_lite"` | `gpt-6.1-sol` (`low`) | Execução de scripts (`blackdetect`, `ebur128`, pranchas de contato). |
| **7. Thumbnail (Arte-base + Composição)** | `TypeName="image-generator"` + `Model="flash"` | `imagegen` + `gpt-6.1-sol` (`medium`) | Arte gerada pelo subagente de imagem; composição via `compose_thumbnail.py`. |
| **8. Pacote de publicação e envio Postiz + R2** | `Model="flash"` (textos) / `Model="flash_lite"` (upload) | `gpt-6.1-sol` (`medium` / `low`) | Redação de metadados em `flash` e upload/stage R2 em `flash_lite`. |
| **9. Revisão final independente (QA Editorial e Visual)** | `Model="pro"` | `gpt-6-astra` (`high`) | **Obrigatório**: 1 subagente `pro` independente inspeciona folhas de contato, timecodes, áudio e capa final. |

3. **Regras Anti-Desperdício e Fallback para Claude**:
   - Nunca faça polling em loop aguardando TTS, ASR, FFmpeg ou Postiz.
   - Nunca passe `Model="inherit"` ao invocar subagentes operacionais se o agente principal for `pro`; defina explicitamente `Model="flash"` ou `Model="flash_lite"`.
   - Se a Revisão Final (`pro`) apontar ajustes objetivos (ex.: corrigir um timecode, trocar um card ou reajustar volume), aplique a correção usando o executor `flash` e revalide apenas o trecho afetado.
   - **Fallback para Família Claude quando a cota Gemini esgotar (autorizado pelo usuário)**:
     - Se o usage dos modelos Gemini (`Gemini 3.8 Flash` ou `Gemini 4 Argon`) atingir o limite ou falhar por cota, está expressamente autorizado alternar o chat principal ou os subagentes (`Model="inherit"`) para a família Claude.
     - **Ordem de prioridade e custo no Claude**:
       1. **Claude Sonnet 5.5**: primeira escolha para substituir o Gemini no chat e em tarefas operacionais/montagem/revisão (equilíbrio ideal de inteligência com uso moderado).
       2. **Claude Opus 5.5**: acionado apenas para revisão crítica profunda ou direção editorial complexa se o Sonnet também não estiver disponível ou a pedido explícito.
       3. **Claude Fable 5.2** (reserva): usar somente quando o Opus 5.5 estiver indisponível ou com cota esgotada, e apenas nas mesmas etapas reservadas ao Opus (direção inédita/complexa e revisão final independente). Custa cerca de 2× o Opus; nunca usar em tarefas operacionais.
