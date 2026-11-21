p = r"C:\Users\guibson.krause\Documents\ChatGPT\Postiz\docker-compose.yaml"
with open(p, "r", encoding="utf-8") as f:
    text = f.read()

target = "./overrides/facebook-video-once.js:/app/apps/orchestrator/dist/libraries/nestjs-libraries/src/integrations/social/facebook-video-once.js:ro"
replacement = (
    target + "\n"
    "      - ./overrides/tiktok.provider.js:/app/apps/backend/dist/libraries/nestjs-libraries/src/integrations/social/tiktok.provider.js:ro\n"
    "      - ./overrides/tiktok.provider.js:/app/apps/orchestrator/dist/libraries/nestjs-libraries/src/integrations/social/tiktok.provider.js:ro"
)

if target in text and "tiktok.provider.js" not in text:
    text = text.replace(target, replacement)
    with open(p, "w", encoding="utf-8") as f:
        f.write(text)
    print("Sucesso: tiktok.provider.js montado no docker-compose.yaml!")
else:
    print("Ja existia ou target nao encontrado.")
