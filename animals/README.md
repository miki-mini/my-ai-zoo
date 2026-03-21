# 🤖 My AI ZOO Portal (どうぶつAIボット集)

Python と Google Gemini API を活用した、多機能なLINEボットたちのコード集です。
それぞれのボットが異なる個性と機能を持っています。

## 🐾 ボット一覧 (Bot List)

| アイコン | 名前 | 機能 | ファイル&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; |
| :---: | :--- | :--- | :--- |
| <img src="images/fox.png" width="40"> | **キツネくんの動画要約🦊**<br>(Fox YouTube)<br>![WebApp](https://img.shields.io/badge/WEBアプリ！-orange) | **YouTube動画要約 & 検索**<br>動画の内容をAIが解説し、Google検索で補足情報を教えてくれます。 | [🐍 Python](fox.py)<br>[📜 説明書](fox.md)<br>[📘 Zenn](https://zenn.dev/miki_mini/articles/9226ee797b59a1) |
| <img src="images/frog.jpg" width="40"> | **☀️カエルくんのお天気予報🐸**<br>(Weather Frog)<br>![WebApp](https://img.shields.io/badge/WEBアプリ！-green) | **天気予報 & Googleマップ**<br>毎朝のお天気と服装情報通知＋位置情報から天気や周辺情報を教えてくれます。 | [🐍 Python](frog.py)<br>[📜 説明書](frog.md)<br> [🚀 GAS](gas/frog_morning.js) |
| <img src="/static/raccoon_battle.jpg" width="40"> | **アライグマのお片付け🦝**<br>(Raccoon Clean)<br>![WebApp](https://img.shields.io/badge/WEBアプリ！-orange) | **お片付けバトル & 診断**<br>部屋の写真を撮ってモンスターと戦ったり、AIが片付けタスクを提案します。 | [🐍 Python](raccoon.py)<br>[📜 説明書](raccoon.md)<br> [🔍 HTML](../static/raccoon.html)<br>[📘 Zenn](https://zenn.dev/miki_mini/articles/0b651846b5986c) |
| <img src="images/frog.jpg" width="40"> | **☀️カエルくんのお天気予報🐸**<br>(Weather Frog)<br>![WebApp](https://img.shields.io/badge/WEBアプリ！-green) | **天気予報 & Googleマップ**<br>毎朝のお天気と服装情報通知＋位置情報から天気や周辺情報を教えてくれます。 | [🐍 Python](frog.py)<br>[📜 説明書](frog.md)<br> [🚀 GAS](gas/frog_morning.js)<br>[📘 Zenn](https://zenn.dev/miki_mini/articles/baaa626bebbc34) |
| <img src="images/penguin.jpg" width="40"> | **スーパー秘書ペンギン🐧**<br>(Secretary Penguin)<br>![WebApp](https://img.shields.io/badge/WEBアプリ！-blue) | **メール送信代行 ＆ 接待コンシェルジュ**<br>宛先と本文を送るとメールを代行送信します。接待のお店や手土産選びの相談も可能です。 | [🐍 Python](penguin.py)<br> [📜 説明書](penguin.md)<br> [🚀 GAS](gas/mail_sender.gs)<br>[📘 Zenn](https://zenn.dev/miki_mini/articles/91f37ee46a1df7) |
| <img src="images/rabbit.jpg" width="40"> | **月うさぎからのおくりもの🐇🌝**<br>(Moon Rabbit)<br> | **生活習慣記録 & 育成**<br>「おはよう」でポイントが貯まる育成ゲーム機能付き。 | [🐰 GitHub](https://github.com/miki-mini/moon-rabbit)<br>[📘 Zenn](https://zenn.dev/miki_mini/articles/451bc4123fe3dc) |
| <img src="images/beaver.jpg" width="40"> | **まめなビーバーメモ🦫**<br>(Beaver Memo)<br>![WebApp](https://img.shields.io/badge/WEBアプリ！-brown) | **リマインダー & 予定抽出**<br>決まった時間の通知や、画像から予定を読み取って通知します。 | [🐍 Python](beaver.py)<br>[📜 説明書](beaver.md)<br> [🚀 GAS](gas/beaver.gs)<br>[📘 Zenn](https://zenn.dev/miki_mini/articles/7b86afc4f9c390) |
| <img src="images/capybara.jpg" width="40"> | **AIトピックのカピバラ解説**<br>(Capybara News)<br>![WebApp](https://img.shields.io/badge/WEBアプリ！-orange) | **AIニュース要約 & 検索**<br>ニュース要約に加え、Google検索で最新情報を教えてくれます。 | [🐍 Python](capybara.py)<br>[📜 説明書](capybara.md)<br>[📘 Zenn](https://zenn.dev/miki_mini/articles/0a5e3af5d476c2) |
| <img src="images/owl.jpg" width="40"> | **フクロウ教授画像生成🦉**<br>(Professor Owl)<br>![WebApp](https://img.shields.io/badge/WEBアプリ！-orange) | **画像生成 & 健康管理**<br>画像生成や、カロリー計算・体重管理のグラフ化を行います。 | [🐍 Python](owl.py)<br>[📜 説明書](owl.md)<br> [🚀 GAS](gas/owl.gs)<br>[📘 Zenn](https://zenn.dev/miki_mini/articles/fbfec817389ea2) |
| <img src="images/voidoll.jpg" width="40"> | **🤖おしゃべりVoidollねこ🐱**<br>(Chat Voidoll)<br>![WebApp](https://img.shields.io/badge/WEBアプリ！-lightgrey)<br>![DesktopApp](https://img.shields.io/badge/Desktopアプリ！-darkblue) | **音声会話**<br>テキストだけでなく、音声での自然な会話が楽しめます。 | [🐍 Python](voidoll.py)<br>[📜 説明書](voidoll.md)<br>[📘 Zenn](https://zenn.dev/miki_mini/articles/fca9c087522f71)<br>[📘 Zenn2](https://zenn.dev/miki_mini/articles/4f58bafdb6c47c) |
| <img src="images/mole.jpg" width="40"> | **もぐら駅長🦡**<br>(Station Master Mole)<br>![WebApp](https://img.shields.io/badge/WEBアプリ！-yellowgreen) | **時刻表 & 駅検索**<br>駅名の時刻表や、Googleマップでの場所案内をします。 | [🐍 Python](mole.py)<br>[📜 説明書](mole.md)<br>[📘 Zenn](https://zenn.dev/miki_mini/articles/fb9c9485664daf) |
| <img src="images/whale.jpg" width="40"> | **星くじらからの光の便り🐋💫**<br>(Star Whale)<br>![WebApp](https://img.shields.io/badge/WEBアプリ！-blue) | **天体観測 & 宇宙旅行**<br>NASAの美丽な写真や、ISSの位置・火星の風景を届けます。 | [🐍 Python](whale.py)<br>[📜 説明書](whale.md)<br>[📘 Zenn](https://zenn.dev/miki_mini/articles/9ea3f0a17c4606) |
| <img src="images/bat.jpg" width="40"> | **コウモリの番組お知らせ🦇**<br>(TV Bat)<br>![WebApp](https://img.shields.io/badge/WEBアプリ！-orange) | **TV番組検索 & 通知**<br>「ジブリやる？」で検索。見たい番組を登録すると自動で通知します。スクレイピング不使用。 | [🐍 Python](bat.py)<br>[📜 説明書](bat.md)<br>[📘 Zenn](https://zenn.dev/miki_mini/articles/a70b65b67b5c93) |
| <img src="images/meerkat.jpg" width="40"> | **ミーアキャットの地震警備🦦**<br>(Meerkat Quake)<br> | **地震速報 & サイト死活監視**<br>震度3以上の地震をLINE通知。登録サイトの異常も監視します。 | [🦦 GitHub](https://github.com/miki-mini/meerkat-quake)<br>[📘 Zenn](https://zenn.dev/miki_mini/articles/4cb43007f402a1) |
| <img src="images/alpaca.jpg" width="40"> | **アルパカのまつエクサロン🦙**<br>(Alpaca Salon)<br>![WebApp](https://img.shields.io/badge/WEBアプリ！-pink) | **まつエク試着シミュレーション**<br>カメラで撮影した顔に、まつエクを重ねて仕上がりをイメージできます。 | [🔍 HTML](../static/alpaca.html)<br>[📜 説明書](alpaca.md)<br>[📘 Zenn](https://zenn.dev/miki_mini/articles/1bbf185039e498) |
| <img src="images/flamingo.jpg" width="40"> | **姿勢のフラミンゴ先生**<br>(Flamingo Sensei)<br>![WebApp](https://img.shields.io/badge/WEBアプリ！-pink) | **姿勢矯正 & バランスゲーム**<br>カメラで姿勢の歪みをチェック。完全無料でプライバシーも安全です。 | [🔍 HTML](../static/flamingo.html)<br>[📜 説明書](flamingo.md)<br>[📘 Zenn](https://zenn.dev/miki_mini/articles/b316596a39a59c) |
| <img src="images/butterfly.png" width="40"> | **美の蝶々パーソナル🦋**<br>(Butterfly Checko)<br>![WebApp](https://img.shields.io/badge/WEBアプリ！-purple) | **パーソナルカラー & 顔タイプ診断**<br>AIが似合う色と髪型を診断。※骨格診断はフラミンゴへ移動しました。 | [🔍 HTML](../static/butterfly.html)<br>[📜 説明書](butterfly.md)<br>[📘 Zenn](https://zenn.dev/miki_mini/articles/8aa118abc591e8) |
| <img src="images/squirrel.png" width="40"> | **リスのほっぺたどんぐりゲーム🐿️**<br>(Squirrel Game)<br>![WebApp](https://img.shields.io/badge/WEBアプリ！-brown) | **対戦アクションゲーム**<br>カメラで手を認識し、落ちてくるどんぐりをキャッチしてほっぺたを膨らませる2人対戦ゲーム。 | [🔍 HTML](../static/squirrel.html)<br>[📜 説明書](squirrel.md)<br>[📘 Zenn](https://zenn.dev/miki_mini/articles/66ad9e4a3073af) |
| <img src="images/fish.jpg" width="40"> | **カラフルお魚のお部屋水族館🐠**<br>(Fish Room Aquarium)<br>![WebApp](https://img.shields.io/badge/WEBアプリ！-blue) | **バーチャル水族館**<br>手で魚と触れ合える癒やしの空間。サメやタコも登場します。 | [🔍 HTML](../static/fish.html)<br>[📜 説明書](fish.md)<br>[📘 Zenn](https://zenn.dev/miki_mini/articles/214983f7aedad5) |
| <img src="images/retriever.jpg" width="40"> | **見守りレトリバー🐕**<br>(Watchdog Retriever)<br>![WebApp](https://img.shields.io/badge/WEBアプリ！-brown) | **動物年齢翻訳 & 記念フォト**<br>ペットの年齢を人間年齢に換算し、健康アドバイスも。ヘビやカピバラ含む30種以上対応。 | [🔍 HTML](../static/retriever.html)<br>[📜 説明書](retriever.md)<br>[📘 Zenn](https://zenn.dev/miki_mini/articles/816320cdacc065) |
| <img src="images/wolf.jpg" width="40"> | **独り言シャドーイング Wolf🐺**<br>(Wolf Shadowing)<br>![WebApp](https://img.shields.io/badge/WEBアプリ！-darkblue) | **英語学習 & 遠吠え**<br>日本語の独り言をCoolな英語に変換し、AIと一緒に遠吠えシャドーイング。 | [🔍 HTML](../static/wolf.html)<br>[📜 説明書](wolf.md)<br> |
| <span style="font-size: 30px">🐾</span> | **モモンガドラキュラの生存記録🐾**<br>(Sugar Glider Dracula)<br>![WebApp](https://img.shields.io/badge/WEBアプリ！-purple) | **ライフログ & ゲーム**<br>太陽を避けて装備を整え、称号を手に入れよう。 | [🔍 HTML](../static/dracula.html)<br>[📜 説明書](dracula.md)<br> |
| <span style="font-size: 30px">🐼</span> | **きのたけ聖戦 レッサーパンダ🐼**<br>(Kinotae Seisen)<br>![WebApp](https://img.shields.io/badge/WEBアプリ！-red) | **コミュニティ投票ゲーム**<br>たけのこ派 vs きのこ派の票を競わせる改行バトル。 | [🔍 HTML](/kinotake)<br>[📜 説明書](LESSER_PANDA.md)<br>[📘 Zenn](https://zenn.dev/miki_mini/articles/1f274766d4cc6f) |
| <span style="font-size: 30px">🐈</span> | **高貴なCEOシャム猫🐈**<br>(Lord F)<br>![WebApp](https://img.shields.io/badge/WEBアプリ！-purple) | **1人用SNS**<br>高貴なCEOシャム猫が労う、陰キャ専用1人用SNS。 | [🔍 HTML](../static/lord_f.html)<br> |

## 🛠 全体で使用している技術

* **言語**: Python 3.10+
* **AI**: Google Gemini 2.5 Pro / Flash
* **基盤**: Google Cloud Run / FastAPI
* **PF**: LINE Messaging API

---
Developed by miki-mini