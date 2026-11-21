"""Monta REVISAO_FINAL.json a partir do modelo + observacoes do revisor final (Dia 9)."""
import hashlib, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EPR = 'producao/SERIE_AQUECIMENTO_GTA6/DIA_09_2026-11-17'
EP = ROOT / EPR
RF = f'{EPR}/revisao_final'
m = json.loads((EP / 'REVISAO_FINAL_modelo.json').read_text(encoding='utf-8'))


def sha(p):
    return hashlib.sha256((ROOT / p).read_bytes()).hexdigest()


m['revisor'] = {'modelo': 'claude-opus-5-5', 'agent_id': 'revisor-final-independente-dia09'}
m['data'] = '2026-11-17'
extras = [f'{EPR}/publicacao/capas/{c}' for c in ('capa_longo_A.jpg', 'capa_longo_B.jpg', 'capa_vertical_A.jpg', 'capa_vertical_B.jpg')]
extras += [f'{EPR}/publicacao/carrossel/0{i}.jpg' for i in range(1, 5)]
extras += [f'{EPR}/publicacao/{t}' for t in ('01_TITULO_A.txt', '02_TITULO_B.txt', '03_DESCRICAO.txt', '04_TAGS.txt',
                                            '05_COMENTARIO_FIXADO.txt', 'publicacao_secao.json')]
m['artefatos'] += [{'caminho': p, 'sha256': sha(p)} for p in extras]

N = 'NÃO OUVIDO POR HUMANO: conferido por ASR (faster-whisper small; trechos suspeitos também medium): '
aud = {
    (0, 10): N + '"Vice City pede documento na porta. Placa de Neon, over 21 only, ID check. Sim, o jogo mais esperado da década tem segurança de bala[da]". Voz começa no quadro 0 (palavra "Vice" 0,00-0,42 s), gancho de 6 palavras termina em 2,4 s, sem vinheta/respiração antes. RMS 0,162.',
    (125, 140): N + '"espero que o raio caia duas vezes no mesmo lugar. Na arte oficial do Drake One [Dre\'Quan], aparecem duas mulheres de top brilhante numa pista de luz rosa. Eu não vou dizer que são elas. A arte não tem legenda...". Bate com o roteiro; "Dre\'Quan" vira "Drake One/Drei Kuan" no ASR (pronúncia a confirmar por ouvido, sem impacto factual).',
    (245, 260): N + '"Não sei quem são, nem do que falo [falam]. Reunião de mobiliária [imobiliária] no escuro. A Oxstar [Rockstar] não legendou... outra festa. Essa azul com escada, a gente dançando, um caraca [careca] de terno". O ASR medium repete "A Oxstar" e "caraca"; o ASR da produção também. Pode ser só o R aspirado do PT-BR ou a vogal átona, mas precisa de escuta humana em 249,5-250,1 e 257,7-258,1.',
    (365, 380): N + '"O vídeo termina essa sequência cortando do telhado para a cidade à noite, depois para um prédio com piscina e gente tomando sol, e depois para uma cabine de DJ com as mãos para o alto. Da noite armada, para o sol e para a pista em dois cortes. Prefiro o corte". Bate com o roteiro (par. 20).',
    (410.4, 420.4): N + '"[vinte e quatro] horas. E me conta aí, se a porta pedisse o documento, [você] entrava ou ficava na fila? Se inscreve no canal e até amanhã, que agora faltam só 2 dias." Final limpo; "dias" termina em ~419,98 s e o vídeo acaba em 420,42 s sem preto.',
}
for t in m['audio_trechos_ouvidos']:
    t['observacao'] = aud[(t['inicio'], t['fim'])]
m['audio_trechos_ouvidos'] += [
    {'inicio': 40, 'fim': 47, 'observacao': N + '"Em baixo do cartaz aparece um logo, JOUH, Jack of Hearts." A palavra suspeita "cartaz" (par. 4) veio correta no ASR.'},
    {'inicio': 348, 'fim': 356, 'observacao': N + '"e gentileza não é fonte. Terno tem. Dá pra seguir um blazer verde-oliva do roll [hall] ao corredor armado." A frase suspeita "Terno, tem" (par. 19) veio inteligível no ASR.'},
    {'inicio': 394, 'fim': 401, 'observacao': N + '"jogo, se é só enfeite. Sobre o ID check, a única fonte que eu tenho é o cartaz. Isso eu coloco na lista..." "cartaz" (par. 21) veio correto no ASR small; o ASR da produção ouviu "Cartais". Vale escuta humana em 398,8-399,3.'},
]

