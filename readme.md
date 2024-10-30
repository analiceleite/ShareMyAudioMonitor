# 📊 ShareMyAudioMonitor
ShareMyAudioMonitor é um projeto que utiliza Python e Flask para monitorar o volume de som captado pelo microfone do seu computador e compartilhar esses dados em tempo real na rede local (LAN). Com esse projeto, qualquer dispositivo conectado à mesma rede pode acessar uma página web e visualizar o nível de volume do áudio recebido pelo microfone do computador rodando o ShareMyAudioMonitor.
![ShareMyAudioMonitor_print](/utils/image.png)

## 🎯 Objetivo do Projeto
O objetivo é oferecer uma visualização fácil e em tempo real do áudio captado pelo microfone para múltiplos dispositivos conectados à LAN. Esse recurso é especialmente útil em situações como:

- 📡 Monitoramento do volume em ambientes de gravação ou streaming.
- 🎤 Controle remoto para apresentações ou eventos.
- 📱 Acesso remoto em dispositivos sem suporte direto ao monitoramento de áudio.

## 🔧 Tecnologias Utilizadas
- Python 🐍
- Flask 🌐
- Audio Processing Libraries 🎶

## 🚀 Funcionalidades
1. Captura de Áudio 🎙️: Capta o volume do áudio recebido pelo microfone do computador.
2. Disponibilização via Web 🌍: Usa Flask para hospedar uma página web localmente, onde o volume de áudio pode ser visualizado.
3. Acesso LAN 📡: Permite que outros dispositivos conectados à mesma rede local (LAN) possam acessar a visualização em tempo real do áudio.

## ⚙️ Como Funciona
1. O projeto captura o nível de volume do áudio recebido pelo microfone.
2. Os dados de volume são processados e enviados ao servidor Flask.
3. A página web exibe esses dados em tempo real, tornando-os acessíveis para qualquer dispositivo conectado à mesma rede local.

## 🛠️ Como Instalar e Executar

1. Clone o Repositório:
```bash
git clone https://github.com/kmpc2013/ShareMyAudioMonitor.git
```

2. Instale as Dependências:
```bash
pip install -r requirements.txt
```

3. Execute o Projeto:
```bash
python app.py
```

4. Acesse na LAN: No navegador de qualquer dispositivo na mesma rede, acesse o IP do computador na porta definida (por exemplo, http://192.168.0.10:5000).

5. Executar ao iniciar o windows: Caso queira executar o aplicativo toda vez que o windows iniciar, edite o arquivo `run_in_windows.bat` presente no diretório `utils` com o caminho correto do script `app.py` presente em seu computador, então copie o arquivo para o diretório `shell:startup` do windows.

## 💡 Próximos Passos
- Implementação de gráficos históricos para visualização de picos de áudio 📈.
- Opções de configuração de sensibilidade de áudio ⚙️.
- Suporte para autenticação para acesso restrito 🔐.

Contribuições são bem-vindas! 🎉