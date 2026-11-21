# L03 — direção e passagem para execução da voz

Fonte de fala: `producao/L03/01_NARRACAO.txt`. Direção editorial: `producao/L03/02_DIRECAO_E_FONTES.md`. Ambos permanecem intactos. Formato do vídeo: longo, 16:9, 3840 × 2160, 30 fps. A voz validada será o relógio mestre da montagem.

Esta etapa preparou texto e estilo; não chamou a API e não gerou áudio. Modelo e voz definidos pela integração: `gemini-3.8-flash-tts` / `voice_iagtq1gnk2br`. O executor deverá registrar os valores efetivamente usados e o formato obtido.

## Arquivos e divisão recomendada

`L03_INTEGRAL_GEMINI.txt` é a cópia integral de referência. Para geração, usar somente os cinco blocos abaixo, em ordem, com `ESTILO_GEMINI.txt` no campo Style. Não usar glob `*_GEMINI.txt`, pois incluiria a versão integral e duplicaria a narração.

| Arquivo | Parágrafos originais | Palavras | Duração estimada a 155–135 ppm, antes das pausas |
|---|---:|---:|---:|
| `L03_B01_P01-P03_GEMINI.txt` | 1–3 | 121 | 46,8–53,8 s |
| `L03_B02_P04-P07_GEMINI.txt` | 4–7 | 210 | 81,3–93,3 s |
| `L03_B03_P08-P12_GEMINI.txt` | 8–12 | 224 | 86,7–99,6 s |
| `L03_B04_P13-P16_GEMINI.txt` | 13–16 | 182 | 70,5–80,9 s |
| `L03_B05_P17-P19_GEMINI.txt` | 17–19 | 157 | 60,8–69,8 s |

Total: 894 palavras, 19 parágrafos. Faixa estimada: 5min46s–6min37s antes das pausas. A abertura tem 42 palavras: aproximadamente 16,3–18,7 segundos antes das pausas. Esses valores são estimativas editoriais, não timecodes nem garantias de execução do TTS. Não esticar o áudio para cumprir duração.

As duas perguntas internas ficam no mesmo bloco que suas respostas; a piada do frigobar permanece completa no bloco 4. Os cortes ficam em fronteiras de parágrafos e de assunto. Reutilizar blocos aprovados se algum exigir nova tentativa.

## Pausas, intenção e pronúncia

- P1: curiosidade concreta; relevo discreto para “a plateia” e “o celular”. Sem introdução adicional.
- P4–P7: calor de reconhecimento. P5 separa os dois anos com duas tags `<short pause>`; os anos permanecem escritos por extenso como no original.
- P8 e P13: uma `<short pause>` no fim de cada pergunta. Não criar suspense longo; começar a resposta logo depois.
- P9–P12: observação e leitura pessoal. A recorrência de “Às vezes” usa a pontuação original, sem tags extras.
- P14: uma `<short pause>` entre “frigobar.” e “Imaginar,”. Humor seco e breve, sem `<chuckle>` ou efeito de meme.
- P15–P17: enumeração legível e contraste de pontos de vista; não acelerar a lista.
- P18: segurança na resposta em três partes. P19: curiosidade na pergunta final; nenhum acréscimo depois.

Há exatamente cinco tags, todas `<short pause>`. A direção persistente está apenas no estilo. Nenhuma grafia de nome próprio foi alterada: a conferência do áudio deve escutar Vice City, Tommy Vercetti, Real Dimez, GTA seis e Rockstar, além dos dois anos. Divergência de ASR em nome estrangeiro é pista de revisão, não prova de erro. A escolha de pronúncia deve ser consistente entre blocos; não reescrever palavras silenciosamente.

## Integração local e comando para o executor

O Python `automacao/gemini_tts.py` já aceita `--style-file` e `--output-dir`. O atalho `automacao/gerar_narracao_gemini.ps1`, na inspeção desta etapa, só expunha `Roteiros`, `Todos` e `DryRun`. O coordenador autorizou o executor de áudio a acrescentar ao wrapper dois parâmetros opcionais `[string]$StyleFile` e `[string]$OutputDir`, encaminhando `--style-file`/`--output-dir` somente quando preenchidos. Preservar os defaults existentes, a leitura segura da chave e a seleção de `.venv-gemini/Scripts/python.exe`. Esta etapa não alterou o wrapper.

Após essa extensão mínima, executar da raiz do projeto:

