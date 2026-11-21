"""Episode-specific revised cuts. Only C04-C08 outputs; shared modules are read-only."""
import sys,json,hashlib,shutil,wave,subprocess
from pathlib import Path
import shorts_vertical as edit
import producao
from shorts_editorial import shot,graph,vid,OLD,D,V,K,C,ART,CHEETAH,T1,T2,TL,ROOT

edit.PLANS['C04']=[
 shot(None,OLD,'SUA NOSTALGIA\nTEM TRUQUE.','VICE CITY • CLÁSSICO',hook=True),
 graph('Vice City saiu','TRÊS ÉPOCAS',['2002 • LANÇAMENTO','1986 • HISTÓRIA','SUA VIDA • QUANDO JOGOU'],'VICE CITY • NOSTALGIA'),
 shot('Você pode lembrar',OLD,'RÁDIO. PALMEIRAS. TOMMY.','VICE CITY • MATERIAL DO CLÁSSICO'),
 graph('Ou daquela tarde','A SUA TARDE TAMBÉM CONTA',['DIRIGIR SEM RUMO','TEMPO SEM OBRIGAÇÃO'],'MEMÓRIA PESSOAL • EXEMPLO'),
 graph('Hoje, às vezes','A LIBERDADE MUDOU',['QUAL COMPROMISSO VAI ATRASAR?'],'COMPARAÇÃO BEM-HUMORADA'),
 graph('Por isso, pedir','SEPARE AS LEMBRANÇAS',['A CIDADE','A FASE DA SUA VIDA'],'LEITURA DO CANAL'),
 vid('A Rockstar pode',T2,35.1,'RECONSTRUIR UMA AVENIDA.','GTA VI • CIDADE NO TRAILER',motion=2.4),
 graph('Restaurar sua tarde','E CANCELAR TRÊS REUNIÕES?',['A TARDE LIVRE NÃO VEM NO MAPA'],'COMPARAÇÃO BEM-HUMORADA'),
 vid('Nas imagens',T1,51,'O ESPETÁCULO GANHOU TELAS.','GTA VI • REDES NO TRAILER',motion=3),
 shot('As Real Dimez',D(2),'A PLATEIA TAMBÉM FILMA.','REAL DIMEZ • SCREENSHOT'),
 shot('A vontade de aparecer',D(2),'QUEM ASSISTE TAMBÉM ESPALHA.','DETALHE DO MESMO QUADRO',crop=[0,.1,.5,.9]),
 vid('Todo mundo quer',T1,51,'GUARDAR. POSTAR. ESPALHAR.','GTA VI • APRESENTAÇÃO DAS REDES',motion=3),
 vid('A cidade mudou',T1,31,'A CIDADE MUDOU. NÓS TAMBÉM.','GTA VI • CULTURA DE RUA',motion=3.3),
 vid('Dá pra reconhecer',T1,38,'CORES E AMBIÇÃO.','GTA VI • IDENTIDADE VISUAL',motion=3.1),
 shot('Talvez o mais',OLD,'FAMILIAR. E DIFERENTE.','VICE CITY • MEMÓRIA E RETORNO'),
 graph('Até a nostalgia','NEM TUDO FOI NA MESMA DATA.',['1986','2002','A SUA LEMBRANÇA'],'LEITURA DO CANAL'),
 shot('Afinal',OLD,'SUA NOSTALGIA\nTEM TRUQUE.','VICE CITY • CLÁSSICO',hook=True)]

