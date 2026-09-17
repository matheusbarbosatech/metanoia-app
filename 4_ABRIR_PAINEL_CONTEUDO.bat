@echo off
chcp 65001 > nul
title METANOIA // CONTENT STUDIO & AUTOMAÇÃO DE VÍDEOS
cls
echo =====================================================================
echo    ⚔️  METANOIA // CONTENT STUDIO & AGENDADOR DE REDES SOCIAIS ⚔️
echo =====================================================================
echo.
echo Iniciando servidor integrado da Forja...
echo  - Painel Studio:    http://localhost:8585/studio
echo  - Landing Page:     http://localhost:8585
echo.
echo Abrindo seu navegador automaticamente em 3 segundos...
timeout /t 3 /nobreak > nul
start http://localhost:8585/studio

echo.
echo Servidor ativo. Mantenha esta janela aberta enquanto usa o Studio.
echo Para encerrar, feche esta janela ou pressione Ctrl+C.
echo.

python studio_server.py