fr = {
    15: 'Hall roxo da festa (EXT 21:00), homem de chapéu e mulher de vestido. Legenda "eu prometi balada, Boobie Ike, terno". Ilustra a lista da promessa. OK.',
    45: 'Porta com OVER 21 / ID Check e logo JOH Jack of Hearts (EXT 17:33) em "um logo: J O H, Jack". Imagem = fala. OK.',
    75: 'Arte oficial Boobie (close, copo, corrente) em "strip e um estúdio de gravação". Card ARTE OFICIAL já saiu. OK.',
    105: 'Arte oficial Dre\'Quan (neon "…ai Dreams", piscina) em "mais malandro que gangster". OK.',
    135: 'Arte oficial do estúdio (camisa MANATEES) em "elas. A arte não tem legenda". As mulheres saíram de cena antes do "não vou dizer que são elas". OK.',
    165: 'Arte oficial Vice City (notas, poste, luz rosa) em "quando o sol se apaga". Bate com o par. 9. OK.',
    195: 'Terraço de dia (camisa havaiana, mesa) em "À noite, a conta chega". Fim do par. 10. OK.',
    225: 'Andar escuro ao sair do elevador (EXT 21:58) em "ainda não explicou: a imagem só [mostra elevador]". Descompasso leve: o plano já saiu do elevador. Baixa.',
    255: 'Festa azul com escada (EXT 22:55); card saindo (animação de saída) em "azul, com escada, gente dançando". OK.',
    285: 'Mascarado de jaleco branco com fuzil, close, em "Em seguida, homens de máscara e jaleco branco". Imagem = fala; sem sangue. OK.',
    315: 'Tiroteio no escritório (EXT 25:03, HUD 16/78, faísca distante) em "conferir. A pistola silenciada existe". Sem gore. OK.',
    345: 'Andar em obra com barreira amarela (EXT 25:32) em "barreira amarela. Chamar isso de cobertura". Imagem = fala. OK.',
    375: 'Arte oficial VC07 (pole dance, notas) em "Da noite armada pro sol e pra pista". Ilustra a "pista". OK.',
    405: 'Arte oficial Boobie e Dre\'Quan com o letreiro Jack of Hearts na transição para o par. 22. Sem legenda no quadro (pausa entre frases). OK.',
    420: 'Último segundo: arte Dre\'Quan na pista roxa com a legenda "dias.". Sem quadro preto no fim. OK.',
}
cards = {
    1.0: 'Gancho: porta OVER 21 / ID Check / JOH desde o quadro 0; card VÍDEO OFICIAL 17:33 entrou; legenda "Vice City pede documento na porta.". Sem vinheta. OK.',
    3.82: 'Card 17:35 entrando sobre a porta (dois homens se cumprimentando) em "Placa de neon: over twenty-one only". OK.',
    7.82: 'Card 21:38, elevador com o homem de blazer oliva, em "ID check. Sim, o jogo mais". Prévia da promessa; ligação com a fala é solta, mas aceitável.',
    13.82: 'Card 21:00 no hall da festa em "eu prometi balada, Boobie Ike, terno". OK.',
    19.82: 'Card 24:55: escritório escuro com HUD e um corpo caído ao fundo, à direita e pequeno, em "Uma palavra dessa lista eu conferi". Violência fora do primeiro plano. Baixa.',
    34.88: 'Card ARTE OFICIAL (Boobie, close) em "Nome de personagem só entra quando". OK.',
    42.0: 'Card 17:33, porta com cartaz e logo JOH, em "Ele errou. Embaixo do cartaz aparece". OK.',
    46.5: 'Card ARTE OFICIAL, palco JOH Jack of Hearts com dançarinas, em "of Hearts. Será que é do". OK.',
    58.0: 'Card ARTE OFICIAL, Boobie e Dre\'Quan com o letreiro Jack of Hearts, em "seja o mesmo lugar do perfil". OK.',
    66.1: 'Card ARTE OFICIAL, palco JOH com Boobie, em "Boobie Ike, segundo a Rockstar, é". OK.',
    74.93: 'Card ARTE OFICIAL, Boobie close, em "strip e um estúdio de gravação". OK.',
    83.76: 'Card ARTE OFICIAL, Boobie na poltrona de óculos com o maço de notas, em "poltrona, de óculos escuros, com um". Imagem = fala. OK.',
    92.58: 'Card ARTE OFICIAL, Dre\'Quan na pista, em "e advogado. O negócio que mais". OK.',
    101.33: 'Card ARTE OFICIAL, Dre\'Quan no neon Dreams, em "[jovem aspirante] a magnata". OK.',
    110.08: 'Card ARTE OFICIAL, estúdio, em "do Boobie, mas assinou as Real". OK.',
    118.82: 'Card ARTE OFICIAL, Dre\'Quan na pista (sem mulheres em primeiro plano), em "As Real Dimez são Bae-Luxe e". OK.',
    126.82: 'Card ARTE OFICIAL D01, duas mulheres de top brilhante, em "raio caia duas vezes no mesmo". O R7 opcional não foi aplicado: as mulheres entram ~1 s antes de "Na arte oficial do Dre\'Quan", ainda na frase das Real Dimez. Baixa.',
    133.82: 'Card ARTE OFICIAL, estúdio, em "Eu não vou dizer que são elas". As mulheres já saíram. OK.',
    149.28: 'Card ARTE OFICIAL, Boobie com o maço de notas, em "e o dinheiro da droga paga". OK.',
    157.22: 'Card ARTE OFICIAL VC07 (notas, poste, rosa) em "graça. Essa é a arte oficial". OK.',
    166.57: 'Card ARTE OFICIAL, Dre\'Quan no neon, em "apaga e o neon acende, todo". OK.',
    175.92: 'Card 10:00, terraço de dia com HOLD HANDS na tela, em "Mas Vice City também". OK.',
    181.41: 'Card 10:12, bar aberto com camisa havaiana e letreiro Efflu…, em "Olhar Estendido: bar aberto, sol, camisa". OK.',
    186.91: 'Card 10:50, letreiro Effluvia legível, em "O letreiro parece dizer Effluvia". OK.',
    192.41: 'Card 11:08, terraço, em "prova nada. De dia, o luxo". OK.',
    197.9: 'Card 21:07, hall roxo, homem de chapéu e de blazer rosa, em "Agora a noite do vídeo.". OK.',
    207.2: 'Card 21:16, hall com balões e mulheres de vestido, em "dele tem um de chapéu e". OK.',
    216.5: 'Card 21:45, homem de blazer oliva diante das portas do elevador, em "Depois vem o elevador.". OK.',
    225.3: 'Card 21:58 (quadro próprio em frames_card2): andar escuro em obra logo após o elevador, em "a imagem só [mostra elevador]". Descompasso leve, já registrado. Baixa.',
    233.5: 'Card 22:05, corredor com portas, em "errado. Andar de cima: escuro, meio". OK.',
    240.1: 'Card 22:12, sala com a maquete de prédio iluminada, laptop e homem de blazer rosa, em "Dois homens, um de blazer rosa". OK.',
    253.28: 'Card 22:55, festa azul com escada, em "Mais pra frente, outra festa, essa". OK.',
    259.72: 'Card 23:12, festa (homem de gravata-borboleta), em "dela, um homem de máscara no". O mascarado de respirador entra em 261,5 s (quadro Y_0261.50), ~1 s depois. Aceitável.',
    266.16: 'Card 23:38, escritório escuro com HUD 13/78, em "só balada. Porque no quadro seguinte". OK.',
    272.93: 'Card 23:45: tiroteio com corpo no chão e mancha de sangue no plano médio, em "tiroteio. Uma mensagem na tela". A fala é sobre o tiroteio; não é fala neutra. Aceitável.',
    279.7: 'Card 23:53 sobre a mensagem "Lucia: After Czr, he\'s in saferoom" em "Outra menciona uma sala segura.". O card cobre parte da mensagem por ~1,5 s; ela já estava visível antes. Aceitável.',
    286.48: 'Card 24:00, mulher (close) no escritório, em "Em seguida, homens de máscara e". OK.',
    293.2: 'Card 24:10, sala azul com gente caída ao fundo, em "Quem são? Não confirmado". Sem close de ferimento. Aceitável.',
    297.5: 'Card 24:32, placa FLOOR 26 grande em 297,2-298,8, junto de "floor twenty-six". R3 corrigido. OK.',
    300.0: 'Card 24:14, corredor azul, em "twenty-six: andar vinte e seis". OK.',
    314.82: 'Card 25:03, tiroteio no escritório sem gore, em "conferir. A pistola silenciada existe". OK.',
    319.72: 'Card 25:35, mulher junto da barreira amarela (a pistola no chão entra em seguida), em "pistola com silenciador aparece caída no". OK.',
    323.5: 'Card 25:37, still recortado com a pistola com silenciador grande no chão, em "visível. O que o vídeo não". Já em 322,8 s, junto de "cano comprido bem", a pistola ocupa o quadro. R2 corrigido. OK.',
    327.72: 'Card 25:11, braço de jaleco branco disparando a pistola, em "foi essa a arma dos tiros". OK.',
    337.2: 'Card 24:48, andar de escritórios com HUD, em "Cobertura também é palpite.". OK.',
    341.6: 'Card 25:23, porta NOTICE ROOF ACCESS e escada, em "com aviso de acesso ao telhado". Imagem = fala. OK.',
    343.8: 'Card 25:32: mulher engatinhando com a barreira amarela ao fundo, em "e um andar em obra com". Não há esganadura nem rosto ensanguentado (R1 corrigido), mas o homem de jaleco caído fica em primeiro plano à esquerda, com gotas de sangue no chão, de 342,8 a ~343,6. Baixa.',
    349.8: 'Card 24:53, escritório com HUD, em "é fonte. Terno, tem.". OK.',
    352.08: 'Card 21:30, homem de blazer oliva no elevador com a mulher, na pausa antes de "Dá pra seguir um blazer verde-oliva". Sem legenda: o quadro cai no intervalo do SRT, 351,90-352,42. OK.',
    359.24: 'Card 23:30, corredor armado com HUD, em "é figurino, e figurino não é". OK.',
    368.0: 'Card 25:45, cidade à noite, em "do telhado pra cidade à noite". OK.',
    373.6: 'Card 25:54, cabine de DJ com mãos para o alto (372,9-374,4), em "pra uma cabine de DJ com". R4 corrigido. OK.',
    375.6: 'Card ARTE OFICIAL VC07 em "Da noite armada pro sol e". OK.',
    391.28: 'Card 17:33, porta do clube, em "E como funciona a porta com". OK.',
    397.2: 'Card 17:34, still do cartaz OVER 21 ONLY / ID Check (396,4-399,0), em "ID check, a única fonte que". R5 corrigido. OK.',
    400.4: 'Card ARTE OFICIAL, Boobie e Dre\'Quan, em "Isso eu coloco na lista de". OK.',
    413.78: 'Card ARTE OFICIAL, Dre\'Quan na pista, em "porta pedisse documento, você entrava ou". OK.',
}
for f in m['frames_inspecionados']:
    t = f['timecode']
    if isinstance(t, float) and t == 225.0:  # o 225 inteiro e a janela de 30 s; 225.0 e o card
        f['timecode'] = 225.3
        f['arquivo_imagem'] = f'{RF}/frames_card2/C_0225.30.jpg'
        f['observacao'] = cards[225.3]
        continue
    f['arquivo_imagem'] = f'{RF}/frames/L_{float(t):07.2f}.jpg'
    f['observacao'] = fr.get(t) or cards[t]