edit.PLANS['C05']=[
 vid(None,T2,35.1,'GAMEPLAY.\nMAS QUAL CENA?','GTA VI • TRAILER 2',hook=True,motion=2.7),
 graph('A Rockstar descreve','O CONJUNTO É UMA MISTURA',['METADE GAMEPLAY','METADE CINEMATOGRÁFICAS'],'DECLARAÇÃO OFICIAL • TRAILER 2'),
 vid('Isso confirma',T2,75,'O TRAILER NÃO ROTULA CADA PLANO.','GTA VI • TRAILER 2',motion=3.5),
 vid('Uma câmera atrás',T2,42.3,'A CÂMERA É UMA PISTA.','GTA VI • TRAILER 2',motion=1.5),
 vid('Só que uma sequência',T2,45,'O ÂNGULO PODE SER ENCENADO.','GTA VI • EXEMPLO DE ENQUADRAMENTO',motion=4.4),
 graph('A posição da câmera','PISTA ≠ CONTROLE DEMONSTRADO',['ENQUADRAMENTO','DECISÃO DO JOGADOR?'],'CRITÉRIO DE ANÁLISE'),
 graph('Anúncio de apartamento','O ÂNGULO TAMBÉM VENDE',['NA FOTO: CABE UMA FESTA','NA VISITA: CADÊ O ESPAÇO?'],'COMPARAÇÃO HIPOTÉTICA'),
 graph('Você visita','LICENÇA PARA ABRIR A GELADEIRA',['O ENQUADRAMENTO SUGERE MAIS'],'COMPARAÇÃO HIPOTÉTICA'),
 graph('Imagina uma cena','AÇÃO MOSTRADA',['ABRIR A PORTA','CARRO SAIR'],'EXEMPLO HIPOTÉTICO • NÃO É CENA CONFIRMADA'),
 graph('Ver a porta','DECISÃO DISPONÍVEL?',['QUANDO ENTRAR?','PARA ONDE IR?'],'EXEMPLO HIPOTÉTICO'),
 graph('Esse exemplo','VER AÇÃO ≠ PODER ESCOLHER',['AÇÃO MOSTRADA','DECISÃO DO JOGADOR'],'EXEMPLO HIPOTÉTICO'),
 graph('A declaração oficial','A RESPOSTA GERAL EXISTE',['HÁ GAMEPLAY NO CONJUNTO'],'DECLARAÇÃO OFICIAL'),
 vid('Pra classificar',T2,140,'CADA CENA PEDE SUA INFORMAÇÃO.','GTA VI • TRAILER 2',motion=3.8),
 vid('Não dá pra distribuir',T2,35,'FAMILIAR NÃO É PROVA.','GTA VI • TRAILER 2',motion=3.5),
 vid('nem chamar tudo',T2,83,'BONITO NÃO É DIAGNÓSTICO.','GTA VI • TRAILER 2',motion=3.2),
 graph('Empolgação é permitida','EMPOLGAÇÃO COM CRITÉRIO',['NÃO INVENTAR A LEGENDA'],'LEITURA DO CANAL'),
 graph('A resposta geral','DUAS PERGUNTAS',['HÁ GAMEPLAY?','QUAL CENA É CONTROLÁVEL?'],'CRITÉRIO DE ANÁLISE'),
 vid('Então',T2,35.1,'GAMEPLAY.\nMAS QUAL CENA?','GTA VI • TRAILER 2',hook=True,motion=2.7)]

