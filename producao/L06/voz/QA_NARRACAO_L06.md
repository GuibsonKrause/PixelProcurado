# L06 — validação da voz

A geração integral usou Gemini 3.8 Flash TTS com a voz `voice_iagtq1gnk2br`, o texto `03_NARRACAO_GEMINI.txt` e o Style aprovado. A API devolveu WAV PCM de 16 bits, 24 kHz, mono, com duração de 306,960 s e nenhum sample clipado. O original está em `03_NARRACAO_narracao.wav`.

A transcrição local do original sinalizou dicção irregular nos parágrafos 13, 18, 19 e 21. Foram geradas retomadas apenas desses trechos, com orientação de pronúncia no campo Style e as mesmas falas. No parágrafo 21, a primeira frase da locução original preserva “As seis regiões” e a retomada entra em “Nas Keys”. A primeira tentativa desse parágrafo foi descartada após o ASR ler “três”. O relatório `revisao_retomadas.json` traz os textos reconhecidos e as fronteiras no original.

O WAV de edição tem 310,820 s, PCM de 16 bits, 48 kHz e um canal. A normalização mediu −16,84 LUFS e −1,48 dBTP, sem clipping. O alinhamento usa a locução revisada e os 22 parágrafos do roteiro limpo, com nomes próprios escritos conforme as fontes oficiais. A revisão de alinhamento preserva divergências para auditoria. 

A avaliação foi instrumental. ASR e medições identificam as regiões da fala e ajudam a encontrar divergências. Em particular, a leitura de “pântano”, “Keys” e “Grassrivers” no começo ainda variou entre a locução e o reconhecimento automático. A correspondência de nomes na segunda metade melhorou após as retomadas. O ambiente de execução não permitiu escuta subjetiva integral.
