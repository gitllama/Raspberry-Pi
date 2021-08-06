# 4. Express

## 4.1. express-generatorでのテンプレート(ejs)生成

```bash 
$ express appname --view=ejs
$ cd appname
$ npm install bootstrap
$ npm install bulma
$ npm install js-yaml
```

## 4.2. 生成ディレクトリ構成例

```
[root]
 ├─ app.js         ：起点
 ├─ [bin]
 │   └─ www    　  ：サーバープロセスの起動処理
 ├─ [node_modules] ：モジュール
 ├─ [public]　     ：静的リソース（JavaScript, CSS, imgなど）
 ├─ [routes]　     ：ルーティング処理
 │   └─ index.js
 └─ [views]　      ：UIを格納
     └─ index.ejs
```

## 4.3. node.jsの記述変更例

### a. ccsの読込

app.js
```javascript
app.use('/local-bulma', express.static(path.join(__dirname, '/node_modules/bulma')));
```

index.ejs
```html
<link rel="stylesheet" href="local-bulma/css/bulma.min.css">
```

### b. Web APIの作成

index.js
```javascript
// GETリクエスト(情報の取得)に対してレスポンス(値を返却)
app.get('/api/list', (req, res) => {
　var val = req.query.name; // queryから値の取り出し
  res.json(todoList);       // JSONを返却
  // res.send('Hello');     // 文字列の返却
});

app.get('/api/:id', (req, res) => {
  var val = req.params.id;  // paramとして値の取り出し
  res.send('Hello ' + val);
});

// POSTリクエスト(処理の指示)を行いレスポンスを得る(値を返却)
app.post('/api/add', (req, res) => {
  var val = req.query.name;       // queryから値の取り出し
  const todoData = req.body.name; // bodyから値の取り出し
  res.json(todoItem);
});
```

index.ejs
```html
  <script>
  
  fetch(`./api/?name=${query}`, { method: 'GET' })
    .then((res) => res.json())
    .then((obj) => console.log(obj))
    .catch((err) => console.error('Error:', err));
  
  fetch(`./api`, { 
    method : 'POST',
    body : JSON.stringify({ name : 'nyname' })
  }).then((res) => res.json())
    .then((obj) => console.log(obj))
    .catch((err) => console.error('Error:', err));

  </script>
```

- GET : リソースを取得するときに使う
  - 冪等かつ安全かつキャッシュ可能
  - ブックマーク可能
  - queryがつかえる ```GET: /foo/bar?itemId=xxxx-xxxx```
- POST : 特有の処理をするときに使う
  - 冪等でないかつ安全でない
  - ブックマークできない
  - query+Body(URLにかかれないパラメータ) 
    - ```POST: /foo/bar?user="taro"``` 
    - ```body:{"itemId": "xxxx-xxxx"}```
- Other
  - HEAD/OPTIONS/PUT/DELETE

### c. node.jsから子プロセス実行

```javascript
var exec = require('child_process').exec;
const fs = require('fs');

app.post('/api/add', (req, res) => {
  var op = req.body.op;
  var cmd = `./public/rust/i2c -c ./public/remote_config.yml ${op}`;
  // var cmd = `python3 ./scripts/send.py ${op}`

  exec(cmd, function(err,stdout,stderr){
    if(err != null){
      res.json({
        result: 'err',
        stdout : stderr
      });
    }else{
      res.json({
        result : 'sucess',
        stdout : stdout
      });
    }
  });
});
```

## 4.4. 実行

```bash
$ DEBUG=pircsv:* npm start
```

```bash
$ pm2 start [app.json] --name [name]
```