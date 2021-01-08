# 従業員管理アプリケーション

Docker で環境構築をし、CRUD 機能を備えた Web App

## 使用技術

- python
- mysql
- tornado
- unittest
- docker

## 環境構築

```bash
# コンテナをデタッチモード(バックグラウンド)で起動
$ docker-compose up -d --build

# コンテナ、ネットワーク、イメージの削除
$ docker-compose down --rmi all
```

## 初期画面

![alt text](./images/初期画面.png)

## 新規登録画面

![alt text](./images/新規登録.png)

## 一覧画面

![alt text](./images/一覧.png)

## 詳細画面

![alt text](./images/詳細.png)

## 更新画面

![alt text](./images/更新.png)

## 削除画面

![alt text](./images/削除.png)