edit.PLANS['C06']=[
 shot(None,ART,'GRÁFICOS\nNO PÔSTER?','GTA VI • ARTWORK OFICIAL',hook=True),
 shot('Uma imagem oficial',ART,'OFICIAL PODE SER DESENHO.','GTA VI • ARTWORK'),
 shot('Parece óbvio',ART,'ZOOM NO ARQUIVO ERRADO.','RECORTE DA ILUSTRAÇÃO',crop=[.25,.15,.42,.55]),
 graph('Daqui a pouco','DESEMPENHO PELA MOLDURA?',['O MATERIAL NÃO RESPONDE A ISSO'],'COMPARAÇÃO BEM-HUMORADA'),
 shot('Olha a arte',ART,'JASON + LUCIA. CÉU ROSA.','ARTWORK • NÃO É CAPTURA'),
 shot('Ela tem traço',ART,'TRAÇO. CORES. COMPOSIÇÃO.','ESCOLHAS DA ILUSTRAÇÃO'),
 graph('A própria biblioteca','DUAS CATEGORIAS',['ARTWORK & WALLPAPERS','SCREENSHOTS'],'BIBLIOTECA OFICIAL'),
 shot('Uma captura permite',C(1),'UM QUADRO DO JOGO.','SCREENSHOT • CATEGORIA OFICIAL'),
 shot('A ilustração mostra',ART,'ESCOLHAS DO ARTISTA.','ARTWORK • CATEGORIA OFICIAL'),
 graph('As duas são oficiais','OFICIAIS. PERGUNTAS DIFERENTES.',['ARTE → REPRESENTAÇÃO','CAPTURA → QUADRO DIVULGADO'],'CRITÉRIO DE ANÁLISE'),
 graph('Usar o desenho','PLANTA ≠ VENTILAÇÃO',['SETA AZUL NO DESENHO','VENTO REAL?'],'COMPARAÇÃO HIPOTÉTICA'),
 graph('Tem uma seta','DEVE ENTRAR UM VENTO…',['A SETA NÃO É UMA MEDIÇÃO'],'COMPARAÇÃO BEM-HUMORADA'),
 shot('E uma captura',C(1),'UMA CAPTURA É UM INSTANTE.','SCREENSHOT • LIMITE DA EVIDÊNCIA'),
 vid('Sozinha, ela',T2,35.1,'MOVIMENTO PEDE OUTRO MATERIAL.','GTA VI • VÍDEO, NÃO TESTE DE CONTROLE',motion=2.7),
 graph('Pra essas perguntas','A PROVA PRECISA CORRESPONDER',['MOVIMENTO','RESPOSTA AO CONTROLE'],'CRITÉRIO DE ANÁLISE'),
 shot('Antes de discutir',ART,'PRIMEIRO: ORIGEM E CATEGORIA.','ARTWORK • CONFIRA A BIBLIOTECA'),
 graph('Esse passo','EVITE A DISCUSSÃO ERRADA',['CONFIRA O TIPO DE ARQUIVO'],'LEITURA DO CANAL'),
 shot('Afinal',ART,'GRÁFICOS\nNO PÔSTER?','GTA VI • ARTWORK OFICIAL',hook=True)]

edit.PLANS['C07']=[
 shot(None,V(9),'O DETALHE ESTÁ\nFORA DO CARRO.','GTA VI • OLHE AO REDOR',hook=True),
 shot('Na imagem de GTA',V(9),'MOTO. GENTE. PILARES PINTADOS.','SCREENSHOT • QUADRO INTEIRO'),
 shot('O cenário quase',V(9),'O BAIRRO ENTRA NA CONVERSA.','DETALHE DA MESMA IMAGEM',crop=[0,0,.52,1]),
 shot('Compare com',CHEETAH,'AGORA: CHEETAH EM GTA V.','GTA V • DIVULGAÇÃO DE 2012'),
 shot('A traseira ocupa',CHEETAH,'A TRASEIRA DOMINA O QUADRO.','GTA V • MESMA FOTO PROMOCIONAL'),
 shot('Aerofólio',CHEETAH,'A ESTRELA É O CARRO.','GTA V • MESMA FOTO PROMOCIONAL'),
 shot('Na cena de Vice City',V(9),'CARRO + GENTE + RUA.','GTA VI • SCREENSHOT'),
 shot('O lugar ajuda',V(9),'VONTADE DE ESTAR ALI.','GTA VI • DETALHE DO BAIRRO',crop=[.48,0,.52,1]),
 graph('Recortar só','CADÊ OS CONVIDADOS?',['FOTO DO CHURRASCO','SÓ A CHURRASQUEIRA'],'COMPARAÇÃO HIPOTÉTICA'),
 graph('Você até entende','O EQUIPAMENTO NÃO É O EVENTO',['O RECORTE PERDE CONTEXTO'],'COMPARAÇÃO HIPOTÉTICA'),
 graph('Isso não prova','COMPOSIÇÃO ≠ BENCHMARK',['NÃO MEDE DENSIDADE GERAL','NÃO COMPARA DESEMPENHO'],'LIMITES DA EVIDÊNCIA'),
 shot('São imagens promocionais',CHEETAH,'DOIS ENQUADRAMENTOS.','GTA V • DIVULGAÇÃO HISTÓRICA'),
 shot('A comparação aqui',V(9),'O QUE CADA FOTO DESTACA.','GTA VI • SCREENSHOT'),
 shot('Uma concentra',CHEETAH,'O OLHAR NO CARRO.','GTA V • DIVULGAÇÃO DE 2012'),
 shot('A outra abre',V(9),'CARRO, PESSOAS E BAIRRO.','GTA VI • QUADRO INTEIRO'),
 shot('Volta à imagem',V(9),'ACOMPANHE AS BORDAS.','GTA VI • ANÁLISE DA MESMA IMAGEM'),
 shot('Porque',V(9),'O DETALHE ESTÁ\nFORA DO CARRO.','GTA VI • OLHE AO REDOR',hook=True)]

