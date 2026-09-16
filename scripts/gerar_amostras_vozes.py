"""
Gera amostras de áudio de diferentes vozes neurais para o usuário comparar
"""
import asyncio
import edge_tts
from pathlib import Path

SAMPLE_TEXT = "O que cura um homem ferido de verdade não é a culpa, é o discipulado bíblico completo. Bem-vindo à forja do Metanoia."

VOZES = {
    "1_Antonio_Natural": ("pt-BR-AntonioNeural", "+0Hz", "+0%"),
    "2_Humberto_Natural": ("pt-BR-HumbertoNeural", "+0Hz", "+0%"),
    "3_Fabio_Natural": ("pt-BR-FabioNeural", "+0Hz", "+0%"),
    "4_Donato_Natural": ("pt-BR-DonatoNeural", "+0Hz", "+0%"),
    "5_Nicolau_Natural": ("pt-BR-NicolauNeural", "+0Hz", "+0%"),
    "6_Valerio_Natural": ("pt-BR-ValerioNeural", "+0Hz", "+0%"),
    "7_Manoel_Natural": ("pt-BR-ManoelNeural", "+0Hz", "+0%"),
    "8_Thalita_Multilingual": ("pt-BR-ThalitaMultilingualNeural", "+0Hz", "+0%"),
}

async def generate_samples():
    out_dir = Path("output/amostras_vozes")
    out_dir.mkdir(parents=True, exist_ok=True)
    print("Gerando amostras de vozes neurais (sem distorção artificial)...")
    for name, (voice, pitch, rate) in VOZES.items():
        out_file = out_dir / f"{name}.mp3"
        comm = edge_tts.Communicate(SAMPLE_TEXT, voice, pitch=pitch, rate=rate)
        await comm.save(str(out_file))
        print(f"  [OK] {name} -> {out_file.name}")

if __name__ == "__main__":
    asyncio.run(generate_samples())
