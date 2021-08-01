# 2. 開発環境の設定

## 2.1. i2cの設定

- i2cの設定
  - GUIかCUIの```$ sudo raspi-config```起動
  - Interfacing Options > P5 I2C > ON

## 2.2. pythonの設定

## 2.3. Rustの設定

- RustのInstall
  - $ curl https://sh.rustup.rs -sSf | sh
    - Proceed with installation (default)
  - $ rustc --version
  - $ cargo --version
  - $ sudo apt install -y libssl-dev : (cargo-editに必要？)
  - $ sudo apt install -y pkg-config
  - $ cargo install cargo-edit : cargoのコマンドが使えるように
  - cargo-make 
    - $ git clone https://github.com/sagiegurari/cargo-make.git
    - $ cd cargo-make
    - $ cargo install --force cargo-make
  - $ rustup update
- プロジェクトの作成
  - $ cargo new [name] --bin
- debug run
  - $ cargo run
  - $ cargo run -- -h : コマンドラインのデバッグ