edit.PLANS['C08']=[
 shot(None,K(2),'A IGUANA\nVIROU SÍNDICA.','LEONIDA KEYS • SCREENSHOT',hook=True,crop=[.05,.65,.38,.35]),
 shot('Pelo menos',K(2),'A DONA DA RUA.','LEONIDA KEYS • SCREENSHOT',ring=[.07,.71,.31,.18]),
 shot('ela está no asfalto',K(2),'NO ASFALTO. SEM PRESSA.','DETALHE DA MESMA IMAGEM',crop=[.05,.65,.38,.35]),
 shot('A gente chega',K(2),'ADMINISTRAÇÃO LOCAL.','LEONIDA KEYS • QUADRO INTEIRO'),
 graph('Falta só pedir','QUAL O NÚMERO DA RESERVA?',['O HORÁRIO DE VISITA ACABOU'],'PIADA • SITUAÇÃO IMAGINADA'),
 shot('O detalhe funciona',K(2),'UM DETALHE. UMA SITUAÇÃO.','ANÁLISE VISUAL'),
 shot('Você não vê',K(2),'A RUA GANHA PERSONAGEM.','LEONIDA KEYS • MESMA IMAGEM'),
 shot('Encontra um animal',K(2),'NO CAMINHO DAS PESSOAS.','DETALHE DO MESMO QUADRO',ring=[.07,.71,.31,.18]),
 graph('Agora imagina','IMAGINE O MESMO QUADRO',['RUA E PESSOAS','SEM A IGUANA'],'EXERCÍCIO NOSSO • NÃO É OUTRA CAPTURA'),
 graph('É um exercício','EXERCÍCIO, NÃO NOVA CAPTURA',['AUSÊNCIA IMAGINADA'],'HIPÓTESE EDITORIAL'),
 shot('A rua continuaria',K(2),'O PERSONAGEM MUDA O OLHAR.','RETORNO À IMAGEM ORIGINAL'),
 graph('Isso não confirma','A FOTO NÃO CONFIRMA',['BLOQUEIO DE CARROS','REAÇÃO AO JOGADOR','PARTICIPAÇÃO EM MISSÃO'],'LIMITES DA EVIDÊNCIA'),
 shot('A foto mostra',K(2),'PRESENÇA CONFIRMADA.','LEONIDA KEYS • SCREENSHOT',ring=[.07,.71,.31,.18]),
 graph('O comportamento','COMPORTAMENTO PEDE OUTRA PROVA',['PRESENÇA ≠ MECÂNICA'],'CRITÉRIO DE ANÁLISE'),
 shot('por mais convincente',K(2),'POSE DE PROPRIETÁRIO.','DETALHE DA MESMA IMAGEM',crop=[.05,.65,.38,.35]),
 shot('A graça está',K(2),'PEQUENA PARTICIPAÇÃO. GRANDE EFEITO.','ANÁLISE VISUAL'),
 vid('Entre tanta água',T2,83,'ÁGUA. HORIZONTE. KEYS.','GTA VI • PAISAGEM NO TRAILER 2',motion=2),
 shot('foi o sujeito',K(2),'QUEM COMANDA O QUADRO?','LEONIDA KEYS • QUADRO INTEIRO',ring=[.07,.71,.31,.18]),
 shot('Afinal',K(2),'A IGUANA\nVIROU SÍNDICA.','LEONIDA KEYS • SCREENSHOT',hook=True,crop=[.05,.65,.38,.35])]

