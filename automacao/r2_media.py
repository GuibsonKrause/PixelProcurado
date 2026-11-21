"""Temporary media for Postiz's Meta integrations."""

import json
import mimetypes
import re
import subprocess
from pathlib import Path
from time import time
from uuid import uuid4


BUCKET = 'pixel-procurado-publicacoes'
CONFIG = Path(__file__).resolve().parents[1] / '.production-tools' / 'postiz-r2.json'
MEDIA_KEY = re.compile(r'publicacoes/[0-9a-f]{32}\.(mp4|jpg|jpeg|png|webp)')


class R2Media:
    def __init__(self, worker_url=None):
        import boto3
        from botocore.config import Config

        self.worker_url = (worker_url or json.loads(CONFIG.read_text(encoding='utf-8'))['url']).rstrip('/')
        if not re.fullmatch(r'https://pixel-procurado-midia\.[a-z0-9-]+\.workers\.dev', self.worker_url):
            raise ValueError('Endereço do Worker inválido.')
        result = subprocess.run(
            ['powershell', '-NoProfile', '-NonInteractive', '-Command',
             "$ErrorActionPreference = 'Stop'; "
             "$cfg = Import-Clixml -LiteralPath (Join-Path $env:LOCALAPPDATA 'PixelProcurado/r2.xml'); "
             "@{ endpoint = $cfg.Endpoint; access = $cfg.Credential.UserName; "
             "secret = $cfg.Credential.GetNetworkCredential().Password.Trim() } | ConvertTo-Json -Compress"],
            capture_output=True, text=True, timeout=45,
        )
        if result.returncode:
            raise RuntimeError('Não foi possível abrir as credenciais R2 do perfil do Windows.')
        credentials = json.loads(result.stdout)
        if not re.fullmatch(r'https://[0-9a-f]{32}\.r2\.cloudflarestorage\.com', credentials['endpoint']):
            raise ValueError('Endpoint R2 inválido.')
        self.client = boto3.client(
            's3', endpoint_url=credentials['endpoint'], region_name='auto',
            aws_access_key_id=credentials['access'], aws_secret_access_key=credentials['secret'],
            config=Config(signature_version='s3v4', connect_timeout=10, read_timeout=30,
                          request_checksum_calculation='when_required'),
        )

    def stage(self, path, key=None, available_until=None, transfer_config=None, copy_from=None):
        path = Path(path)
        key = key or f'publicacoes/{uuid4().hex}{path.suffix.lower()}'
        if not MEDIA_KEY.fullmatch(key) or not key.endswith(path.suffix.lower()):
            raise ValueError('Tipo de mídia R2 inválido.')
        content_type = mimetypes.guess_type(path.name)[0]
        size = path.stat().st_size
        if not size:
            raise ValueError('Arquivo de mídia vazio.')
        expires_at = int(available_until.timestamp() if available_until else time() + 7 * 86400)
        if expires_at <= time():
            raise ValueError('A validade da mídia precisa estar no futuro.')
        url = f'{self.worker_url}/{key}'
        try:
            if copy_from:
                if not MEDIA_KEY.fullmatch(copy_from) or copy_from == key:
                    raise ValueError('Origem de cópia R2 inválida.')
                self.client.copy_object(
                    Bucket=BUCKET, Key=key, CopySource={'Bucket': BUCKET, 'Key': copy_from},
                    ContentType=content_type, MetadataDirective='REPLACE',
                    Metadata={'expires-at': str(expires_at * 1000)},
                )
            else:
                self.client.upload_file(
                    str(path), BUCKET, key,
                    Config=transfer_config,
                    ExtraArgs={'ContentType': content_type,
                               'Metadata': {'expires-at': str(expires_at * 1000)}},
                )
            with path.open('rb') as local:
                prefix = local.read(256)
            result = subprocess.run(
                ['node', '-e', """
const { url, type, size, prefix } = JSON.parse(require('fs').readFileSync(0, 'utf8'));
const last = Buffer.from(prefix, 'hex').length - 1;
fetch(url, { headers: { Range: `bytes=0-${last}` }, signal: AbortSignal.timeout(20000) })
  .then(async response => {
    if (response.status !== 206 || response.headers.get('content-type') !== type ||
        response.headers.get('content-range') !== `bytes 0-${last}/${size}` ||
        Buffer.from(await response.arrayBuffer()).toString('hex') !== prefix) process.exitCode = 1;
  }).catch(() => { process.exitCode = 1; });
"""],
                input=json.dumps({'url': url, 'type': content_type, 'size': size, 'prefix': prefix.hex()}),
                text=True, capture_output=True, timeout=45,
            )
            if result.returncode:
                raise ValueError('O Worker não devolveu os bytes esperados para a mídia.')
        except Exception:
            self.remove(key)
            raise
        return {'id': '', 'path': url}, key

    def remove(self, key):
        if not MEDIA_KEY.fullmatch(key):
            raise ValueError('Chave de mídia R2 inválida.')
        self.client.delete_object(Bucket=BUCKET, Key=key)
