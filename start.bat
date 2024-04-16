@echo off

set PYTHON=
set GIT=
set VENV_DIR=
set COMMANDLINE_ARGS=--xformers --medvram --api --port=7861

cd stable-diffusion-webui

start webui.bat

cd ../

call stable-diffusion-webui\venv\Scripts\activate.bat

python gradio_ui.py

pause