extra = {
    0.0: 'Quadro 0: porta OVER 21 / ID Check / JOH com a legenda do gancho já na tela. Sem preto e sem vinheta. OK.',
    342.8: 'Início do plano 52: homem de jaleco caído em primeiro plano, à esquerda, e mulher engatinhando. Sem esganadura. Baixa (corpo em fala neutra).',
    343.2: 'Mulher engatinhando, barreira amarela ao fundo, homem caído ainda à esquerda. Baixa.',
    322.8: 'Still Q2537: pistola com silenciador grande, junto de "chão, com o cano comprido bem". Fato confere com FONTES (25:36,8-25:38,5).',
    297.8: 'Placa FLOOR 26 legível junto de "A única placa legível é floor". OK.',
    373.4: 'Cabine de DJ com mãos para o alto, junto de "pra uma cabine de DJ com". OK.',
    396.4: 'Still do cartaz OVER 21 ONLY / ID Check em "se é só enfeite: sobre o". OK.',
    126.5: 'D01 (duas mulheres) já na tela em "raio caia duas vezes no mesmo" (R7 opcional não aplicado). Baixa.',
    20.5: 'Escritório com HUD e faísca, sem gore, em "Uma palavra dessa lista eu conferi". OK.',
    419.5: 'Fim: arte Dre\'Quan com "amanhã, que agora faltam só dois". Sem preto. OK.',
}
for t, o in extra.items():
    m['frames_inspecionados'].append({'timecode': t, 'arquivo_imagem': f'{RF}/frames_extra/X_{t:07.2f}.jpg', 'observacao': o})

