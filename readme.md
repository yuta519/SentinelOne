
【SentinelOne EPP】APIを活用したサンプルスクリプト(イベントの自動解決)
============


本サンプルスクリプトについて
------------

本サンプルスクリプトは、SentinelOneが検知したイベントの中で対応不要なイベント(※1)をAPIから一括で解決済み(Resolved)にします。
※1 レピュテーションと静的ファイル解析のエンジンで検知し対象ファイルが隔離されたイベント


ファイル一覧
------------

- .env
- requirements.txt 
- readme.md
- mark_as_resolved.py
- settings.py
- lambda/mark_as_resolved_lambda.py


環境情報
------------

本サンプルスクリプトの動作環境は下記となります。

- python3.7
- 必要な python ライブラリ
	- urllib.request
	- json
	- python-dotenv


セットアップ方法
------------

#### python ライブラリのインストール

ライブラリのインストールにはpipが必要です。

```
pip install -r requirements.txt
```


#### 管理サーバ・アカウント情報の追加

.env内の下記項目を環境にあわせて置き換えます。

	- <SentinelOne Manager URL>
	- <user name>
	- <user password>


#### スクリプトの実行

下記を実行すると対応不要なイベントを一括で解決済みにします。

```
python mark_as_resolved.py
```


自動化方法
------------

本サンプルスクリプトの実行を自動化する2つ方法(cronから実行・AWS Lambdaから実行)をご紹介します。

#### cronから実行

```
crontab -e
```

ex) 5分間隔で実行する場合

```
*/5 * * * * 'python /path/to/mark_as_resolved.py'
```


#### AWS Lambdaから実行

AWS Lambdaにて本スクリプトを実行する。イベントのトリガーはCloud Watchにてスケジュールで行う。

1. AWSマネージドコンソールからLambdaサービスへ移動
2. 「関数の作成」へ進む
3. 関数の作成画面から
	- 「一から作成」を選択
	- 基本的な情報
		- 「関数名」を任意で記入
		- 「ランタイム」を「python3.7」を選択
		- 「アクセス権限」を任意で設定
4. Designer画面からLambdaを選択し、関数コードに既存で用意されるlambda_function.pyに/lambda/mark_as_resolved_lambda.pyを転記
5. Designer画面左側のトリガーの追加から「CloudWatch Events」を追加し「トリガーの設定」から新規でルールを作成する。ルールタイプはスケジュール式を選択し下記のように入力する

ex) 5分間隔で実行する場合
```
	rate(5 minutes)
```