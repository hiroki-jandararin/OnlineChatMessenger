# Oneline Chat Messenger

TCP + UDP チャットメッセンジャーアプリ

---

## ✅ 概要

* TCP：ルーム作成・参加などのコントロール操作
* UDP：実際のチャットメッセージのやり取り
* トークン・ユーザー・IPアドレスの検証を行い、なりすまし防止も対応
* JSONではなく独自バイナリプロトコルを採用

  * 高速・軽量な通信を実現
  * パフォーマンス向上・帯域の節約

---

## 📂 ディレクトリ構成

```
OnelineChatMessenger/
├── client/
│   ├── create_room.py
│   ├── join_room.py
│   └── udp_chat.py
├── server/
│   ├── main.py
│   ├── tcp_handler.py
│   ├── udp_handler.py
│   └── room_manager.py
├── shared/
│   ├── config.py
│   └── protocol.py
└── README.md
```

---

## ▶️ 実行方法

### サーバーの起動

```bash
python -m server.main
```

### クライアント（ルーム作成）

```bash
python -m client.create_room
```

### クライアント（ルーム参加）

```bash
python -m client.join_room
```

---

## ✏️ 操作手順

1. **create\_room.py** 実行

   * ユーザー名を入力 → `user1`
   * ルーム名を入力 → `room1`
   * 接続IP → `0.0.0.0`（ローカル）
   * チャットネーム → `your_name`
2. **join\_room.py** 実行

   * ユーザー名 → `user2`
   * ルーム名 → `room1`
   * 接続IP → `0.0.0.0`
   * チャットネーム → `your_name2`
3. メッセージを送信 → すべての参加者にリアルタイムでブロードキャスト

---

## 📡 プロトコル仕様（技術的詳細）

### 🔧 TCPヘッダー構造（32バイト）

| フィールド            | サイズ   | 内容               |
| ---------------- | ----- | ---------------- |
| room\_name\_size | 1バイト  | ルーム名のバイト数        |
| operation        | 1バイト  | 操作種別 (1:作成,2:参加) |
| state            | 1バイト  | 状態コード            |
| payload\_size    | 29バイト | ボディのサイズ          |

### 💬 TCPボディ構造

* room\_name + payload（例：ユーザー名やトークン）

### 📡 UDPメッセージ構造

| フィールド       | 内容             |
| ----------- | -------------- |
| usernamelen | 1バイト           |
| username    | 可変長            |
| tokenlen    | 1バイト           |
| token       | 可変長            |
| roomnamelen | 1バイト           |
| roomname    | 可変長            |
| message     | 残り全部（UTF-8文字列） |

---

## 🧪 テスト項目チェックリスト

### ✅ 正常系

*

### 🔒 異常系

*

---

## 🪵 ログ例

```
[TCP] 接続 from ('127.0.0.1', 63572)
[DEBUG] Parsed header - room_name_size: 5, op: 1, state: 0, payload_size: 10
TCP処理: room=room1, op=1, state=0, user=user1
[UDP] user1@room1: hello from ('127.0.0.1', 55185)
```

---

## 🛠 今後の改善案

*

---

## 👤 作者

* Nakano Hiroki