cart = {
    29.0: 'Cartela C03 REGRAS DE HOJE (24,88-33,88): o texto bate com o par. 3. A legenda queimada fica abaixo do texto, sem colisão neste quadro. OK.',
    53.0: 'Cartela C04 TAGLINE: "It\'s all about heart — the Jack of Hearts", igual a F1. A legenda queimada ("about heart, the Jack of Hearts") fica SOBRE o rodapé "rockstargames.com/VI/boobie · consulta 17/11/2026", e a fonte fica ilegível (recorte em revisao_final/prancha_rodapes.jpg). Média.',
    144.0: 'Cartela C08 PÁGINA OFICIAL DE VICE CITY: a tradução bate com F5. O rodapé "Tradução livre · rockstargames.com/VI/vice-city · 17/11/2026" fica coberto pela legenda queimada ("do perfil do Boobie, e ela"). Média.',
    310.5: 'Cartela C17 CONFERI NO QUADRO: "Pistola silenciada: existe (25:37) / Quem usou: não confirmado / Cobertura: não confirmado", igual a FONTES. O rodapé "Quadro de 25:37 do vídeo oficial An Extended Look" fica coberto pela legenda queimada. Média.',
    385.5: 'Cartela C21 NÃO CONFIRMADO: os 5 itens batem com o par. 21 e FONTES. O 5º item ("Como funciona o ID check") fica coberto pela legenda queimada durante quase toda a cartela (também em 388,5 s). Média.',
    409.0: 'Cartela C22 AMANHÃ: DIA 10 / Véspera / As últimas 24 horas / GTA 6 · 19 de novembro de 2026: data correta e sem colisão. OK.',
}
for t, o in cart.items():
    m['frames_inspecionados'].append({'timecode': t, 'arquivo_imagem': f'{RF}/frames_cartelas/K_{t:07.2f}.jpg', 'observacao': o})
