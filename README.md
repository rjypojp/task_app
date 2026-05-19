# タスク管理アプリ

Flaskを使ったタスク管理アプリです。  
ユーザーごとにタスクを管理でき、天気や祝日情報の取得、Googleカレンダー連携機能を利用できます。

---

## 機能

- ユーザー登録・ログイン
- タスクの追加・編集・削除・完了管理
- コメントの追加
- 天気情報の取得（OpenWeather API）
- 祝日情報の表示
- Googleカレンダー連携

---

## 使用技術

- Python
- Flask
- SQLite
- HTML / CSS
- OpenWeather API
- Google Calendar API

---

## セットアップ方法

```bash
git clone <リポジトリURL>
cd task_app
pip install -r requirements.txt
python app.py
``` 

---

## .env設定

アプリを動かすために、プロジェクト直下に `.env` ファイルを作成し、以下を記述してください。

```env
SECRET_KEY=your_secret_key
OPENWEATHER_API_KEY=your_api_key
```
※ `your_secret_key` や `your_api_key` は各自の値に置き換えてください。

---

## 工夫した点

- 「実際に使いやすいか」を意識して設計しました
- 天気APIとカレンダーを組み合わせて、日常で役立つ機能を追加しました
- Googleカレンダーと連携し、予定管理をしやすくしました。
- タスクに補足コメントを追加できるようにし、情報管理をしやすくしました
- パスワードはハッシュ化し、セキュリティ面も考慮しました
- ChatGPTを活用しつつ、自分で理解しながら実装・ノートに整理して進めました

---

## 公開URL

以下のURLから実際にアプリを利用できます。

https://task-app-t4xs.onrender.com

※ Renderの無料プランを利用しているため、初回アクセス時は起動まで30秒ほどかかる場合があります。

---

## ローカル実行

http://127.0.0.1:5000