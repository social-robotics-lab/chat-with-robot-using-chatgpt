import argparse
import os
# import openai
from openai import OpenAI
import speech_recognition as sr
import time
from robottools import RobotTools
from dotenv import load_dotenv

parse = argparse.ArgumentParser()
parse.add_argument('--ip', required=True)
parse.add_argument('--port', default=22222, type=int)
args = parse.parse_args()

load_dotenv()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
model_engine = 'gpt-3.5-turbo-1106'

rt = RobotTools(args.ip, args.port)

# 音声認識器を作成
r = sr.Recognizer()

# ChatGPTへのリクエストに含めるパラメータ
params = [
    {'role': 'system', 'content': 'あなたはユーザーの雑談相手です。'}
]

# マイクから音声を連続認識
with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source)  # ノイズ対策（オプション）
    while True:
        print('USER: ', end='')
        # 音声読み込み
        audio = r.listen(source)
        t0 = time.time()
        try:
            user_input = r.recognize_google(audio, language='ja-JP')
            params.append({'role': 'user', 'content': user_input})
            print(user_input)
        except sr.UnknownValueError:
            print('\nGoogle Speech Recognition could not understand audio')
            continue
        except sr.RequestError as e:
            print('\nCould not request results from Google Speech Recognition service; {0}'.format(e))
            continue

        # 応答生成
        print('ROBOT: ', end='')
        response = client.chat.completions.create(
            model=model_engine,
            messages=params
        )
        message = response.choices[0].message.content
        params.append({'role': 'assistant', 'content': message})
        print(message)

        # ロボットに生成された応答を送信
        d = rt.say_text(message)
        m = rt.make_beat_motion(d, speed=1.5)
        rt.play_motion(m)

        # 発話中は音声認識を止める
        time.sleep(d)
        
        # ユーザ発話の録音完了からロボット発話の再生完了までPulseAudioのサーバに溜まったデータを削除
        r.record(source, time.time() - t0)
        if user_input.startswith('終了'): break