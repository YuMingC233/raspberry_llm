#!/usr/bin/env python

# recordtest.py
#
# This is an example of a simple sound capture script.
# 这是一个简单的音频捕捉脚本示例。
#
# The script opens an ALSA pcm device for sound capture, sets
# 脚本打开一个用于声音捕捉的ALSA pcm设备，设置
# various attributes of the capture, and reads in a loop,
# 捕捉的各种属性，并在循环中读取，
# writing the data to standard out.
# 并将数据写入标准输出。
#
# To test it out do the following:
# 要测试它，请执行以下操作：
# python recordtest.py out.raw # talk to the microphone (对着麦克风说话)
# aplay -r 8000 -f S16_LE -c 1 out.raw

# !/usr/bin/env python

from __future__ import print_function

import sys
from datetime import datetime
import ssl
import time
import wave
import alsaaudio
import websocket

from gpiozero import Button
from signal import pause

from pydub import AudioSegment

from iat_ws_python3_demo import Ws_Param, on_message, on_error, on_close, on_open

"""
指令错误时的帮助说明
"""

# 声卡上的按钮对应的BCM引脚号
button = Button(17)
# 默认声卡
device = 'default'

"""
录音方法
"""


def recoding():
    global recording_stopped
    global hash_name

    # 使用哈希值作为文件名
    hash_name = hash(time.time()).__str__() + ".wav"

    f = wave.open(hash_name, 'wb')

    # Open the device in nonblocking capture mode. The last argument could
    # 以非阻塞捕捉模式打开设备。最后一个参数也可以是
    # just as well have been zero for blocking mode. Then we could have
    # 零，代表阻塞模式。那样我们就可以不必要
    # left out the sleep call in the bottom of the loop
    # 在循环底部放置sleep调用
    inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NONBLOCK, channels=1, rate=16000,
                        format=alsaaudio.PCM_FORMAT_S16_LE, periodsize=160, device=device)

    f.setnchannels(1)
    f.setsampwidth(2)  # PCM_FORMAT_S16_LE remains the same as it represents 16-bit sample width
    f.setframerate(16000)

    print('%d channels, %d sampling rate\n' % (f.getnchannels(),
                                               f.getframerate()))
    # The period size controls the internal number of frames per period.
    # 周期大小控制每周期的内部帧数。
    # The significance of this parameter is documented in the ALSA api.
    # 这个参数的重要性在ALSA api文档中有说明。
    # For our purposes, it is suficcient to know that reads from the device
    # 对我们来说，只需知道从设备读取
    # will return this many frames. Each frame being 2 bytes long.
    # 将返回这么多帧。每个帧是2字节长。
    # This means that the reads below will return either 320 bytes of data
    # 这意味着下面的读取将返回320字节的数据
    # or 0 bytes of data. The latter is possible because we are in nonblocking
    # 或者0字节的数据。后者是可能的，因为我们处于非阻塞
    # mode.
    # 模式。
    inp.setperiodsize(160)

    while not recording_stopped:
        # Read data from device (设备读取数据)
        l, data = inp.read()

        if l:
            f.writeframes(data)
            time.sleep(.001)

    f.close()


"""
结束录制
"""


def stop_recoding():
    global recording_stopped
    recording_stopped = True
    print("button pressed.")


def convert_to_mp3(wav_filename):
    audio = AudioSegment.from_wav(wav_filename)
    mp3_filename = wav_filename.replace('.wav', '.mp3')
    audio.export(mp3_filename, format='mp3')
    print("转换成功！")
    sys.exit(0)


if __name__ == '__main__':
    # 停止录制标志
    global recording_stopped
    # 录制时自动生成的基于时间的哈希文件名称
    global hash_name

    recording_stopped = False

    # 当按钮被按下时，结束recoding方法
    button.when_pressed = stop_recoding

    recoding()

    # convert_to_mp3(hash_name)

    # print("录音结束，正在推送……")
    # time1 = datetime.now()
    # wsParam = Ws_Param(APPID='518780c2', APISecret='ZGIyNjY4OTY4MDA5ZjQxMWFkY2M5OTAx',
    #                    APIKey='b0782afd1d08c6093ffa6205a400010f',
    #                    AudioFile=hash_name)
    #
    # websocket.enableTrace(False)
    # wsUrl = wsParam.create_url()
    # # 在 '__init__.py' 中找不到引用 'WebSocketApp'
    # ws = websocket.WebSocketApp(wsUrl, on_message=on_message, on_error=on_error, on_close=on_close)
    # ws.on_open = on_open
    # ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
    # time2 = datetime.now()
    # print(time2-time1)

    pause()  # 等待按钮按压事件
