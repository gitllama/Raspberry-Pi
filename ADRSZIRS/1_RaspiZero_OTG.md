# 1. OTGでのRaspberry Pi Zero WH環境構築

## 1.1. Raspberry Pi OSの起動

- [公式](https://www.raspberrypi.org/software/)よりインストーラDL
  - WinsowマシンにSD刺す
  - OSとインストール先を選択しインストール
    - CHOOSE OS : Raspberry Pi OS (32-bit)
    - CHOOSE SD CARD : 対象SDカードドライブ
- SSH設定の有効化
  - SDを一度抜き差ししてWinsowにマウント
  - /boot/config.txt編集
    - ```dtoverlay=dwc2```の追記
  - /boot/cmdline.txt編集
    - rootwait後に``` modules-load=dwc2,g_ether ```(半角スペース必須)
  - sshファイルの作成(boot直下にsshという拡張子ナシ空ファイル
- Windows設定
  - Bonjourをインストール(Firewall udp5353の開放)
  - SD入れRaspberry Piの起動
  - OTG接続(電源ではなくUSB Portの方に接続)
  - COMでマウントしてる場合はUSB RNDIS Gadgetドライバのインスコ
    - デバイスマネージャーから確認、ドライバない場合は下記よりDL
    - [Acer Incorporated. – Other hardware – USB Ethernet/RNDIS Gadget Windows 7,Windows 8,Windows 8.1 and later drivers](https://www.catalog.update.microsoft.com/Search.aspx?q=USB%20RNDIS%20Gadget)
  - Tera Term等でSSH接続確認
    - host : raspberrypi.local
    - user / pass : pi / raspberry

## 1.2. wifi+リモートディスクトップの設定

- wifi確認
  - ```$ sudo iwlist wlan0 scan | grep ESSID```
  - ```$ sudo nano /etc/wpa_supplicant/wpa_supplicant.conf```
    - wifi設定の書込
  - ```$ sudo reboot``` or ```$ sudo halt```
  - ```$ ifconfig```
- アップデート
  - ```$ sudo apt-get update```
  - ```$ sudo apt full-upgrade```
  - ```$ sudo apt clean```
- VNC設定(Windowのリモートディスクトップを使用した接続)
  - ```$ sudo apt-get install tightvncserver``` 必要ないかも
  - ```$ sudo apt-get install xrdp``` : RDPプロトコル
  - ```$ sudo raspi-config```
    - interfaxeing option > VNC > ON : これだけでも動く
 
リモートディスクトップ先につながってるなら、ぜんぶGUIのウィザードで設定してもいいかも。
