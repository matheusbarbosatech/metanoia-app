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
echo Recursos integrados:
echo  * Banco de Vídeos Cinemáticos: Pexels API + Pixabay API integrados (.env)
echo  * Vozes Neurais Naturais: Antonio (PT-BR), Francisca (PT-BR), Duarte (PT-PT)
echo  * Legendas dinâmicas amarelas sincronizadas com contorno preto
echo  * Header oficial METANOIA // FORJA DE 90 DIAS
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
