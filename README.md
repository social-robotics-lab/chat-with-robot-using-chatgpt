# chat-with-robot-using-chatgpt
ChatGPTを用いてロボットと雑談するプログラムです。ユーザの音声は自分のPCのマイクで取得し、ロボットの返答はロボットから出力します。

このプログラムを実行する際は、Sotaの中で[RobotControllerを起動](https://github.com/social-robotics-lab/RobotController_bin)しておいてください。

## Install
```
git clone https://github.com/social-robotics-lab/chat-with-robot-using-chatgpt.git
```

srcフォルダの下に.envファイルを作成し、下記のようにOpenAIのAPIキーを入力してください。
```
OPENAI_API_KEY='your api key'
```

## Docker build and run
```
cd chat-with-robot-using-chatgpt
docker compose build
docker compose run --rm app --ip 192.168.11.xxx
```
※SotaのIPアドレスを指定する

## Tips
WSL+Dockerの環境では、WSLがWindowsのマイク入力をPulseAudioを使って取得しています。WSL上でPulseAudioのクライアントは/mnt/wslg/を経由してPulseAudioのサーバに接続されています。Dockerコンテナに/mnt/wslg/をそのままマウントすることで、WSL上で取得されたマイク入力をDockerコンテナに渡すことができます。[参考](https://stackoverflow.com/questions/68310978/playing-sound-in-docker-container-on-wsl-in-windows-11)