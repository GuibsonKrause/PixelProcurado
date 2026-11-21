"""C09–C12: canonical revised scripts, word-aligned contextual edits. No upload."""
import sys, json, shutil, hashlib, wave, re
from pathlib import Path
import shorts_vertical as edit
import producao
from shorts_editorial import shot, graph, vid, K, G, R, B, J, T1, T2, TV, META, ROOT

IDS=['C09','C10','C11','C12']
edit.PLANS['C09']=[
 shot(None,K(1),'MESMA ÁGUA.\nOUTRA DESCONFIANÇA.','DUAS PAISAGENS • GTA VI',hook=True),
 shot('Nas Keys o mar',K(1),'HORIZONTE ABERTO.','KEYS • IMAGEM ANALISADA'),
 shot('Em Grassrivers o barco',G(3),'O CAMINHO SE FECHA.','GRASSRIVERS • IMAGEM ANALISADA'),
 vid('Num lugar',T2,6.2,'ONDE PARAR PRA OLHAR?','KEYS • TRECHO DO TRAILER 2',motion=1.6),
 shot('No outro',G(3),'O QUE A VEGETAÇÃO ESCONDE?','GRASSRIVERS • IMAGEM ANALISADA'),
 shot('A viagem continua',G(3),'DE BARCO. COM MENOS CONFIANÇA.','GRASSRIVERS • IMAGEM ANALISADA'),
 shot('É a sensação',K(1),'É UMA LEITURA VISUAL.','ANÁLISE DOS ENQUADRAMENTOS'),
 shot('A foto das Keys',K(1),'ESPAÇO + HORIZONTE.','KEYS • IMAGEM ANALISADA'),
 shot('A de Grassrivers',G(3),'PARTES DO CAMINHO OCULTAS.','GRASSRIVERS • IMAGEM ANALISADA'),
 vid('A abertura do cenário',T1,36,'O CENÁRIO MUDA A EXPECTATIVA.','TRAILER 1 • PAISAGEM',motion=1.5),
 graph('Parece a diferença','DUAS CASAS DE FÉRIAS',['UMA VARANDA','UMA LANTERNA POR PRECAUÇÃO'],'COMPARAÇÃO HIPOTÉTICA'),
 graph('A segunda pode','PODE SER ÓTIMA.',['MAS TEM UM BARULHO NO QUINTAL'],'COMPARAÇÃO HIPOTÉTICA'),
 graph('Isso não confirma','A IMAGEM NÃO CONFIRMA',['PERSEGUIÇÃO','EMBOSCADA','SISTEMA DE FURTIVIDADE'],'LIMITES DA EVIDÊNCIA'),
 shot('A análise é das imagens',G(3),'VISÍVEL. ENCOBERTO.','ANÁLISE DOS ENQUADRAMENTOS'),
 vid('As duas regiões',T2,6.2,'A ÁGUA LIGA AS PAISAGENS.','KEYS • TRAILER 2',motion=1.6),
 shot('Nas Keys, procuro',K(1),'PROCURE O HORIZONTE.','KEYS • IMAGEM ANALISADA'),
 shot('Em Grassrivers, examino',G(3),'EXAMINE A PRÓXIMA CURVA.','GRASSRIVERS • IMAGEM ANALISADA'),
 shot('Porque',K(1),'MESMA ÁGUA.\nOUTRA DESCONFIANÇA.','DUAS PAISAGENS • GTA VI',hook=True),
]
edit.PLANS['C10']=[
 vid(None,TV,148,'PROPAGANDA\nNA SUA PLAYLIST.','GTA V • SELF RADIO NO PC',hook=True,motion=5),
 graph('No GTA cinco','MODO RADIO • PC',['SUA MÚSICA','LOCUÇÃO + INTERVALOS'],'SELF RADIO • RECURSO DOCUMENTADO',radio=True),
 vid('Sua seleção começa',TV,154,'UMA ESTAÇÃO DAQUELE MUNDO.','GTA V • CONTEXTO DE DIREÇÃO',motion=5),
 vid('Isso muda',TV,151,'UMA LISTA PESSOAL.','GTA V • CONTEXTO DE DIREÇÃO',motion=5),
 graph('Quando entra um locutor','MAIS GENTE OUVINDO',['SUA SELEÇÃO','UM PÚBLICO IMAGINADO'],'LEITURA DO CANAL',radio=True),
 graph('É engraçado','FORA DO JOGO',['PAGAR PARA FUGIR DO ANÚNCIO'],'COMPARAÇÃO EDITORIAL',radio=True),
 vid('Dentro de GTA',TV,154,'O ANÚNCIO AJUDA A CIDADE.','GTA V • CONTEXTO DE DIREÇÃO',motion=3),
 graph('A paz durou','O INTERVALO ENCONTROU VOCÊ.',['OUTRO CAMINHO PARA A PROPAGANDA'],'HUMOR EDITORIAL',radio=True),
 graph('E um anúncio fictício','O QUE ESSA CIDADE VALORIZA?',['O QUE VENDE?','PARA QUEM?'],'LEITURA DO CANAL',radio=True),
 vid('A rua fica',TV,154,'A RUA NA IMAGEM. A CIDADE NO SOM.','GTA V • CONTEXTO DE DIREÇÃO',motion=5),
 graph('Estou falando','GTA V • PC',['SELF RADIO','MODO RADIO'],'ESCOPO DO RECURSO',radio=True),
 graph('Isso não confirma','NÃO É CONFIRMAÇÃO DE GTA VI',['NEM DESCRIÇÃO DE TODOS OS MODOS'],'LIMITES DA EVIDÊNCIA',radio=True),
 vid('O detalhe interessante',TV,148,'MÚSICAS PESSOAIS. EMISSORA DO JOGO.','GTA V • CONTEXTO DE DIREÇÃO',motion=5),
 graph('Não é só','TEM UMA CIDADE NOS INTERVALOS.',['SUA FAIXA','A APRESENTAÇÃO DO MUNDO'],'LEITURA DO CANAL',radio=True),
 vid('Afinal',TV,148,'PROPAGANDA\nNA SUA PLAYLIST.','GTA V • SELF RADIO NO PC',hook=True,motion=5),
]
edit.PLANS['C11']=[
 vid(None,T2,12,'MORA GRÁTIS.\nMAS TEM COBRANÇA.','JASON + BRIAN • GTA VI',hook=True,motion=5),
 vid('Brian oferece',T2,18.5,'UMA CASA. UMA CONTRAPARTIDA.','TRAILER 2 • BRIAN E JASON',motion=5),
 graph('É o acordo','O ACORDO DESCRITO',['MORADIA SEM ALUGUEL','AJUDA NAS COBRANÇAS'],'SÍNTESE DO PERFIL OFICIAL'),
 graph('O boleto desapareceu','A OBRIGAÇÃO MUDOU DE FORMATO.',['MORADIA ↔ SERVIÇOS'],'LEITURA DO CANAL'),
 vid('Ter um lugar',T2,7.8,'UM LUGAR PRA MORAR.','TRAILER 2 • AMBIENTE DE JASON',motion=3.5),
 vid('Ao mesmo tempo',T2,20,'PEDIDOS E SERVIÇOS.','TRAILER 2 • BRIAN E JASON',motion=3),
 shot('A relação fica',B(4),'O QUE CADA LADO ENTREGA?','ANÁLISE DA RELAÇÃO'),
 graph('Imagina precisar','E SE PRECISAR RECUSAR?',['UMA TAREFA','A SUA MORADIA'],'SITUAÇÃO HIPOTÉTICA'),
 graph('A conversa começa','COMEÇA COM UM FAVOR.',['TERMINA COM AS CAIXAS?'],'SITUAÇÃO HIPOTÉTICA'),
 graph('Essa situação','POSSIBILIDADE.',['NÃO É UMA CENA ANUNCIADA'],'LIMITE DO EXEMPLO'),
 graph('Também não prova','O ACORDO NÃO PROVA',['TRAIÇÃO','PERDA DA CASA'],'LIMITES DA EVIDÊNCIA'),
 vid('O que sabemos',T2,13,'O QUE SABEMOS É A TROCA.','TRAILER 2 • BRIAN E JASON',motion=4),
 graph('A tensão vem','DIFÍCIL SEPARAR',['GRATIDÃO','INTERESSE','OBRIGAÇÃO'],'LEITURA DO CANAL'),
 shot('É aquela oferta',B(3),'LEVE NA OFERTA. PESADA NA VEZ.','LEITURA DO CANAL'),
 vid('Por isso, o detalhe',T2,18.5,'MORADIA TAMBÉM É RELAÇÃO.','TRAILER 2 • BRIAN E JASON',motion=5),
 graph('Quando alguém','O QUE ACOMPANHA A AJUDA?',['OFERTA','PEDIDO'],'LEITURA DO CANAL'),
 shot('Principalmente',B(4),'INCLUI A CHAVE DA SUA CASA.','LEITURA DO CANAL'),
 vid('Porque',T2,12,'MORA GRÁTIS.\nMAS TEM COBRANÇA.','JASON + BRIAN • GTA VI',hook=True,motion=3),
]
edit.PLANS['C12']=[
 vid(None,'videosGTAVI/GTAVI_Videos/Raul_Bautista_Video_Clip.mp4',0,'SABE ROUBAR.\nMAS SABE PARAR?','RAUL BAUTISTA • GTA VI',hook=True,motion=1),
 shot('A apresentação oficial',R(3),'EXPERIÊNCIA + RISCO CRESCENTE.','SÍNTESE DO PERFIL OFICIAL'),
 shot('As duas características',R(2),'AS DUAS COISAS JUNTAS.','LEITURA DO PERFIL'),
 graph('Quem já escapou','O QUE A EXPERIÊNCIA ENSINA?',['RECONHECER O PERIGO','OU CONFIAR DEMAIS?'],'LEITURA DO CANAL'),
 vid('Também pode começar','videosGTAVI/GTAVI_Videos/Raul_Bautista_Video_Clip.mp4',0,'SEMPRE DAR UM JEITO?','RAUL • CLIPE OFICIAL',motion=1),
 graph('O currículo aumenta','O LIMITE PEDIU DEMISSÃO.',['EXPERIÊNCIA NÃO É GARANTIA'],'HUMOR EDITORIAL'),
 graph('Imagina alguém','UM PLANO. A CALMA DE UMA PIZZA.',['O RISCO CONTINUA ALI'],'SITUAÇÃO INVENTADA'),
 graph('A tranquilidade convence','QUEM TEM ROTA DE VOLTA?',['O ENTREGADOR','OU A EQUIPE?'],'SITUAÇÃO INVENTADA'),
 graph('Essa situação','ESSE PLANO FOI INVENTADO.',['NÃO É MISSÃO ANUNCIADA'],'LIMITE DO EXEMPLO'),
 shot('O perfil não entrega',R(1),'O PERFIL NÃO ENTREGA UMA MISSÃO.','LIMITES DA EVIDÊNCIA'),
 graph('Ele permite observar','UMA TENSÃO',['CAPACIDADE','CONFIANÇA','RISCO'],'LEITURA DO PERFIL'),
 graph('Uma pergunta','QUEM PAGA QUANDO DÁ ERRADO?',['QUEM PROPÕE?','QUEM ASSUME O CUSTO?'],'CRITÉRIO DE LEITURA'),
 shot('A resposta pode',R(3),'A RESPOSTA MUDA A CORAGEM.','LEITURA DO CANAL'),
 graph('Às vezes','QUEM FICOU COM A CONTA?',['DISCURSO','CONSEQUÊNCIA'],'LEITURA DO CANAL'),
 vid('Eu prestaria atenção','videosGTAVI/GTAVI_Videos/Raul_Bautista_Video_Clip.mp4',0,'SABER FAZER. SABER PARAR.','RAUL • CLIPE OFICIAL',motion=1),
 shot('Experiência pode',R(4),'EXPERIÊNCIA ≠ PRUDÊNCIA.','LEITURA DO CANAL'),
 shot('Afinal',R(1),'SABE ROUBAR.\nMAS SABE PARAR?','RAUL BAUTISTA • GTA VI',hook=True),
]

