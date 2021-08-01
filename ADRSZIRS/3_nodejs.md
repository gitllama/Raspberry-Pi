# 3. node.jsとの連携

## 3.1. PythonのCall

a. Python-shell

```$ npm install python-shell```

```javascript
var {PythonShell} = require('python-shell');

PythonShell.runString('x=1+1;print(x)', null, function (err, data) {
  if (err) throw err;
  console.log(data)
});

var options = {
  mode: 'text',
  pythonPath: './',
  args ; ['2', '3']
};
PythonShell.run('script.py', options, function (err, data) {
  if (err) throw err;
  console.log(data);
});

var pyshell = new PythonShell('my_script.py');
pyshell.send('hello');
pyshell.on('message', function (message) {
  console.log(message);
);
```

```python
import sys

data = sys.stdin.readline() // pyshell.sendでは標準入力から値を取得
num1 = int(sys.argv[1])     // PythonShell.runのoption argsを使用した際はargvから値を取得
num2 = int(sys.argv[2])
print(num1 + num2)          // 標準出力へ結果を返す
```

b. child_process

```javascript
var exec = require('child_process').exec;

var params = "1 4";
var cmd = `python3 ./script.py ${params}`;
exec(cmd, function(err, stdout, stderr){
  if(err != null){
    console.log("err");
    return;
  }
  console.log(stdout);
}
```

## 3.2. RustのCall

Pythonと同様child_processが使用できる
