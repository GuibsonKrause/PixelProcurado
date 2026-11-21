"""Self-check local; não consulta API nem envia mídia."""
import distribuir_l05_postiz as s

assert len(s.FILES) == 5
assert s.WHEN.isoformat() == '2026-11-03T12:00:00-03:00'
assert s.FILES['instagram_story'] == s.FILES['facebook_story']
assert len(s.CAPTION) <= 2200
original = s.read
s.read = lambda path: {'01_TITULO.txt':'GTA V e GTA VI: olhe ao redor','02_DESCRICAO.txt':'Descrição de teste','04_TAGS.txt':'GTAV,GTAVI'}[path.name]
try:
    for name in s.FILES:
        result = s.payload(name, {'id':'video','path':'https://example.org/video.mp4'}, {'id':'cover','path':'https://example.org/cover.jpg'})
        post = result['posts'][0]
        provider,kind = name.split('_')
        assert result['type']=='schedule' and result['date']==s.WHEN.isoformat()
        assert post['integration']['id']==s.CHANNELS[provider]
        assert len(post['value'][0]['image'])==1
        assert post['settings']['__type']==provider
        if provider=='youtube': assert post['settings']['type']=='public'
        else: assert post['settings']['post_type']==('story' if kind=='story' else 'post')
finally:
    s.read = original
print('PASS: cinco destinos, data fixa, schema mínimo, caption e single-media Stories.')
