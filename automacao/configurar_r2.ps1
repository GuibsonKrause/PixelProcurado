$ErrorActionPreference = 'Stop'

py -3.12 -c 'import boto3'
if ($LASTEXITCODE -ne 0) { throw 'Execute: py -3.12 -m pip install --user boto3' }

$endpoint = (Read-Host 'S3 endpoint da Cloudflare').Trim().TrimEnd('/')
if ($endpoint -notmatch '^https://[0-9a-f]{32}\.r2\.cloudflarestorage\.com$') {
    throw 'Informe o endereco HTTPS indicado como S3 endpoint na tela do token.'
}
$accessKey = (Read-Host 'Access Key ID').Trim()
$secret = Read-Host 'Secret Access Key (entrada oculta)' -AsSecureString
if (-not $accessKey -or $secret.Length -eq 0) { throw 'Preencha as duas chaves.' }
$credential = [pscredential]::new($accessKey, $secret)

try {
    $env:PIXEL_R2_ENDPOINT = $endpoint
    $env:PIXEL_R2_ACCESS_KEY = $accessKey
    $env:PIXEL_R2_SECRET_KEY = $credential.GetNetworkCredential().Password.Trim()
    @'
import os
from urllib.request import urlopen
from uuid import uuid4

import boto3
from botocore.config import Config

bucket = 'pixel-procurado-publicacoes'
key = f'testes/conexao-{uuid4().hex}.txt'
body = b'Pixel Procurado - teste de conexao R2\n'
client = boto3.client(
    's3',
    endpoint_url=os.environ['PIXEL_R2_ENDPOINT'],
    aws_access_key_id=os.environ['PIXEL_R2_ACCESS_KEY'],
    aws_secret_access_key=os.environ['PIXEL_R2_SECRET_KEY'],
    region_name='auto',
    config=Config(signature_version='s3v4', connect_timeout=10, read_timeout=20),
)

def check():
    client.put_object(Bucket=bucket, Key=key, Body=body, ContentType='text/plain')
    try:
        url = client.generate_presigned_url(
            'get_object', Params={'Bucket': bucket, 'Key': key}, ExpiresIn=300
        )
        with urlopen(url, timeout=20) as response:
            if response.read(len(body) + 1) != body:
                raise ValueError('Conteudo recebido difere do original')
    finally:
        client.delete_object(Bucket=bucket, Key=key)

try:
    check()
except Exception as exc:
    code = getattr(exc, 'response', {}).get('Error', {}).get('Code')
    print('Falha no teste R2:', type(exc).__name__, code or '')
    raise SystemExit(1) from None
'@ | py -3.12 -
    if ($LASTEXITCODE -ne 0) { throw 'O teste falhou. As novas credenciais nao foram salvas.' }
} finally {
    Remove-Item Env:PIXEL_R2_ENDPOINT, Env:PIXEL_R2_ACCESS_KEY, Env:PIXEL_R2_SECRET_KEY -ErrorAction SilentlyContinue
}

$configDir = Join-Path $env:LOCALAPPDATA 'PixelProcurado'
New-Item -ItemType Directory -Path $configDir -Force | Out-Null
[pscustomobject]@{ Endpoint = $endpoint; Credential = $credential } |
    Export-Clixml -LiteralPath (Join-Path $configDir 'r2.xml')
Write-Host 'R2 OK: upload, link temporario e exclusao validados. Credenciais salvas no perfil do Windows.'
