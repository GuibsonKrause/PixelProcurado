$ErrorActionPreference = 'Stop'

$secureKey = Read-Host 'Cole sua GEMINI_API_KEY (a entrada ficara oculta)' -AsSecureString
$pointer = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secureKey)
try {
    $plainKey = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($pointer)
    if ([string]::IsNullOrWhiteSpace($plainKey)) {
        throw 'A chave nao pode ficar vazia.'
    }
    [Environment]::SetEnvironmentVariable('GEMINI_API_KEY', $plainKey, 'User')
    $env:GEMINI_API_KEY = $plainKey
    Write-Host 'GEMINI_API_KEY salva no perfil do Windows. A chave nao foi gravada no projeto.'
}
finally {
    if ($pointer -ne [IntPtr]::Zero) {
        [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($pointer)
    }
    $plainKey = $null
}
