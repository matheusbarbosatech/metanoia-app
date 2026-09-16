@echo off
title METANOIA - Transcricao de Videoaulas Especialistax (Deepgram Nova-2)
echo =========================================================================
echo    METANOIA - Extracao e Transcricao de Videoaulas (#especialistax)
echo =========================================================================
echo Iniciando pipeline de audio FFmpeg + Deepgram Nova-2...
cd /d "%~dp0"
python scripts\transcrever_especialistax.py
pause