y = {
    260.5: '"um homem de máscara no [rosto]": o plano ainda mostra o senhor de gravata-borboleta. O mascarado entra em 261,5 (respirador). Descompasso de ~1 s, aceitável.',
    261.5: 'Mascarados de respirador e jaleco com fuzil em "rosto. Esse é o último quadro". Coerente com "homem de máscara no rosto".',
    262.5: 'Mascarado aponta a pistola e outro empurra uma pessoa com os braços erguidos, em "Esse é o último quadro em que a balada ainda parece só balada". É confronto, sem ferimento visível. Baixa (já é a virada).',
    263.5: 'Três mascarados armados no hall em "em que a balada ainda parece". Sem tiro. Aceitável.',
    264.5: 'Mascarado com fuzil em "só balada. Porque no quadro seguinte". Aceitável.',
    290.8: 'Fim do plano 41 (EXT ~1445,3): corredor dos mascarados com detritos no chão, em "jaleco branco com fuzil, no corredor". OK.',
    291.4: 'EXT ~1445,9: mascarados no corredor. O trecho 1446,0-1446,7 deixado em aberto pela 2ª revisão não mostra gore. OK.',
    291.8: 'Portas do elevador fechadas (início do plano 42). Sem preto. OK.',
    292.1: 'O elevador abre com um corpo e uma mancha vermelha no chão, visíveis pela fresta, em "e no elevador". Pequeno e ao fundo, e a fala é sobre os mascarados. Baixa.',
    305.5: 'Fim do plano 44: mulher em silhueta no corredor, em "porque o enredo ninguém me entregou". OK.',
    305.9: 'Mulher no corredor rumo à porta da escada. Sem violência. OK.',
    306.3: 'Mulher na porta da escada. OK.',
    306.7: 'Porta FIRE EXIT, escada. OK.',
    307.1: 'Último quadro antes da C17 (EXT ~1462,4): a mulher entra na escada. O "agarrão" de EXT 1463,0 NÃO aparece (corte em 1462,62). R3 confirmado.',
    347.5: 'Plano 50 (EXT ~1537,0): mulher se abaixando junto à barreira amarela em "é gentileza minha". A pistola reaparece de passagem, uma repetição aceitável.',
}
for t, o in y.items():
    m['frames_inspecionados'].append({'timecode': t, 'arquivo_imagem': f'{RF}/frames_extra2/Y_{t:07.2f}.jpg', 'observacao': o})
