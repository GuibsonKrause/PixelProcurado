# Revisão final independente — TRUQUE_NZ_2026-11-15

Data: 2026-11-15 · Revisor: claude-opus-5-5 (subagente; não planejou nem montou) · Resultado: **aprovado_com_ressalvas**
Validador: `py -3.12 automacao/validar_revisao.py producao/TRUQUE_NZ_2026-11-15` → código 0 (também com `--cards qa/revisao_final/cards.json`).

**Não houve escuta humana.** O revisor não ouve áudio: as evidências de áudio são medições do ffmpeg e ASR faster-whisper `small`. É o maior modelo disponível na máquina; medium e large-v3 não estão instalados e não foram baixados.

## Veredito por peça
| Peça | Veredito |
|---|---|
| Longo 4K (389 s) | Publicável. Ressalva: falta uma escuta humana curta dos timecodes da lista |
| Short (75 s) | Publicável. O loop fecha (o último quadro é igual ao primeiro) |
| Vertical integral (389 s, 190 MB) | Publicável. Primeira inspeção visual: nenhum artefato ou faixa verde, cards inteiros |
| Story (22,4 s) | Publicável. Termina em corte seco, sem chamada visual |
| Capa 16:9 | Publicar. Na 2ª rodada o relógio foi retocado para "8 \| 00": retoque aceitável e legível a 320 px; texto, selo e logo inteiros |
| Capa 9:16 | Corrigir antes (média): o arco do mapa parte dos EUA, não do Brasil. O controle parece um DualShock (baixa) |

## Problemas
- ~~**Média** — Capa 16:9: o relógio flip mostra "1 | 10".~~ Corrigido na 2ª rodada (agora "8 | 00"; ver `qa/revisao_final/capas/thumbnail_A_v2_zoom_relogio.jpg` e `thumbnail_A_v2_preview320.jpg`).
- **Média** — Capa 9:16: o mapa sai da América do Norte.
- **Média** — Pronúncias sem escuta humana. O ASR `small` ouviu "troque"/"troco" em truque (17,1 e 166,2 s); a vogal medida é /u/, como nas ocorrências corretas. Ouviu "foga"/"fogo" em folga (33,4, 351,1 e Short 70,6 s), "Alcant"/"álcool" em Auckland (100,8 e 374,3 s), "neus holandês" em neozelandês (107,2 e 301,8 s) e "Barrow Field" em Battlefield (325,7 s). No Short, "da manhã" (~2,2 s) sai rápido.
- **Baixa** — Em 02:20,9 a legenda quebra "Series S" em duas: "...Series" / "S, a localização..." (Longo e Vertical).
- **Baixa, aceitos** — O card "UTC−3 = 16 H" é ambíguo. O Story não tem chamada visual. A linha de detalhe dos cards do Vertical é pequena.

## O que passou
- Nenhum quadro preto e nenhum artefato nos 192 quadros salvos (`qa/revisao_final/<peça>/`, folhas em `qa/revisao_final/folhas/`).
- Todos os cards conferem com a fala e com os números: 16 h, UTC+13, UTC−3, 08:00 de quarta 18/11, 09/11 às 21h, NZ$ 139,95. O card de ilustração das configurações tem rótulo.
- As legendas (SRT do Longo e do Short) têm as mesmas palavras da narração limpa e seguem o alinhamento palavra por palavra.
- Áudio: Longo e Vertical medem −16,7 LUFS (pico −1,3 dBFS); Short −17,1 LUFS; Story −16,7 LUFS. Silêncios acima de 1,2 s só no Longo/Vertical, em 71,98 s (1,33 s) e 368,57 s (1,50 s), ambos pausas de roteiro.
- Os capítulos batem com o alinhamento (00:40,5, 01:26,7, 02:17,9, 02:58,8, 04:07,7, 04:45,0 e 05:36,4). Todas as mídias e capas existem. Maior Instagram: 190 MB (limite 300 MB); YouTube: 791 MB (limite 1 GB).
