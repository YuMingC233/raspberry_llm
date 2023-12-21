# 基于树莓派与音频hat的大语言模型应用

### 硬件信息

[raspberry pi zero 2 wh](https://datasheets.raspberrypi.com/rpizero2/raspberry-pi-zero-2-w-product-brief.pdf?_gl=1*1o10b0z*_ga*MTc1MTQ2NzkxMS4xNzAyOTY4NDg5*_ga_22FD70LWDS*MTcwMzE0NzQyMS4xLjEuMTcwMzE0NzQ0NS4wLjAuMA..)

[WM8960 Audio HAT](https://www.waveshare.com/wiki/WM8960_Audio_HAT)

一台能够科学上网的android手机与能连wifi的PC or Laptop

### 部署

1. 参考[此文档](https://www.yiboard.com/thread-1770-1-1.html)物理初始化树莓派
    1. 如果严格按照上面的文段操作后，将hdmi插入显示器时出现彩虹屏幕，请检查刷入的系统位数是否与树莓派的处理器位数对应。
        
        ![Untitled](static/readme/Untitled.png)
        
    2. 请根据业务与树莓派自身体质**慎重思考**是否选用带有桌面的系统。
    3. 下面的内容将假定您选用了下面的系统，以及在接下来的cutsom setting中设定了用户名、密码，**手机热点**的wifi名称与密码。
        
        ![Untitled](static/readme/Untitled%201.png)
        
2. 让树莓派科学上网
    1. 手机打开sufboard，点选右上角三个点→设置→覆盖。打开覆盖局域网共享后，下方将会弹出提示“需要重启”，点选重启后回到首页。您再启动之后将会在仪表盘中看到“本地代理”，表示已经成功开启了局域网的节点共享。（其他app同理）
        
        ![Untitled](static/readme/Untitled%202.png)
        
    2. 打开手机热点与树莓派后，进入树莓派终端后`apt-get update` ，只需确认有数据交互即可，确保树莓派连接上了wifi。
    3. `sudo nano ~/.bashrc` 在该文件的最底端写入：
        
        ```bash
        alias unsetproxy="unset https_proxy && unset http_proxy"
        alias setproxy="export https_proxy=http://sufboard中在本地代理中给出的http ip地址:1234 && export http_proxy=http://同上:1234"
        ```
        
        `ctrl+o` 保存，回车确定后 `ctrl+x` 退出。
        
    4. 执行`sudo source ~/.bashrc` ，接着执行`setproxy` 即可。
3. 安装pyenv，方便管理多版本的python。
    
    [****linux ubuntu 安装多版本 python****](https://www.notion.so/linux-ubuntu-python-4996df5eab774dc295be5a490dfc9df1?pvs=21)
    
    注意，因为本树莓派的内存实在太小 **(512M)**，我尝试执行了许多遍 `pyenv install 3.8` ，以及按照下面的步骤设置了swap空间，在很多次的**过热自动重启**（注意散热）以及**重试**后，它装上了😭。
    
    [linux 设置swap空间以增加小内存缓存](https://www.notion.so/linux-swap-277b27d0c81b4c398b62a478c3fef542?pvs=21)
    
4. 将声卡HAT扣到树莓派的排针上，并重启树莓派。*别把针脚扣坏了*
5. 参照该文档[安装驱动](https://www.waveshare.com/wiki/WM8960_Audio_HAT)以及测试即可。
    1. 在文档的****Install Driver****部分，执行 `sudo ./install.sh` 时，可能会出现：
        
        ```
        Error! Your kernel headers for kernel xxx cannot be found.
        Please install the linux-headers-xxx-xxx package,
        or use the --kernelsourcedir option to tell DKMS where it's located
        ```
        
        要解决这个问题，你需要安装与你当前运行的内核版本相对应的内核头文件。可以使用以下命令安装内核头文件：
        
        ```bash
        sudo apt update
        sudo apt install raspberrypi-kernel-headers
        ```
        
        安装完毕后，重新运行**`sudo ./install.sh`**脚本应该能够编译并安装WM8960声卡驱动。
        
        **在Linux环境下安装驱动时请务必注意，任何错误都将导致硬件无法正常使用。请谨慎对待任何不寻常的log。**
        
    2. 在文档的****Examples****部分，执行 `sudo python3 setup.py build` 时，可能会出现：
        
        ```python
        alsaaudio.c:14:10: fatal error: Python.h: No such file or directory
           14 | #include "Python.h"
              |          ^~~~~~~~~~
        compilation terminated.
        ```
        
        这个错误信息表明你的系统中缺少Python开发头文件。如果你使用的是Python 3（从你的命令 **`sudo python3 setup.py build`** 来看），你可以通过运行以下命令来安装Python 3开发包：
        
        ```bash
        sudo apt-get update
        sudo apt-get install python3-dev
        ```
        
        安装完成后，重新尝试执行build命令。这应该能够解决编译错误。
        
    3. 同样的部分，在执行 `sudo python [playwav.py](http://playwav.py/) music.wav` 时，可能会出现：
        
        ```python
        Traceback (most recent call last):
          File "/home/hnjd/download/WM8960_Audio_HAT_Code/playwav.py", line 10, in <module>
            import alsaaudio
        ModuleNotFoundError: No module named 'alsaaudio'
        ```
        
        如果在上面的 `Install ibraries` 步骤中并没有成功安装该库时，就会出现这个错误。你可以简单的执行下面的这个命令：
        
        ```bash
        sudo pip3 install pyalsaaudio
        ```
       
        即可。


### 常用命令

- 播放音频
aplay xxx.wav
- 录制音频
arecord -f S32_LE -r 16000 -c 2 test.wav
- 实时监听
arecord -f cd | sudo arecord -f cd | aplay