def audio(rid):
    p=edit.BASE/rid
    raw=edit.BASE/'C09/voz/lote_raw'/f'{rid}_narracao.wav'
    dest=p/'voz/narracao_original.wav'
    if not dest.exists():shutil.copy2(raw,dest)
    if not (p/'voz/narracao.wav').exists():producao.normalize(dest,p/'voz/narracao.wav')
    if not (p/'voz/palavras_asr.json').exists():
        from faster_whisper import WhisperModel
        import numpy as np
        temp=p/'voz/asr_audio.f32'
        producao.run(['-i',p/'voz/narracao.wav','-ar','16000','-ac','1','-f','f32le',temp])
        model=WhisperModel('small',device='cpu',compute_type='int8',cpu_threads=4,download_root=str(ROOT/'.course-tools/models'),local_files_only=True)
        segments,_=model.transcribe(np.fromfile(temp,dtype=np.float32),language='pt',beam_size=1,vad_filter=True,word_timestamps=True,initial_prompt='Jason. Brian Heder. Raul Bautista. GTA seis. Self Radio. Leonida Keys. Grassrivers.')
        words=[dict(word=w.word.strip(),start=round(w.start,3),end=round(w.end,3),probability=round(w.probability,4)) for s in segments for w in (s.words or [])]
        assert words
        edit.write_json(p/'voz/palavras_asr.json',words)
        temp.unlink()
        edit.write_json(p/'voz/configuracao_asr.json',dict(model='small',device='cpu',compute_type='int8',beam_size=1,cpu_threads=4))
    stats={}
    for name in ['narracao_original.wav','narracao.wav']:
        wav=p/'voz'/name
        with wave.open(str(wav)) as w:stats[name]=dict(duration=w.getnframes()/w.getframerate(),rate=w.getframerate(),channels=w.getnchannels(),sample_width=w.getsampwidth())
        log=producao.run(['-i',wav,'-af','loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json','-f','null','-'])
        stats[name]['loudness']=json.loads(log[log.rfind('{'):log.rfind('}')+1])
        log=producao.run(['-i',wav,'-af','silencedetect=noise=-40dB:d=1.5','-f','null','-'])
        stats[name]['silences_over_1_5s']=[x for x in log.splitlines() if 'silence_' in x]
    edit.write_json(p/'voz/validacao_audio.json',stats)
    print('AUDIO '+rid,flush=True)