m['audio_trechos_ouvidos'] += [
    {'inicio': 10, 'fim': 25, 'observacao': N + '"hoje é o dia 9 da série de aquecimento e ontem eu prometi balada, boobieike, terno e pistola silenciada na cobertura, vou entregar quase tudo, uma palavra dessa lista eu conferi no quadro e não baixo [bate] direito, já chego nela". O bloco 1 regerado bate com o roteiro.'},
    {'inicio': 307, 'fim': 348, 'observacao': N + '"Agora, a promessa de ontem. Pistola silenciada na cobertura. Eu fui conferir. A pistola silenciada existe, por volta dos 25 minutos e 37 segundos. Uma pistola com silenciador aparece caída no chão, com o cano cumprido bem visível. O que o vídeo não mostra é quem usou. Nem se foi essa arma dos tiros anteriores... acerto no susto não é fonte. Cobertura também é palpite. O que existe nos quadros é um andar [de] escritório, uma escada com um aviso de acesso ao telhado e um andar em obra com barreira amarela. [Chamar isso de] cobertura..." A versão corrigida (25:37, "andar em obra") é a que está no MP4. O fim do trecho sai embaralhado no ASR porque a janela corta no meio da frase.'},
]
leg = [
    (21.0, 'Uma palavra dessa lista eu conferi', 'Cue 20,02-21,58; ASR da produção: "Uma"@20,02 … "conferi"@21,22. Legenda queimada igual ao SRT no quadro G_0021.00.'),
    (126.1, 'raio caia duas vezes no mesmo', 'Cue 125,60-126,90; ASR: "raio"@125,60, "mesmo"@126,76. Queimada igual (G_0126.10).'),
    (209.5, 'outro de blazer rosa conversando.', 'Cue 208,56-210,08; ASR: "rosa"@209,14, "conversando"@209,44. Em 210,2 cai no intervalo entre cues (210,08-210,82), por isso a amostra foi para 209,5. Queimada igual (G_0209.50).'),
    (294.3, 'Quem são? Não confirmado.', 'Cue 293,86-296,14; ASR: "quem"@293,86, "são"@294,22. Queimada igual (G_0294.30).'),
    (399.4, 'Isso eu coloco na lista de', 'Cue 399,32-401,12; ASR: "Isso"@399,32. Queimada igual (G_0399.40).'),
    (250.0, 'escuro. A Rockstar não legendou, então', 'Cue 248,46-251,12. O texto da legenda está correto; o ASR ouve "Oxstar" (ver problema de pronúncia).'),
    (258.0, 'careca de terno e, no meio', 'Cue 257,82-259,48. Legenda correta e a imagem mostra o careca de terno; o ASR ouve "caraca".'),
    (2.0, 'Vice City pede documento na porta.', 'Cue 0,00-2,40, igual à fala do gancho (ASR "Vice"@0,00). Queimada desde o quadro 0.'),
]
m['legendas']['amostras'] = [{'timecode': t, 'texto': x, 'sincronizado': True, 'observacao': o} for t, x, o in leg]

m['thumbnail'] = {
    'arquivo': f'{EPR}/publicacao/capas/capa_longo_A.jpg',
    'preview_reduzido': f'{RF}/capas/preview_capas_capa_longo_A.jpg',
    'observacao': 'Capa A (1280x720; preview com 640 px de largura): "DINHEIRO / SEM LEI" em branco e amarelo, logo GTA VI inteira e selo PIXEL / PROCURADO. Lê bem em 640 px e em miniatura de celular. A arte é gerada por IA (palco com notas voando), e a descrição avisa. Ela não repete o gancho do título A ("pede documento"), que complementa. A capa B ("PEDE DOCUMENTO" sobre o quadro real da porta ID Check/JOH) é a mais coerente com o título A e com o combinado "só imagem oficial". Incoerência capa A x título registrada como problema média. As capas verticais A/B e o carrossel 01-04 também foram conferidos em preview (revisao_final/capas): legíveis, rodapé 1/4…4/4, "pistola com silenciador … por volta de 25:37" e "Quem usou a pistola… não confirmado" batem com FONTES.',
}

