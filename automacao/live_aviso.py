"""Avisos do fluxo de live: AVISOS.md + notificacao do Windows + webhook opcional (LIVE_WEBHOOK_URL).

  from live_aviso import avisar; avisar("Clipe aguardando aprovacao", "t3_000020 nota 82", "acao")
  py -3.12 automacao/live_aviso.py "titulo" "mensagem" [info|acao|erro]
"""
import json, os, subprocess, sys, urllib.request
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOG = ROOT / "producao" / "live" / "AVISOS.md"
ICONE = {"info": "i", "acao": "!", "erro": "x"}
TOAST = r"""
[Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
$x = [Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent('ToastText02')
$n = $x.GetElementsByTagName('text')
$n.Item(0).AppendChild($x.CreateTextNode($env:AVISO_T)) | Out-Null
$n.Item(1).AppendChild($x.CreateTextNode($env:AVISO_M)) | Out-Null
$app = '{1AC14E77-02E7-4E5D-B744-2EB1AE5198B7}\WindowsPowerShell\v1.0\powershell.exe'
[Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier($app).Show([Windows.UI.Notifications.ToastNotification]::new($x))
"""


def avisar(titulo, msg="", nivel="info"):
    try:
        LOG.parent.mkdir(parents=True, exist_ok=True)
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(f"- {datetime.now():%d/%m %H:%M:%S} [{ICONE.get(nivel, 'i')}] **{titulo}** {msg}\n")
    except OSError:
        pass
    print(f"[aviso:{nivel}] {titulo} {msg}", flush=True)
    if os.name == "nt":
        try:
            subprocess.Popen(["powershell", "-NoProfile", "-NonInteractive", "-Command", TOAST],
                             env={**os.environ, "AVISO_T": titulo[:80], "AVISO_M": msg[:160]},
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except OSError:
            pass
    url = os.environ.get("LIVE_WEBHOOK_URL")
    if url:
        try:
            req = urllib.request.Request(url, data=json.dumps({"content": f"**{titulo}** {msg}"}).encode(),
                                         headers={"Content-Type": "application/json"})
            urllib.request.urlopen(req, timeout=10).read()
        except Exception:
            pass


if __name__ == "__main__":
    avisar(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "", sys.argv[3] if len(sys.argv) > 3 else "info")