def audio(rid):
 print('AUDIO START',rid,flush=True)
 p=edit.BASE/rid
 for name in ['voz','projeto','exportacoes','publicacao']:(p/name).mkdir(exist_ok=True)
 raw=p/f'voz/bruto/{rid}_narracao.wav'; normalized=p/'voz/narracao.wav'
 assert raw.is_file(),raw
 if not normalized.exists():producao.normalize(raw,normalized)
 words=p/'voz/palavras_asr.json'
 if not words.exists():
  from faster_whisper import WhisperModel
  import numpy as np
  temp=p/'voz/asr_16k.f32'
  edit.run(['-i',normalized,'-ar','16000','-ac','1','-f','f32le',temp],p/'voz/asr_decode.log')
  model=WhisperModel('small',device='cpu',compute_type='int8',cpu_threads=2,download_root=str(ROOT/'.course-tools/models'),local_files_only=True)
  segments,_=model.transcribe(np.fromfile(temp,dtype=np.float32),language='pt',beam_size=1,best_of=1,vad_filter=True,word_timestamps=True,initial_prompt='GTA seis. Jason. Lucia. Leonida Keys. Vice City. Rockstar. Real Dimez. Cheetah.')
  result=[]
  for seg in segments:
   result.extend(dict(word=w.word.strip(),start=round(w.start,3),end=round(w.end,3),probability=round(w.probability,4)) for w in seg.words or [])
   print(rid,'ASR',round(seg.end,2),seg.text.strip(),flush=True)
  assert result
  edit.write_json(words,result);temp.unlink()
 with wave.open(str(raw)) as w: info=dict(duration=w.getnframes()/w.getframerate(),rate=w.getframerate(),channels=w.getnchannels(),width=w.getsampwidth())
 log=producao.run(['-i',raw,'-af','silencedetect=noise=-40dB:d=0.8,volumedetect','-f','null','-'])
 (p/'voz/medicoes_bruto.txt').write_text(log,encoding='utf8')
 edit.write_json(p/'voz/validacao_bruto.json',dict(**info,model='gemini-3.8-flash-tts',voice='voice_iagtq1gnk2br',source_sha256=hashlib.sha256((ROOT/f'producao/cortes/{rid}_GEMINI.txt').read_bytes()).hexdigest(),wav_sha256=hashlib.sha256(raw.read_bytes()).hexdigest()))
 print('AUDIO READY',rid,info,flush=True)