```powershell
$roteirosL03 = @(
    'producao/L03/voz/L03_B01_P01-P03_GEMINI.txt',
    'producao/L03/voz/L03_B02_P04-P07_GEMINI.txt',
    'producao/L03/voz/L03_B03_P08-P12_GEMINI.txt',
    'producao/L03/voz/L03_B04_P13-P16_GEMINI.txt',
    'producao/L03/voz/L03_B05_P17-P19_GEMINI.txt'
)
.\automacao\gerar_narracao_gemini.ps1 -Roteiros $roteirosL03 -StyleFile 'producao/L03/voz/ESTILO_GEMINI.txt' -OutputDir 'producao/L03/voz/gemini/bruto_v1' -DryRun
```

Confirmar que o dry run aponta para este estilo e destino, a voz e modelo esperados e exatamente os cinco blocos. Só então executar o mesmo comando sem `-DryRun`, sob responsabilidade do executor designado. Não usar `-Todos`, não chamar o Python global e não copiar estilo para o texto falado.

O gerador grava cada WAV a partir do nome do texto: por exemplo, `L03_B01_P01-P03_narracao.wav`. Uma falha no meio da lista pode deixar blocos anteriores válidos no destino; inspecioná-los antes de retomar e passar apenas os pendentes. O gerador substitui um WAV homônimo existente, por isso dirigir correções para uma nova pasta (`bruto_v2`, por exemplo) e selecionar somente os blocos afetados. Nunca sobrescrever uma entrega aprovada.

## Validação e montagem do áudio

1. Validar cada WAV: conclusão do processo, cabeçalho, duração, codec, taxa de amostragem, canais, pico e silêncios. Registrar o formato observado.
2. Transcrever localmente e comparar com os parágrafos limpos correspondentes; não comparar com tags nem com este documento. Investigar omissões, duplicações, fala da tag e divergências materiais. Escutar os pontos sinalizados e os nomes próprios; ASR não comprova pronúncia correta.
3. Conferir especialmente os dois anos no bloco 2, pergunta/resposta no bloco 3, frigobar e pergunta/resposta no bloco 4 e a pergunta final no bloco 5. Medir ppm por bloco para detectar lentidão ou aceleração; a faixa é direção, não motivo isolado para regeneração quando a fala soar natural.
4. Se houver erro material, corrigir somente a versão Gemini do bloco afetado, preservando todas as palavras, e regenerar somente esse bloco, no máximo duas novas tentativas antes de devolver o bloqueio ao coordenador. Uma preferência pequena de interpretação não justifica repetir todos os blocos.
5. Concatenar blocos aprovados na ordem, preservando o início e fim de cada palavra. Nas quatro junções, remover apenas silêncio excedente confirmado e manter uma pausa natural de transição; não inserir sobreposição de fala. Registrar offsets reais dos blocos para alinhamento posterior. Escutar as junções e a estabilidade de voz/volume.
6. Preservar os WAVs brutos e a concatenação bruta. Normalizar uma cópia da narração integral com `automacao/producao.py normalize`, padrão do projeto de -16 LUFS e pico verdadeiro de -1,5 dB. Medir novamente após normalização. A aplicação uniforme ao conjunto ajuda a manter continuidade entre blocos.
7. Entregar ao coordenador a narração integral validada, WAVs por bloco, transcrição, medições, offsets e pontos efetivamente escutados. Legendas partem do roteiro limpo, sem tags. O coordenador é o único escritor de `producao.json`.

## Integridade da preparação

A verificação local passou: removendo somente `<short pause>` e normalizando espaços, a versão integral e a concatenação dos cinco blocos são idênticas ao original, com comparação sensível a maiúsculas e pontuação. Foram confirmadas 894 palavras, 19 parágrafos e cinco tags. Os hashes da fonte e da direção editorial permaneceram iguais antes e depois da escrita dos derivados:

- `01_NARRACAO.txt`, SHA-256: `47AD0A356C31DB478580D3B25A74A298AC23E0789EC8514EB5C12F92ED5407AF`.
- `02_DIRECAO_E_FONTES.md`, SHA-256: `96AC4D63DB310C2F21F765CD06605963EFE05AD2F30B049D8DD32BCB03CCF875`.

Dry run e validação de áudio ficam com o executor após a extensão do wrapper. A direção de voz ainda não é evidência de resultado sonoro.