def finish(rid):
    p=edit.BASE/rid
    import shorts_publicacao as pub
    pub.make(rid)
    old=p/'historico/antes_revisao_20261031/publicacao'
    for name in ['capa_master.png','capa_youtube.jpg','thumbnail_base_gerada.png','PROMPT_THUMBNAIL.txt']:
        shutil.copy2(old/name,p/'publicacao'/name)
    guide=p/'publicacao/00_GUIA_DE_PUBLICACAO.md'
    t=guide.read_text(encoding='utf8').replace('Preparado em 27/10/2026.','Revisado em 31/10/2026.')
    guide.write_text(t,encoding='utf8')
    (p/'publicacao/08_FONTES_RECONFERIDAS_20261031.md').write_text('''# Fontes reconferidas em 31/10/2026

Perfis oficiais: https://www.rockstargames.com/VI/only-in-leonida
Brian oferece moradia sem aluguel em troca de ajuda nas cobranças locais. Raul é apresentado como assaltante experiente cuja imprudência aumenta as apostas. Essas informações sustentam C11/C12; os exemplos hipotéticos são identificados na edição.

Self Radio: https://support.rockstargames.com/articles/5L6IP5RzI8kQXyXCddPO2Z/how-to-play-custom-music-on-the-self-radio-station-in-gtav-and-gta-online-on-pc
O modo Radio intercala arquivos pessoais com anúncios e DJ. C10 se refere a GTA V no PC. A imagem de direção não é demonstração da configuração da Self Radio.

Biblioteca oficial: https://www.rockstargames.com/VI/media
As fotografias das Keys/Grassrivers são preservadas quando C09 analisa os seus enquadramentos. Vídeos identificados de água entram em passagens de ambientação e não substituem a evidência fotográfica.

Regras YouTube consultadas na data:
- https://support.google.com/youtube/answer/72431?hl=pt-BR — Shorts: miniatura personalizada no Studio desktop com conta verificada, 9:16 recomendado.
- https://support.google.com/youtube/answer/9884579?hl=pt-BR — capítulos: ao menos três, início 00:00, mínimo 10 s por capítulo. Os marcadores do pacote são opcionais para consulta, sem promessa de capítulos no player Shorts.
- https://support.google.com/youtube/answer/146402?hl=pt-BR — tags no campo próprio; efeito geralmente pequeno fora de grafias incorretas.
- https://support.google.com/youtube/answer/6388789?hl=pt-BR — telas finais em 5–20 s finais, vídeo com pelo menos 25 s. Esta edição mantém retorno ao gancho e não acrescenta tela final.
- https://support.google.com/youtube/answer/14328491?hl=pt-BR — declarar alterações realistas significativas conforme o uso efetivo. A origem da voz personalizada não foi presumida.

As capas anteriores foram inspecionadas em prancha a 25%: legíveis, fiéis ao assunto e diferenciadas; preservadas sem nova geração faturável. Arte-base é montagem editorial, não captura oficial.

Não houve upload, publicação, agendamento ou acesso ao Postiz.
''',encoding='utf8')
    data=json.loads((p/'projeto/timeline.json').read_text(encoding='utf8'))
    files=[p/'voz/NARRACAO.txt',p/'voz/GEMINI.txt',p/'voz/narracao_original.wav',p/'voz/narracao.wav',p/'exportacoes'/f'Pixel_Procurado_{rid}_Short_1080x1920.mp4',p/'exportacoes'/f'{rid}_legendas.srt',p/'publicacao/capa_master.png',p/'publicacao/capa_youtube.jpg']
    video_shots=[s for s in data['shots'] if s['file'].endswith('.mp4')]
    motion_seconds=sum(min(s['frames']/30,s.get('motion',s['frames']/30)) for s in video_shots)
    manifest=dict(id=rid,date='2026-10-31',inputs=[dict(path=str(x.relative_to(ROOT)),sha256=hashlib.sha256(x.read_bytes()).hexdigest(),bytes=x.stat().st_size) for x in files],shots=len(data['shots']),video_shot_seconds=sum(s['frames']/30 for s in video_shots),source_motion_seconds=motion_seconds,duration=data['duration'],tts=dict(model='gemini-3.8-flash-tts',voice='voice_iagtq1gnk2br',language='pt-BR'),limits=['Revisão visual por amostras, não escuta humana integral.','Fontes horizontais preservadas em painel vertical; GTA V de apoio é 720p.','C09 analisa fotografias específicas; C12 perfil e hipóteses sem missão anunciada.','Trechos muito curtos sustentam o último quadro após o movimento; tempo real em source_motion_seconds.','Sem upload, agendamento ou Postiz.'])
    edit.write_json(p/'projeto/manifesto_revisado.json',manifest)
    qa=json.loads((p/'projeto/qa/validacao_final.json').read_text(encoding='utf8'))
    wav=json.loads((p/'voz/validacao_audio.json').read_text(encoding='utf8'))['narracao.wav']
    lines=[f'# {rid} — revisão concluída em 31/10/2026','',f"Voz integral: {data['duration']:.3f} s. MP4: {qa['video_duration']:.3f} s, {qa['width']}×{qa['height']}, {qa['fps']} fps, {qa['video_codec']}/{qa['audio_codec']}.",f"Planos: {len(data['shots'])}; legendas: {len(data['captions'])}. Planos de vídeo: {len(video_shots)}, com {motion_seconds:.2f} s efetivos de movimento da fonte; após a duração disponível, último quadro sustentado.",f"Voz normalizada medida: {wav['loudness']['input_i']} LUFS / {wav['loudness']['input_tp']} dBTP. Silêncios >1,5 s: {wav['silences_over_1_5s']}.",'','Decodificação integral final sem erros. Correlação do áudio exportado com WAV normalizado em cinco janelas: '+', '.join(f"{x['correlation']:.6f}" for x in qa['audio_correlations'])+'.','Amostras visuais em projeto/qa/contato.jpg; imagens da amostra em projeto/amostra_previa.jpg quando aplicável. Revisão final independente cabe ao coordenador.','','## Limites','',*['- '+x for x in manifest['limits']],'','## SHA-256','',*['- '+str(x.relative_to(ROOT))+': '+hashlib.sha256(x.read_bytes()).hexdigest() for x in files],'','Roteiros preservados. Capas anteriores validadas e reaproveitadas; histórico por ID mantido. Fontes e regras de publicação reconferidas em publicacao/08_FONTES_RECONFERIDAS_20261031.md.']
    lines.insert(6,f"AAC final medido: {qa['loudness_aac']['input_i']} LUFS / {qa['loudness_aac']['input_tp']} dBTP. A codificação apresentou pequeno overshoot sobre o alvo −1,5 dBTP do WAV, registrado sem afirmar pico idêntico ao master.")
    (p/'RELATORIO_REVISAO_20261031.md').write_text('\n'.join(lines)+'\n',encoding='utf8')

def preview(rid):
    import av
    from PIL import Image
    p=edit.BASE/rid/'projeto'
    sheet=Image.new('RGB',(1080,640))
    for col,index in enumerate([0,2,8]):
        with av.open(str(p/f'render/{index:03}.mp4')) as c:
            t=min(1,float(c.duration/1e6)-.05)
            c.seek(int(t*1e6))
            f=next(f for f in c.decode(video=0) if float(f.time)>=t)
            im=f.to_image();im.thumbnail((360,640));sheet.paste(im,(col*360,0))
    sheet.save(p/'amostra_previa.jpg')

if __name__=='__main__':
    action=sys.argv[1]
    for rid in sys.argv[2:] or IDS:
        if action=='audio':audio(rid)
        elif action=='prepare':edit.prepare(rid)
        elif action=='sample':edit.render(rid,{0,2,8})
        elif action=='render':edit.render(rid)
        elif action=='qa':edit.qa(rid)
        elif action=='finish':finish(rid)
        elif action=='preview':preview(rid)
        else:raise ValueError(action)







