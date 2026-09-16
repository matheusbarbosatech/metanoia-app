@echo off
chcp 65001 > nul
title GERADOR DE VÍDEOS VIRAIS // METANOIA IA
cls
echo =====================================================================
echo    ⚔️  GERADOR AUTOMÁTICO DE VÍDEOS VIRAIS COM IA // METANOIA ⚔️
echo =====================================================================
echo.
echo Este script gera vídeos verticais (1080x1920) 100%% prontos para:
echo  - TikTok
echo  - Instagram Reels
echo  - YouTube Shorts
echo.
echo Recursos inclusos:
echo  * Locução neural masculina grave (pt-BR-AntonioNeural) - 100%% Grátis
echo  * Legendas dinâmicas amarelas sincronizadas na tela
echo  * Header oficial METANOIA // FORJA DE 90 DIAS
echo  * Fundo Dark Obsidian ou seus vídeos da pasta 'assets\videos_fundo'
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
