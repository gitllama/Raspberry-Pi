# 2. 開発環境の設定

## 2.1. i2cの設定

- i2cの設定
  - GUIかCUIの```$ sudo raspi-config```起動
  - Interfacing Options > P5 I2C > ON

## 2.2. pythonの設定

## 2.3. Rustの設定

- RustのInstall
  - ```$ curl https://sh.rustup.rs -sSf | sh```
    - Proceed with installation (default)
  - ```$ rustc --version```
  - ```$ cargo --version```
  - ```$ sudo apt install -y libssl-dev``` : (cargo-editに必要？)
  - ```$ sudo apt install -y pkg-config```
  - ```$ cargo install cargo-edit``` : cargoのコマンドが使えるように
  - cargo-make 
    - ```$ git clone https://github.com/sagiegurari/cargo-make.git```
    - ```$ cd cargo-make```
    - ```$ cargo install --force cargo-make```
  - ```$ rustup update```
- プロジェクトの作成
  - $ cargo new [name] --bin
- debug run
  - $ cargo run
  - $ cargo run -- -h : コマンドラインのデバッグ

## 2.4. サーバーの設定

express + PM2を使用

- インストール
  - ```$ sudo apt install nodejs npm```
  - ```$ sudo npm install express-generator -g```
  - ```$ npm i -g pm2```
- テンプレートの生成
  - ```$ express --view=ejs``` : ejsテンプレートの場合
- appのrun(ターミナルが落ちると終了)
  - ```DEBUG=pircsv:* npm start```
  - http://raspberrypi.local:3000/で接続
- pm2でプロセスの実行(別プロセスで実行), 終了
  - ```$ pm2 start [app.json] --name [name]```
  - ```$ pm2 start [app.json] --name [name] --env production```
  - ```$ pm2 list```
  - ```$ pm2 stop app```
- pm2で自動起動のスクリプトを作成
  - ```$ pm2 startup```
  - 指定されたコマンドの実行
    - 例) ```sudo env PATH=$PATH:/usr/local/bin /usr/local/lib/node_modules/pm2/bin/pm2 startup systemd -u pi --hp /home/pi```
  - ```$ pm2 save```
　- ```$ reboot```