def publication(rid):
 import shorts_publicacao as pub
 p=edit.BASE/rid;pub.make(rid)
 readme=p/'00_LEIA_ME.md';saved=p/'historico/2026-10-31_pre_revisao/00_LEIA_ME.md'
 if readme.exists() and not saved.exists():shutil.copy2(readme,saved)
 readme.write_text(f'''# {rid} — produção revisada em 31/10/2026

Nova narração gerada a partir do roteiro canônico revisado, com legendas e montagem sincronizadas. Os avisos editoriais de 29/10 referem-se à versão anterior, preservada no histórico.

- [Vídeo vertical 1080×1920](exportacoes/Pixel_Procurado_{rid}_Short_1080x1920.mp4)
- [Legendas SRT](exportacoes/{rid}_legendas.srt)
- [Capa pronta](publicacao/capa_youtube.jpg)
- [Guia e textos de publicação](publicacao/00_GUIA_DE_PUBLICACAO.md)
- [Direção e tempos](projeto/DIRECAO.md)
- [Validação técnica](projeto/qa/validacao_final.json)
- [Relatório e limites](RELATORIO_REVISAO_2026-10-31.md)

Não houve upload, agendamento ou publicação.
''',encoding='utf8')
 old=p/'historico/2026-10-31_pre_revisao/publicacao'
 # Reuse inspected coherent commissioned illustration; retain exact provenance.
 for n in ['thumbnail_base_gerada.png','PROMPT_THUMBNAIL.txt','capa_master.png','capa_youtube.jpg']:
  if (old/n).exists():shutil.copy2(old/n,p/'publicacao'/n)
 guide=p/'publicacao/00_GUIA_DE_PUBLICACAO.md'
 text=guide.read_text(encoding='utf8').replace('Preparado em 27/10/2026.','Atualizado em 31/10/2026.')
 a=text.index('4. Envie capa_youtube.jpg');b=text.index('5. Aguarde processamento',a)
 text=text[:a]+'4. A ajuda oficial consultada em 31/10/2026 informa miniatura personalizada de Shorts pelo Studio no computador para contas verificadas. Use capa_youtube.jpg se o campo estiver disponível; caso contrário, use a seleção de quadro oferecida pela conta. [Ajuda oficial](https://support.google.com/youtube/answer/72431?hl=pt-BR).\n'+text[b:]
 text=text.replace('Pixel Procurado — Shorts de GTA |','Pixel Procurado — Shorts de GTA (sugestão, se existir) |')
 guide.write_text(text,encoding='utf8')
 (p/'publicacao/08_REGRAS_CONSULTADAS.md').write_text('''# Referências oficiais consultadas em 31/10/2026

- Miniaturas e Shorts: https://support.google.com/youtube/answer/72431?hl=pt-BR — a página informa upload pelo Studio no computador, conta verificada.
- Capítulos: https://support.google.com/youtube/answer/9884579?hl=pt-BR — primeiro 00:00, três marcações crescentes e dez segundos por capítulo; aqui são apenas marcadores opcionais fora da descrição principal.
- Tags: https://support.google.com/youtube/answer/146402?hl=pt-BR — contribuição limitada, especialmente úteis para grafias alternativas.
- Tela final: https://support.google.com/youtube/answer/6388789?hl=pt-BR — últimos 5–20 segundos, vídeo de ao menos 25 segundos; a edição preserva o loop e não inclui tela final gráfica.
- IA: https://support.google.com/youtube/answer/14328491?hl=pt-BR — avaliar representação realista e origem efetiva da voz. Origem pessoal da voz personalizada não confirmada.

Reconsulta editorial do Trailer 2: página oficial acessível em https://www.rockstargames.com/VI/trailer-2. O extrator público do YouTube não apresentou a descrição e X retornou 403; a declaração de mistura gameplay/cinemática é sustentada pela apuração documental anterior preservada no histórico, sem alegar nova verificação do texto completo.
''',encoding='utf8')
 credits=p/'publicacao/07_CREDITOS_E_MIDIAS.md'
 text=credits.read_text(encoding='utf8').replace('Apuração reconfirmada em 27/10/2026:','Apuração documental anterior em 27/10/2026:')
 credits.write_text(text,encoding='utf8')
 files=[p/'exportacoes'/f'Pixel_Procurado_{rid}_Short_1080x1920.mp4',p/'exportacoes'/f'{rid}_legendas.srt',p/'voz/narracao.wav',p/'publicacao/capa_youtube.jpg',p/'projeto/timeline.json']
 data=json.loads((p/'projeto/timeline.json').read_text(encoding='utf8'))
 edit.write_json(p/'projeto/qa/hashes.json',{f.relative_to(ROOT).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files})
 video_seconds=sum(s['frames']/30 for s in data['shots'] if s['file'].endswith('.mp4'))
 real_motion=sum(min(s['frames']/30,s.get('motion',s['frames']/30)) for s in data['shots'] if s['file'].endswith('.mp4'))
 edit.write_json(p/'projeto/qa/composicao_midia.json',dict(duration=data['duration'],video_source_seconds=video_seconds,real_video_motion_seconds=real_motion,real_video_motion_ratio=real_motion/data['duration'],still_and_graphics_seconds=data['duration']-real_motion))
 if rid=='C05':shutil.copy2(p/'historico/2026-10-31_pre_revisao/projeto/fonte_descricao_trailer2.txt',p/'projeto/fonte_descricao_trailer2.txt')
 (p/'RELATORIO_REVISAO_2026-10-31.md').write_text(f'''# {rid} — produção revisada

Roteiro canônico preservado; narração nova Gemini 3.8 Flash TTS / voz voice_iagtq1gnk2br. Áudio bruto e normalizado separados; alinhamento Whisper small local int8 (beam5 C04; beam1 C05–C08 após passagem beam5 lenta interrompida em C05, sem repetir TTS). Duração {data['duration']:.3f}s, 1080×1920, 30fps. {len(data['shots'])} planos; {len(data['captions'])} legendas. Planos derivados de vídeo: {video_seconds:.2f}s; movimento real do vídeo: {real_motion:.2f}s ({real_motion/data['duration']:.1%}), restante em quadros sustentados. A seleção de fotos foi mantida onde a fala analisa exatamente uma imagem. C07 compara duas fotografias específicas e não recebe clipe genérico como substituição.

Timeline: projeto/timeline.json e DIRECAO.md. Gráficos Remotion em sequência de quadros transparentes, composição e movimentos FFmpeg, codificação H.264 QSV e AAC 48kHz. Áudio dos clipes removido. Capa editorial anterior reaproveitada após inspeção; não é screenshot novo.

QA técnica: projeto/qa/validacao_final.json; decodificação integral e correlações de áudio em cinco posições. Evidências visuais amostradas em projeto/qa/contato.jpg. Hashes em projeto/qa/hashes.json. Diferenças ASR em projeto/revisao_alinhamento.json. Análise automática e amostragem visual não equivalem a escuta humana integral nem comprovam pronúncia perfeita. Algumas fontes horizontais são reduzidas ao painel vertical; mantêm o quadro para leitura analítica. Sem parallax 3D.

Versão anterior preservada em historico/2026-10-31_pre_revisao. Nenhum upload, agendamento ou publicação.
''',encoding='utf8')

