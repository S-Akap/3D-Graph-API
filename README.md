# 3D-Graph-API

このプロジェクトは、日本の自治体の人口、座標、標高に関する情報を提供するFlaskベースのAPIです。APIは、政府のオープンデータや地理データベースなど、さまざまなソースからデータを取得します。

**サンプル** 東京都[https://architectural-digital-design.onrender.com/api/12](https://architectural-digital-design.onrender.com/api/12)

## 目次

- [特徴](#特徴)
- [実行環境](#実行環境)
- [設定](#設定)
- [使用方法](#使用方法)
- [APIエンドポイント](#apiエンドポイント)

## 特徴

- 日本の各自治体の人口データを取得
- 緯度経度を平面直角座標に変換
- 座標に基づいて標高データを取得
- 市区町村データ（ID、名前、座標（x, y, 標高）、人口）を提供

## 実行環境

- Python 3.8+
- Flask
- requests
- numpy
- python-dotenv

## 設定

1. プロジェクトのルートディレクトリに `.env` ファイルを作成し、以下の環境変数を追加します:

    ```env
    APP_ID=your_estat_app_id
    API_KEY=your_resas_api_key
    ```

2. `your_estat_app_id` をあなたのe-Stat APIのアプリIDに、`your_resas_api_key` をあなたのRESAS APIキーに置き換えます。

## 使用方法

1. Flaskアプリケーションを起動します:

    ```bash
    flask run
    ```

2. APIは `http://127.0.0.1:5000/` で利用可能になります。

## APIエンドポイント

### 都道府県コードで市区町村データを取得

- **エンドポイント:** `/api/<int:pref_code>`
- **メソッド:** `GET`
- **URLパラメータ:**
  - `pref_code` (整数): 市区町村データを取得する都道府県コード。
- **説明:** 指定された都道府県コードに対する市区町村データ（ID、名前、座標（x, y, z）、人口）を返します。
- **レスポンス:**

    ```json
    {
        "status": "SUCCESS",
        "result": [
            {
                "id": "city_code",
                "name": "city_name",
                "coordinates": {
                    "x": x_coordinate,
                    "y": y_coordinate,
                    "elevation": elevation
                },
                "population": population
            },
            ...
        ]
    }
    ```
