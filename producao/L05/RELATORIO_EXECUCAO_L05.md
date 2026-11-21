# L05 — relatório do executor

PASS técnico e inspeção visual amostrada concluídos em03/11/2026. Revisão editorial independente cabe ao coordenador/Astra e não está sendo alegada por este relatório.

Entregas: exportacoes/Pixel_Procurado_L05_4K.mp4 eSRT; publicacao/capa_youtube.jpg1280×720(431939bytes), capa_master.png1920×1080, arte-base/prompt; textos01–06 eguia00; projeto/edicao_l05.json editável. Roteiros canônicos01/03 eStyle04 preservados.

Vídeo:3840×2160,H.264,30fps,9746frames,324.866667s. Áudio:AAC48kHz,324.84s. MP4:92305283bytes.47planos/132legendas, sem intervalos inválidos ou sobreposição; exposição mínima0.850s. Voz cobre o áudio integral e a imagem cobre seu último sample com tolerância menor que1frame. Gancho inicial de6palavras termina2.08s, com evidência na tela desde0.

Decodificação integral do MP4 sem erros. Mux sem avisos temporais pendentes. QA em projeto/render4k/qa/validacao_final.json e decodificacao_integral.txt. Correlação com WAV normalizado em1/32/81/162/244/292/320s: mínimo0.999968076; duração decodificada confere, sem truncamento/deslocamento detectado.

Medição AAC final:-16.92LUFS,-1.23dBTP,LRA2.90. O AAC excede o alvo inicial-1.5dBTP em0.27dB; não se afirma que o exportado manteve-1.5dBTP. A cópiaWAV normalizada mede-16.91LUFS/-1.47dBTP, sem amostras clipadas. OriginalGeminiPCM16/24kHzmono preservado. ASR integral small/int8/beam1 e segunda conferência local pontual. Divergências fonéticas estão documentadas em EDICAO_L05.md e arquivosvoz; sem omissão extensa ou tag falada detectada. Não foi feita escuta subjetiva integral.

Amostra5planos aprovada antes do integral, com entrada/contornos/hold/fonteV/cartela. Após reduzir arredondamento do zoom de16px para2px, abertura refeita e amostra revalidada. Os caches estáticos foram conservados somente após comparação de assinaturas antigas/entradas e prova de dimensões idênticas, em projeto/render4k/cache_upgrade_static_zoom.json. Não foi alterado browser alheio; browserRemotion próprio fechado ao concluir o lote.

Inspeção final real do MP4: duas pranchas contato_final_real_1/2.jpg,com frames/tempos em amostras_mp4_real.json. Foram vistos diretamente16quadros do arquivo final, além dos estados da amostra. Fontes exatas,ciclista/praia,Cheetah/rua,jato/orla,títulos,contornos,legendas e encerramento coerentes nas amostras; sem rosto coberto ou elemento indicado incorretamente. Inspeção visual amostrada não é revisão integral.

Limites: fontesV640×360 ampliadas em painel identificado; VI3840×2160 reduzidas para o painel. Composição final4K não implica detalhe4Knativo em todas as fontes. Fotografias inteiras com movimentos2D/contornosRemotion; sem parallax. Não foram usados clipes genéricos para substituir as seis evidências. Thumbnail: montagem editorialIA, não screenshot, informada no prompt e descrição.

SHA256 MP4:b286b951c08767d4266dd398b5872c5ac35b6b64b95a17adf1f7a82fb92a0665
SHA256 SRT:4ddf76af1ed7434376c7f770a359d3f869f853ebb0e49b56dfff0b0a7e1725c0
SHA256 capaJPG:4a49eb28fda4e2462aa5fd4a9766613806c6d4ca0c4ff1a4a7e74ada88986185
Manifesto:exportacoes/SHA256SUMS.json; entradas:projeto/hashes_entradas.json.

Não houve upload/agendamento/Postiz nem alteração de conta por este executor. Não foi escrito producao.json, de ownership do coordenador. Fontes oficiais e regras de publicação foram consultadas em03/11/2026; detalhes/limites em FONTES_VERIFICADAS.md eguia. Final estável, pronto para revisão independente e derivações autorizadas.

Quadros finais inspecionados: 0.400s/f12, 7.000s/f210, 34.000s/f1020, 70.000s/f2100, 81.000s/f2430, 98.000s/f2940, 133.000s/f3990, 160.000s/f4800, 174.000s/f5220, 205.000s/f6150, 219.000s/f6570, 235.000s/f7050, 250.000s/f7500, 279.000s/f8370, 297.000s/f8910, 320.000s/f9600.
