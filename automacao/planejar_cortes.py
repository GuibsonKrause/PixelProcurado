import json
import subprocess
import os

with open("producao/starlink/whisper_exato.json", "r", encoding="utf-8") as f:
    words_data = json.load(f)

# Let's inspect the exact segments and identify silence gaps
print(f"Total whisper segments: {len(words_data)}")

# Planned cut points:
# Cut 1: 0.00 to 10.30 (Hook + Planos residenciais)
# Cut 2: 11.10 to 28.50 (Plano Max)
# Cut 3: 29.20 to 39.60 (Plano 100 mega)
# Cut 4: 40.50 to 51.20 (Plano Viagem 100GB)
# Cut 5: 51.80 to 64.70 (Plano Viagem Ilimitado)
# Cut 6: 64.70 to 86.80 (Abaixou muito, regras ate 30 nov, instalacao garantida)
# Cut 7: 115.60 to 122.60 (Se voce comprar comigo ganha 200 reais de credito)
# Cut 8: 138.70 to 141.20 (Entra em contato agora mesmo!)

cuts = [
    (0.00, 10.30, "Hook + Intro residenciais"),
    (11.10, 28.60, "Plano Max"),
    (29.10, 39.60, "Plano 100 Mega residencial"),
    (40.40, 51.20, "Plano Viagem 100GB"),
    (51.80, 64.80, "Plano Viagem Ilimitado"),
    (64.80, 86.80, "Regras da promo + instalacao garantida"),
    (115.60, 122.60, "Bonus 200 reais de credito"),
    (138.60, 141.20, "CTA Final")
]

total_dur = sum(c[1] - c[0] for c in cuts)
print(f"\nPlanned cuts total duration: {total_dur:.2f} seconds (Max allowed: 90s)")
for i, c in enumerate(cuts):
    print(f"  Clip {i+1}: {c[0]:6.2f}s -> {c[1]:6.2f}s ({c[1]-c[0]:.2f}s) - {c[2]}")
