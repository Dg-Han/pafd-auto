# pafd-auto
自动填写pafd（ver 202203）<br>
>电脑端自动调用wx进行填写，大致用时1min，适合在洗漱打水摸鱼但电脑闲置时使用<br>

`pafd.py`和`pafd_ui.py`中均包含模板识别和特征识别两种图像识别方法，可根据自身需求修改选取其中任一方法

---
2022.03.13更新<br>
`pafd_ui.py`为上版本未开发完全的带UI版本<br>
>图片识别方法为pyautogui中locateCenterOnScreen函数，因此仅支持原图匹配，如无法识别图片需考虑重新截取`Photos`文件夹中的目标图片，以解决不同分辨率及缩放可能带来的问题<br>

---
`pafd.py`为源码<br>
>当前版本（20220309）使用cv2中sift特征识别方法识别图像<br>

`Photos`文件夹为使用图片库，运行源码前需保证该文件夹及其内容与源码在同一路径下<br>
`config.bat`为Python第三方库配置文件，运行前需确保系统环境变量中包含python路径<br>

