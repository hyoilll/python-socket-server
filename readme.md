# Python ソケット通信を利用したファイルを伝送するプログラム

---

**概要**

- クライアント側からサーバー側までファイルを伝送し、セーブするプログラム

**作業期間**

- 一週間

**開発言語・技術：**

- Python

**分類**

1. チェット

2. ファイル伝送

**機能**

1. チェット
   - Thread を利用してリアルタイムでクライアント側とサーバー側が通信することが可能
2. ファイル伝送
   - クライアント側からサーバー側までアップロード
   - サーバー側からクライアント側までダウンロード
   - サーバー側のファイルリストをチェック

**シミュレーション**

1. 接続

![server-connect](https://user-images.githubusercontent.com/50327128/107147830-822c9180-6993-11eb-988d-464522e1aab4.JPG)

2. アップロード

![server-upload](https://user-images.githubusercontent.com/50327128/107147832-848eeb80-6993-11eb-94c6-48201f37ee92.JPG)

3. サーバー側のファイルリストをチェック

![server-filelistprint](https://user-images.githubusercontent.com/50327128/107147835-8658af00-6993-11eb-9caf-cfb2f344b5c4.JPG)

4. ダウンロード

![server-download](https://user-images.githubusercontent.com/50327128/107147836-8789dc00-6993-11eb-88e2-1b3f1e139a7a.JPG)
