@echo off
chcp 65001 > nul
title GERADOR DE VÍDEOS VIRAIS // METANOIA IA
cls
echo =====================================================================
echo    ⚔️  GERADOR AUTOMÁTICO DE VÍDEOS VIRAIS COM IA // METANOIA ⚔️
echo =====================================================================
echo.
echo Este pipeline cinematográfico gera vídeos verticais (1080x1920):
echo  - TikTok
echo  - Instagram Reels
echo  - YouTube Shorts
echo.
echo Recursos integrados de alta retenção:
echo  * Cortes Dinâmicos a cada 2.5s (Faíscas, Guerreiro, Bigorna, Tempestade, Chamas)
echo  * Trilha Sonora Épica de Cinema (Orquestra + Tambores de Guerra)
echo  * Vozes Neurais Gratuitas (Duarte Épico, Francisca Firme, Brian Multilingual, etc.)
echo  * Suporte a Áudio Próprio (Grave no WhatsApp/celular e coloque na pasta 'input_audio')
echo  * Legendas Dinâmicas Amarelas de Alto Impacto + Header Oficial
echo.
echo =====================================================================
echo.

python scripts\gerador_videos_metanoia.py

echo.
echo Abrindo a pasta de vídeos gerados...
explorer output
echo.
echo Pressione qualquer tecla para fechar...
pause > nul
