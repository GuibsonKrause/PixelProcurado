"""Autochecagem leve da posição dos painéis, sem FFmpeg ou render."""
from produzir_v2 import card_position


def test_card_position():
    long_hd = {"resolucao": [1920, 1080]}
    long_4k = {"resolucao": [3840, 2160]}
    vertical_hd = {"resolucao": [1080, 1920]}
    vertical_4k = {"resolucao": [2160, 3840]}
    assert card_position({}, long_hd) == (58, 730)
    assert card_position({}, long_4k) == (116, 1460)
    assert card_position({}, vertical_hd) == (150, 1060)
    assert card_position({}, vertical_4k) == (300, 2120)
    assert card_position({"card_posicao": [58, 180]}, long_hd) == (58, 180)
    assert card_position({"card_posicao": [58, 180]}, long_4k) == (116, 360)
    assert card_position({"card_posicao": [150, 190]}, vertical_hd) == (150, 190)
    assert card_position({"card_posicao": [150, 190]}, vertical_4k) == (300, 380)
    assert card_position({"card_posicao": [58, 180]}, {"resolucao": [960, 540]}) == (29, 90)
    for invalid in ([], [1], [1, 2, 3], [-1, 2], [True, 2], ["58", 180], [float("inf"), 2]):
        try:
            card_position({"card_posicao": invalid}, long_hd)
        except ValueError:
            pass
        else:
            raise AssertionError(f"posição inválida aceita: {invalid!r}")
    for fmt, position in ((long_hd, [1900, 180]), (long_4k, [58, 1000]),
                          (vertical_hd, [400, 190]), (vertical_4k, [150, 1800])):
        try:
            card_position({"card_posicao": position}, fmt)
        except ValueError:
            pass
        else:
            raise AssertionError(f"painel fora do quadro aceito: {position!r}")


if __name__ == "__main__":
    test_card_position()
    print("OK: fallback, posição explícita, escala horizontal/vertical, entradas inválidas e bounds")
