---
title: anime-audio-translator
app_file: __main__.py
sdk: gradio
sdk_version: 5.32.1
---
## 🎙️ Anime Dialog Translator

Translate Japanese anime audio into English and Filipino (Tagalog) effortlessly.

#### clone the app
```bash
git clone https://github.com/ken-027/anime-dialog-translator
```

### configure environment
fill up ur anthropic api key
``` bash
cp .env.sample .env
```

### setup a virtual environment and activate
```cmd
py -m venv venv && venv\Scripts\activate
```

### install packages
```cmd
py -m pip install -r requirements.txt
```

### install ffmpeg and run this command as administrator
```bash
choco install ffmpeg
```

### run the app
```cmd
py .
```

<br/>

![work1](/screenshots/anime-audio-translator.png)
![work2](/screenshots/anime-audio-translator-2.png)


[Demo](https://huggingface.co/spaces/kenneth-andales/anime-audio-translator)