m['problemas'] = [
    {'severidade': 'media', 'timecode': '49-57; 140.3-148.3; 307.3-313.8; 381.3-390.3', 'status': 'aberto',
     'descricao': 'A legenda queimada colide com o texto das cartelas. Em C04, C08 e C17 cobre o rodapé de fonte (URL rockstargames.com/VI/boobie, /VI/vice-city, data de consulta, "Quadro de 25:37 do vídeo oficial…"). Em C21 cobre o 5º item da lista, "Como funciona o ID check". Fontes e item ficam ilegíveis em 4K e no vertical; a promessa de "mostrar a fonte" fica prejudicada. Quadros: frames_cartelas/K_* e prancha_rodapes.jpg.',
     'correcao': 'Refazer C04/C08/C17/C21 com o rodapé e a última linha acima da faixa de legenda (margem inferior ≥ ~30% da altura, ou rodapé no topo) OU suprimir/subir a legenda nos cortes sem_card. Depois re-renderizar longo, vertical e reel (o reel contém a C03/C04) e revalidar só essas janelas.'},
    {'severidade': 'media', 'timecode': None, 'status': 'aberto',
     'descricao': 'A capa A ("DINHEIRO SEM LEI", arte gerada por IA com dançarinas e notas voando) é a capa ligada em publicacao_secao.json ao YouTube longo; a vertical A vai para Short, Instagram integral e Reel. Ela não tem relação com o título A ("Vice City Pede Documento na Porta…") e mostra uma cena que não existe no jogo, num episódio cujo combinado é "só o que a imagem oficial mostra". O aviso na descrição atenua, mas não resolve a coerência capa x título.',
     'correcao': 'Em publicacao_secao.json, trocar capa_longo_A.jpg → capa_longo_B.jpg ("PEDE DOCUMENTO" sobre o quadro real da porta) e capa_vertical_A.jpg → capa_vertical_B.jpg; manter A só como variante de teste. Se trocar, ajustar a frase da descrição sobre a capa A.'},
    {'severidade': 'baixa', 'timecode': '292.1', 'status': 'aceito',
     'descricao': 'Quando o elevador abre ("e no elevador"), aparece de relance pela fresta um corpo com mancha vermelha, pequeno e ao fundo. A fala é sobre os mascarados, não é neutra.',
     'correcao': 'Opcional: plano 42 terminando ~0,3 s antes.'},
    {'severidade': 'baixa', 'timecode': '249.5-250.1; 257.7-258.1', 'status': 'aberto',
     'descricao': 'Possível erro de pronúncia na locução: três ASRs (o small da produção, o small e o medium desta revisão) ouvem "A Oxstar não legendou" em vez de "A Rockstar" e "um caraca de terno" em vez de "um careca". A legenda está correta. Não foi ouvido por humano.',
     'correcao': 'Ouvir 4:09,5-4:10,1 e 4:17,7-4:18,1. Se a troca for audível, regerar só o bloco TTS do par. 13/14 com a mesma voz, reconcatenar, normalizar e revalidar só esse trecho. Se soar natural (R aspirado, vogal átona), aceitar.'},
    {'severidade': 'baixa', 'timecode': '342.8-343.6', 'status': 'aberto',
     'descricao': 'Fala neutra ("e um andar em obra com"): o homem de jaleco branco caído fica em primeiro plano, à esquerda, com gotas de sangue no chão, por ~0,8 s. Não há ato violento: a esganadura e o rosto ensanguentado do R1 foram removidos.',
     'correcao': 'Opcional: plano 52 com inicio 1533.1 (mesmo corte [342.8, 351.08]) ou zoom/recorte à direita sobre a mulher e a barreira. Exige re-render, por isso deixar para uma eventual v3.'},
    {'severidade': 'baixa', 'timecode': '125.8-127.5', 'status': 'aceito',
     'descricao': 'A arte D01 (duas mulheres) entra ainda em "esperam que o raio caia duas vezes", frase sobre as Real Dimez. É uma associação implícita de ~1 s, e o roteiro nega a identificação logo depois (R7 opcional da 2ª revisão).',
     'correcao': 'Opcional: D02 em [122.6, 127.5] e D01 a partir de 127.5.'},
    {'severidade': 'baixa', 'timecode': '222-227', 'status': 'aceito',
     'descricao': 'Em "a imagem só mostra elevador" o plano já está no andar escuro, logo depois do elevador (EXT 21:58).',
     'correcao': 'Opcional: manter o elevador (EXT 21:45-21:55) até ~226,5.'},
    {'severidade': 'baixa', 'timecode': None, 'status': 'aberto',
     'descricao': 'O título A chama o An Extended Look de "Trailer Oficial", mas FONTES e a descrição o tratam como "vídeo oficial". Imprecisão leve de nomenclatura no título (o roteiro também diz "letreiro do trailer").',
     'correcao': 'Trocar no 01_TITULO_A.txt e no publicacao_secao.json: "Vice City Pede Documento na Porta: o Que o Vídeo Oficial Mostra da Noite do GTA 6" (85 caracteres).'},
    {'severidade': 'baixa', 'timecode': None, 'status': 'aberto',
     'descricao': 'A FONTES F5 continua citando "/VI/vice-city e /VI/jason" para a frase do Boobie ("club money … drug money"), sem fixar a página. A cartela C08 e o roteiro dizem página de Vice City (R8 da 2ª revisão, não fechado).',
     'correcao': 'Fixar no F5 de FONTES.md a URL que de fato traz a frase. Não exige mudança no vídeo se for /VI/vice-city.'},
    {'severidade': 'baixa', 'timecode': None, 'status': 'aceito',
     'descricao': 'Os textos "short" (Shorts/Reel/FB curto) e o comentário fixado não citam a contagem. Os demais (descrição, meta_longo, story, carrossel) dizem "terça 17/11, faltam 2 dias para 19/11" corretamente, e o par. 22 diz "quarta, dezoito".',
     'correcao': 'Opcional: acrescentar "Faltam 2 dias para 19/11." ao texto short.'},
    {'severidade': 'baixa', 'timecode': 'story 0.0', 'status': 'aceito',
     'descricao': 'O story começa exatamente no ataque da voz (RMS 0,10 nos primeiros 25 ms, sem pré-rolagem). O ASR ouviu "Amanhã" inteiro, mas pode haver ataque seco.',
     'correcao': 'Nenhuma, salvo se a escuta humana notar clique. Nesse caso, 2-3 frames de fade-in no áudio.'},
]
m['resultado'] = 'aprovado_com_ressalvas'
m['verificacoes_extras'] = {
    'vertical': 'Pixel_Procurado_DIA09_Vertical_V2.mp4 1080x1920, 420,42 s. Quadros em 1, 45, 200, 323, 343,5 e 419,9 s (revisao_final/frames_pecas/V_*): fundo desfocado do próprio plano, sem verde, legenda abaixo do vídeo e card dentro da área útil. Áudio igual ao do longo (correlação 0,955, deslocamento de 43 ms entre os arquivos). O ASR do final dá "...faltam só dois dias.".',
    'reel': 'Pixel_Procurado_DIA09_Reel_V2.mp4 64,30 s. A voz começa em ~0,05 s ("Vice City pede documento na porta"). A última palavra, "fonte.", termina em ~63,74 s e o resto fica em silêncio (RMS 0,001). Quadros em 63,6 e 64,2 s com a legenda "Achar não é fonte." sobre a arte do Jack of Hearts, sem preto. Cartelas REGRAS DE HOJE e TAGLINE legíveis.',
    'story': 'Pixel_Procurado_DIA09_Story_V2.mp4 15,12 s. Começa na voz ("Amanhã, quarta, dezoito de novembro") com a cartela AMANHÃ: DIA 10 / 19 de novembro de 2026. Termina em "dias." (14,70 s), com silêncio nos últimos 0,3 s e quadro limpo (S_0015.05).',
    'textos': 'Título A: 83 caracteres; título B: 66; descrição: 2136 (≤5000). 13 tags, soma ponderada 231 (<400); 04_TAGS.txt igual a tags_youtube. Os 20 capítulos batem com audio/ancoras_paragrafos.json (par. 1-2 em 0:00, par. 18-19 juntos em 5:36 e demais pelo início do parágrafo, com arredondamento para baixo). Pistola com silenciador em 25:37 e "quem usou / cobertura não confirmados" estão alinhados com FONTES. A descrição avisa sobre a capa por IA e a voz sintética. Datas: terça 17/11 e faltam 2 dias para 19/11 estão corretos (17/11/2026 é terça).',
    'fatos_roteiro': 'Os par. 2, 17, 18 e 21 tratam a pistola com silenciador como existente (EXT 25:37, quadro conferido em 322,8-323,5 s) e "cobertura" e "quem usou" como não confirmados. Os textos de Boobie, Dre\'Quan e Real Dimez batem com F1-F4, e a frase noturna com F5.',
    'srt_x_roteiro': 'O texto integral do SRT do longo foi comparado palavra a palavra (difflib, normalizado) com 01_NARRACAO.txt: 1163 = 1163 palavras e zero diferenças.',
    'revisoes_anteriores': 'REVISAO_FOLHAS.md: A1 (pistola sincronizada com a fala), A3 (cidade/piscina/DJ), A4 (sem esganadura), A5 (porta no par. 21), A6 (Lucia/saferoom), B1 (poltrona), B2 (D03 em "Real Dimez são"), B3 (FLOOR 26), B4 (porta em "embaixo do cartaz") e C3 (o plano 31 não abre em preto; a sala de reunião é um plano único) estão fechados no render. C1 (rodapé da C08) agora está inteiro, mas coberto pela legenda (problema média). C4 (movimento dos stills) não foi verificado. REVISAO_FOLHAS_2.md: R1-R6 fechados no render; R7 opcional não aplicado; R8 aberto (baixa).',
    'nao_verificado': 'O áudio não foi ouvido por humano em nenhum trecho, só por ASR e RMS. O vídeo foi conferido por quadros amostrados (82 do longo, 18 das peças), sem assistir em tempo real. Não foram conferidos o picture-in-picture das redes, a capa pública nem a decodificação integral (o validar_v2 da produção registrou 0 pretos).',
}
(EP / 'REVISAO_FINAL.json').write_text(json.dumps(m, ensure_ascii=False, indent=2), encoding='utf-8')
print('ok', len(m['frames_inspecionados']), 'frames')