if __name__=='__main__':
 action=sys.argv[1]
 for rid in sys.argv[2:] or [f'C{i:02}' for i in range(4,9)]:
  if action=='audio':audio(rid)
  elif action=='prepare':
   edit.prepare(rid)
   if rid=='C07':
    p=edit.BASE/rid;data=json.loads((p/'projeto/timeline.json').read_text(encoding='utf8'));fixes=[]
    for c in data['captions']:
     previous=c['text'];c['text']=c['text'].replace('A Aerofólio','Aerofólio').replace('comparar a desempenho','comparar desempenho')
     if previous!=c['text']:fixes.append(dict(start=c['start'],asr_caption=previous,caption=c['text'],reason='Remoção de artigo espúrio do reconhecimento; roteiro canônico e concordância preservados, áudio inalterado'))
    edit.write_json(p/'projeto/timeline.json',data);edit.write_json(p/'projeto/correcoes_legendas_editoriais.json',fixes)
    (p/'exportacoes'/f'{rid}_legendas.srt').write_text('\n\n'.join(f"{i+1}\n{edit.stamp(c['start'])} --> {edit.stamp(c['end'])}\n{c['text']}" for i,c in enumerate(data['captions']))+'\n',encoding='utf8')
  elif action=='sample':edit.render(rid,{0,1,5,10})
  elif action=='samplesheet':
   from PIL import Image,ImageDraw
   p=edit.BASE/rid/'projeto';out=Image.new('RGB',(1080,520));draw=ImageDraw.Draw(out)
   for j,i in enumerate([0,1,5,10]):
    frame=p/f'sample_{i:03}.jpg';edit.run(['-ss',.8,'-i',p/f'render/{i:03}.mp4','-frames:v',1,'-vf','scale=270:480',frame],p/f'sample_{i:03}.log')
    out.paste(Image.open(frame),(j*270,0));draw.text((j*270+5,490),f'{rid} shot {i}',fill='white')
   out.save(p/'amostra_antes_integral.jpg')
  elif action=='render':edit.render(rid)
  elif action=='qa':
   edit.qa(rid)
   p=edit.BASE/rid;data=json.loads((p/'projeto/timeline.json').read_text(encoding='utf8'))
   assert (p/'voz/NARRACAO.txt').read_text(encoding='utf8')==(ROOT/f'producao/cortes/{rid}_NARRACAO.txt').read_text(encoding='utf8')
   assert all(a['end']<=b['start'] for a,b in zip(data['captions'],data['captions'][1:]))
   assert all(a['from']+a['frames']==b['from'] for a,b in zip(data['shots'],data['shots'][1:]))
   edit.write_json(p/'projeto/qa/continuidade_legendas.json',dict(canonical_script_identical=True,shot_gaps=0,caption_overlaps=0,caption_count=len(data['captions']),minimum_caption_seconds=min(c['end']-c['start'] for c in data['captions']),captions_under_085_seconds=[c for c in data['captions'] if c['end']-c['start']<.85],source_hashes={file:hashlib.sha256((ROOT/file).read_bytes()).hexdigest() for file in {s['file'] for s in data['shots'] if s['file']}}))
  elif action=='publication':publication(rid)
  else:raise ValueError(action)
