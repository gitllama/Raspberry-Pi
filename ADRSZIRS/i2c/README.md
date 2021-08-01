# ADRSZIRS サンプルプログラム

- 3_2adrszIRS-sample.py : ビット・トレード・ワンオリジナル
- adrszirs.py : Pyhtonでの一部書き換え
- rust_i2c : Rustでの書き換え

## 実行方法

```bash
# 読み取り
$ python3 ./3_2adrszIRS-sample.py r

# 書き込み
$ python3 ./3_2adrszIRS-sample.py w [code] 
```

### I2C関係内部コマンド

|コマンド名|番号|機能|
|:-|:-:|:-:|
|R1_log_start|0x15|赤外線記録 開始|
|R2_log_stop|0x25|赤外線記録 停止|
|R3_data_num_read|0x35|赤外線コード長 読み取り|
|R4_data_read|0x45|赤外線コード 読み取り|
|W1_data_num_write|0x19|赤外線コード長 書き込み|
|W2_data_write|0x29|赤外線コード 書き込み|
|W3_trans_req|0x39|赤外線送信 指令|
