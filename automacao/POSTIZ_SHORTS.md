# Rotina Postiz — Pixel Procurado

Esta rotina usa o Postiz local em `http://localhost:4007` e a CLI oficial do
Postiz. Ela não publica nada por padrão.

## Segurança do fluxo

- `plan`: valida vídeos, títulos, descrições, tags e capas; não envia arquivos.
- `check`: testa a chave e localiza o canal conectado.
- `draft`: envia os arquivos somente ao Postiz local e cria rascunhos.
- `schedule`: cria agendamentos que poderão chegar ao YouTube. Exige a trava
  adicional `--confirm-youtube`.
- `replace-schedule`: envia a nova mídia, cria o novo agendamento e só então
  remove o rascunho antigo registrado para o mesmo ID e horário. Exige
  `--confirm-youtube` e `--confirm-replace`.
- Se já houver um rascunho com a mesma data, `schedule` promove esse rascunho
  sem reenviar o vídeo. Uma data diferente é recusada para evitar surpresas.
- O estado fica em `producao/shorts/POSTIZ_ESTADO.json`, ignorado pelo Git. Isso
  impede upload ou criação duplicada quando um comando é retomado.
- A visibilidade padrão é `não listado`. Publicação pública exige também
  `--visibility public --confirm-public`.

## Configuração local

Nesta máquina, `POSTIZ_API_KEY` e `POSTIZ_API_URL` já estão gravadas como
variáveis do usuário do Windows. O arquivo abaixo é apenas uma alternativa
portátil para outra máquina.

Crie o arquivo ignorado `.env.postiz.local` na raiz:

```text
POSTIZ_API_URL=http://localhost:4007/api
POSTIZ_API_KEY=SUA_CHAVE_LOCAL
```

Não envie esse arquivo ao Git nem compartilhe a chave.

## Uso

Validar a fila principal, sem datas:

```powershell
python .\automacao\postiz_shorts.py plan
```

Visualizar uma hipótese de agenda, sem criar posts:

```powershell
python .\automacao\postiz_shorts.py plan --start 2026-11-02T19:00 --interval-days 2
```

Testar Postiz e canal:

```powershell
python .\automacao\postiz_shorts.py check
```

Criar um único rascunho local para revisão:

```powershell
python .\automacao\postiz_shorts.py draft --ids C03 --start 2026-11-02T19:00
```

O comando `schedule` só deve ser usado depois de confirmar datas, ordem,
visibilidade e o resultado do primeiro rascunho. As reservas `L01-R02` e
`L01-R03` não entram na fila principal, a menos que seja usado
`--include-reserves` ou `--ids`.

O comentário fixado permanece no arquivo `03_COMENTARIO_FIXADO.txt`: o Postiz
agenda o vídeo, mas fixar um comentário é uma ação posterior no YouTube.

## Substituir um rascunho antigo e publicar no horário preservado

Use somente depois que a nova mídia e seu pacote tiverem sido validados:

```powershell
python .\automacao\postiz_shorts.py replace-schedule --ids C03 `
  --start 2026-11-02T19:00 --confirm-youtube --confirm-replace `
  --visibility public --confirm-public
```

A rotina cria o novo agendamento antes de remover o rascunho antigo. A data
precisa coincidir com a registrada em `POSTIZ_ESTADO.json`.
