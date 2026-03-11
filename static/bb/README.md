# 🐕 BERNARD BEACON

![alt text](BB.webp)

> **Digital Smoke Signal for Disaster Scenarios**
> セルネットワーク完全不通時のオフラインSOSシステム / Offline SOS system for complete cellular network outages

[English Documentation is available below.](#english-documentation)

---

## コンセプト

大地震などでセルタワーが倒壊し、インターネットが完全に失われた状況を想定しています。

**天才的なループホール：** 救助者はアプリ不要。
パニックに陥った人々がWi-Fi設定を開いたとき、`!__SOS_35.681_139.767__!` というSSIDが目に入ります。接続するとキャプティブポータルが起動し、詳細なSOS情報が画面に表示されます。

```
被災者のスマホ              救助者のスマホ
┌─────────────────┐        ┌──────────────────┐
│ BERNARD BEACON  │  WiFi  │  Wi-Fi設定       │
│ [DEPLOY BEACON] │ ────→  │ !_SOS_35.6_139.7 │
│                 │        │ ← 接続すると...   │
│ 🐕 送信中...    │        │ ⚡SOS画面が出現！│
└─────────────────┘        └──────────────────┘
```

---

## スクリーンショット / UI概要

```
┌─────────────────────────────────┐
│  🐕  BERNARD BEACON             │
│  Digital Smoke Signal           │
├─────────────────────────────────┤
│ [1] SOSプロフィール — 事前設定   │
│   氏名、場所、医療情報、連絡先    │
├─────────────────────────────────┤
│ [2] GPS取得 & ビーコンID生成     │
│   📍 35.68145, 139.76715 ±4m   │
│   ┌─────────────────────────┐   │
│   │!_SOS_35.681_139.767_R302│   │  ← SSID
│   └─────────────────────────┘   │
├─────────────────────────────────┤
│ [3] ビーコン展開 — 緊急起動       │
│         ╭─────────╮             │
│         │   🆘    │  ← 巨大ボタン│
│         │ DEPLOY  │             │
│         │ BEACON  │             │
│         ╰─────────╯             │
└─────────────────────────────────┘
```

---

## 機能一覧

### STEP 1 — SOSプロフィール設定
事前（平常時）に入力・保存する情報です。

| フィールド | 内容 |
|---|---|
| 氏名 | 救助者への本人特定情報 |
| 場所の詳細 | 建物名・住所 |
| 建物内の位置 | 階・部屋番号（SSID生成に使用） |
| 医療情報 | 血液型・持病・アレルギー・常用薬 |
| 緊急連絡先 | 家族・勤務先の電話番号 |
| 現在の状況 | 負傷状態・残余物資など |

> `localStorage` に保存されるため、電源断→再起動後も復元されます。

---

### STEP 2 — GPS取得 & SSID生成

#### GPS取得

```
API: navigator.geolocation.getCurrentPosition()
     + Android: FusedLocationProviderClient (PRIORITY_HIGH_ACCURACY)

ソース: https://developer.mozilla.org/en-US/docs/Web/API/Geolocation/getCurrentPosition
```

- GPS / Wi-Fi / セルタワーを自動的に最良の方法で測位
- 精度（誤差メートル）も取得・表示
- 設定済みならアプリ起動時に自動取得

#### SSID生成ルール

```
IEEE 802.11 制限: 最大 32バイト (UTF-8)

フォーマット:
  !_SOS_{緯度}_{経度}_R{部屋番号}
  例: !_SOS_35.681_139.767_R302

"!_" プレフィックス:
  ASCIIコードが小さいため、ほぼ全てのOSの
  Wi-Fiスキャンリストで最上位に表示される。
```

---

### STEP 3 — ビーコン展開

#### A. キャプティブポータルHTTPサーバー

```
ライブラリ: NanoHTTPD v2.3.1
ポート: 8080
ソース: https://github.com/NanoHttpd/nanohttpd
```

- デバイスのホットスポットに接続した端末からのHTTPリクエストに応答
- OS別キャプティブポータルプローブを検知して302リダイレクトを返却

| OS | プローブURL | 期待値 |
|---|---|---|
| Android | `connectivitycheck.gstatic.com/generate_204` | 204 No Content |
| iOS/macOS | `captive.apple.com/hotspot-detect.html` | 特定レスポンス |
| Windows | `www.msftconnecttest.com/connecttest.txt` | 特定テキスト |

**302を返す**ことでOSが「キャプティブポータルあり」と判断し、
「ネットワークにサインイン」通知 → ブラウザでSOSページを自動表示。

> ⚠️ **Port制限:** LinuxベースのAndroidではport 80はroot権限が必要。
> 本実装はport 8080で動作。自動検知ができない場合でも、
> **SSIDにGPS座標が含まれる**ため情報伝達は成立します。

#### B. テザリング設定 Intent

```
API: android.provider.Settings (TetherSettings → Panel → Wireless)
ソース: https://developer.android.com/reference/android/provider/Settings#ACTION_WIRELESS_SETTINGS
```

Android 10 以降、アプリからのSSID書き換えは禁止されています
(`WifiManager.setWifiApConfiguration()` deprecated in API 29)。
そのため、クリップボードにSSIDをコピーした上でOSのテザリング設定画面を開き、
ユーザーが貼り付ける「セミオートマティック」方式を採用しています。

#### C. バッテリー節約パルスモード

テザリングは約400mAの消費電流があります。パルスモードで大幅に節約できます。

```
デフォルト設定: ON 1分 / スリープ 5分 (6分サイクル)

計算例 (3000mAhバッテリー):
  常時稼働: ~7.5時間
  パルスモード: ~15〜20時間（理論値の約2.5倍）

根拠: 救助チームのエリア巡回は10〜30分間隔が多く、
      6分サイクルで十分な検出確率を確保できる。
```

---

## アーキテクチャ

```
┌─────────────────────────────────────────────────────┐
│                  static/bb/index.html               │
│  (HTML + CSS + JavaScript — 完全オフライン動作)      │
│                                                      │
│  ① localStorage  → プロフィール永続化               │
│  ② Geolocation API → GPS取得                        │
│  ③ Clipboard API → SSID自動コピー                   │
│  ④ Capacitor Bridge → ネイティブ機能呼び出し        │
└────────────────┬────────────────────────────────────┘
                 │ window.Capacitor.Plugins.BernardBeacon
┌────────────────▼────────────────────────────────────┐
│         BernardBeaconPlugin.java (Capacitor)         │
│                                                      │
│  getLocation()         FusedLocationProviderClient   │
│  copyToClipboard()     ClipboardManager              │
│  openHotspotSettings() Settings Intent               │
│  startServer()  ──────────────────────────┐          │
│  stopServer()                             │          │
│  isServerRunning()                        │          │
└───────────────────────────────────────────┼──────────┘
                                            │
┌───────────────────────────────────────────▼──────────┐
│              SOSHttpServer.java (NanoHTTPD)           │
│                           port 8080                  │
│                                                      │
│  全リクエスト → SOSページ (200 OK)                   │
│  キャプティブプローブ → 302 Redirect                 │
└──────────────────────────────────────────────────────┘
```

---

## ファイル構成

```
project/
├── static/bb/
│   └── index.html                  # メインアプリ UI
│
├── android/app/src/main/
│   ├── AndroidManifest.xml         # パーミッション宣言
│   └── java/com/miki/botapp/
│       ├── MainActivity.java        # プラグイン登録
│       ├── BernardBeaconPlugin.java # Capacitorブリッジ
│       └── SOSHttpServer.java       # NanoHTTPDサーバー
│
├── android/app/build.gradle        # 依存関係
└── capacitor.config.json           # appName, webDir設定
```

---

## ビルド & 実行

```bash
# 1. Webアセットをネイティブプロジェクトに同期
npx cap sync android

# 2a. Android Studioで開く
npx cap open android

# 2b. またはコマンドラインでビルド
cd android && ./gradlew assembleDebug

# 3. APKの場所
#    android/app/build/outputs/apk/debug/app-debug.apk
```

### 必要な環境
- Node.js + npm
- Android Studio (Hedgehog 以降推奨)
- Android SDK API 36
- 実機テスト推奨 (GPS・テザリングはエミュレータ非対応)

---

## 依存関係

| ライブラリ | バージョン | 用途 |
|---|---|---|
| `@capacitor/core` | ^8.0.2 | JS↔Android ブリッジ |
| `@capacitor/android` | ^8.0.2 | Android WebView ホスト |
| `org.nanohttpd:nanohttpd` | 2.3.1 | 組み込みHTTPサーバー |
| `com.google.android.gms:play-services-location` | 21.3.0 | GPS (FusedLocation) |

---

## パーミッション

| パーミッション | 用途 |
|---|---|
| `ACCESS_FINE_LOCATION` | GPS高精度測位 |
| `ACCESS_COARSE_LOCATION` | GPS粗精度フォールバック |
| `INTERNET` | HTTPサーバー (port 8080) |
| `ACCESS_WIFI_STATE` | デバイスIPアドレス取得 |
| `CHANGE_WIFI_STATE` | Wi-Fi設定連携 |
| `FOREGROUND_SERVICE` | 画面OFF中もサーバーを維持 |
| `POST_NOTIFICATIONS` | フォアグラウンドサービス通知 |

---

## 緊急時の使い方（3ステップ）

```
【事前】アプリを開いて STEP 1 を記入・保存する

【緊急時】
  STEP 2: 「📍 取得」をタップ → GPSとSSIDが自動生成される
  STEP 3: 「🆘 DEPLOY BEACON」をタップ
          → SSIDがコピーされ、テザリング設定が開く
          → ホットスポット名にSSIDを貼り付けてONにする

【あとは待つだけ】
  救助者がWi-Fiスキャン → !_SOS_... を発見 → 接続
  → SOS情報ページが自動表示
```

---

## 名前の由来

**St. Bernard（セント・バーナード犬）** — アルプスの雪山で遭難者を救助した歴史的な救助犬。
**Beacon（ビーコン）** — 煙信号・灯台など、位置を知らせるサインの総称。

> *「デジタルの煙信号」— ネットワークが完全に死んでも、Wi-Fiという電波だけで救助を呼ぶ。*

---
## 🎥 Video Demonstration


https://github.com/user-attachments/assets/1c98794f-615b-437f-9310-7e0e5ecb4d72



---
## ライセンス

MIT License

---

*BERNARD BEACON — Built with ❤️ for survival*

---
---

# English Documentation

## Concept

This app is designed for disaster scenarios (like massive earthquakes) where cell towers collapse and internet access is completely lost. **It works anywhere in the world** because it relies on standard Wi-Fi tethering and Captive Portal technology built into every smartphone.

**The Genius Loophole:** Rescuers *do not* need to have the app installed.
When people open their Wi-Fi settings looking for a connection, they will spot an abnormal SSID like `!_SOS_35.681_139.767_R302`. Simply seeing this communicates your exact GPS location. If they connect to it, a captive portal automatically launches on their phone, displaying your detailed SOS information.

```text
Victim's Phone              Rescuer's Phone
┌─────────────────┐        ┌──────────────────┐
│ BERNARD BEACON  │  WiFi  │  Wi-Fi Settings  │
│ [DEPLOY BEACON] │ ────→  │ !_SOS_35.6_139.7 │
│                 │        │ ← Upon connect...│
│ 🐕 Sending...   │        │ ⚡SOS page pops up│
└─────────────────┘        └──────────────────┘
```

## Features

### STEP 1 — SOS Profile Setup
Information to enter and save during normal times (stored in `localStorage`).
- Name
- Location Details (Address/Building Name)
- In-Building Position (Floor/Room number)
- Medical Info (Blood type, allergies, medications)
- Emergency Contacts
- Current Condition

### STEP 2 — GPS Acquisition & SSID Generation
- Uses `navigator.geolocation` / Android's `FusedLocationProviderClient` to get high-accuracy coordinates (lat/lng/accuracy), even offline.
- Generates a Wi-Fi SSID within the 32-byte (UTF-8) IEEE 802.11 limit.
- Puts `!_` at the beginning so the SSID floats to the very top of Wi-Fi scan lists.
- Example: `!_SOS_35.681_139.767_R302`

### STEP 3 — Deploy Beacon
- **A. Captive Portal HTTP Server:** Runs a NanoHTTPD server on port 8080. It intercepts captive portal probes from Android/iOS/Windows and returns a `302 Redirect`, tricking the rescuer's OS into showing a "Sign in to network" pop-up that displays your SOS web page.
- **B. Hotspot Settings Intent:** Due to Android 10+ privacy restrictions on Apps modifying SSIDs, the app automatically copies the SSID to your clipboard and opens the native Android Hotspot Settings. You just paste it in and turn the hotspot ON.
- **C. Battery Pulse Mode:** Tethering eats battery quickly (~400mA). Pulse Mode (e.g. 1 min ON / 5 mins OFF) extends your battery life by up to 2.5x, giving you enough juice to survive overnight while still being statistically likely to be found during rescuer sweeps.

## Origin of the Name

**St. Bernard** — The historic rescue dog from the Swiss Alps.
**Beacon** — A signal fire or lighthouse indicating location.

> *"A digital smoke signal" — Even when the network is completely dead, we call for help over the airwaves using just Wi-Fi.*
