# words

iOS アプリ「言葉ジグソー（仮）」の問題データです。誤解されやすい日本語（慣用句・ことわざ・四字熟語など）を収録しています。

## 配信 URL

```
https://masanorifunaki.github.io/words/words.json
```

アプリは起動時にこの URL から取得します。`main` に push すると GitHub Pages に反映されるため、言葉の追加にアプリの再ビルドは要りません。

## GitHub Pages の公開設定

公開元は `main` ブランチのルート（`/`）です。ビルドは GitHub 標準の Pages ビルドに任せており、Actions のワークフローは置いていません。

### 初回の有効化

リポジトリは Public にしておきます。有効化は次のどちらかでします。

- 画面: Settings → Pages → Build and deployment で、Source を `Deploy from a branch`、Branch を `main` と `/ (root)` にして Save を押します。
- CLI:

  ```bash
  gh api -X POST repos/masanorifunaki/words/pages -f "source[branch]=main" -f "source[path]=/"
  ```

### 公開状態を確かめる

ビルドの状態を確かめます。`built` なら公開済みです。

```bash
gh api repos/masanorifunaki/words/pages --jq .status
```

配信された JSON を取得して、件数を確かめます。

```bash
curl -s https://masanorifunaki.github.io/words/words.json | python3 -c "import json,sys; print(len(json.load(sys.stdin)['words']))"
```

push から反映までは数分かかります。CDN のキャッシュが残るため、直後は古い内容が返ることがあります。

## JSON スキーマ

```json
{
  "version": 2,
  "words": [
    {
      "no": 1,
      "id": "nasake-wa-hito-no-tame-narazu",
      "text": "情けは人のためならず",
      "reading": "なさけはひとのためならず",
      "category": "ことわざ",
      "meaning": "人に情けをかけておけば、巡り巡って自分に良い報いが返ってくる。",
      "misunderstanding": "情けをかけるのはその人のためにならない、という意味だと思われがち。",
      "note": "「ためならず」は「ためではない」の意。"
    }
  ]
}
```

| フィールド | 内容 |
| --- | --- |
| `no` | 数えるための通し番号。1 から連番 |
| `id` | 出題の識別子。一度公開したら変更しない |
| `text` | パズルにする言葉 |
| `reading` | 読み（ひらがな） |
| `category` | `ことわざ` / `慣用句` / `四字熟語` / `故事成語` / `言葉` / `副詞` |
| `meaning` | 正しい意味 |
| `misunderstanding` | よくある誤解 |
| `note` | 由来などの補足 |

## 言葉を追加する手順

1. `words.json` の `words` の末尾に 1 件追加します。`no` は最後の番号 + 1 にします。
2. 手元で検証します。`N words OK` と出れば通過です。

   ```bash
   python3 scripts/validate_words.py
   ```

3. ブランチを切って PR を作ります。GitHub Actions の `Validate words.json` が同じ検証を走らせます。
4. 検証が通ったら `main` にマージします。反映まで数分かかります。

## 検証の内容

`scripts/validate_words.py` は次を確かめます。PR と `main` への push のたびに GitHub Actions でも走ります。

- JSON として読めること
- `version` が整数で、`words` が 1 件以上あること
- `no` が 1 からの連番であること
- `id` が重複していないこと
- `id` から `note` までの文字列フィールドが空でないこと
- `category` が定義済みの値であること。新しいカテゴリを使うときは、スクリプトの `CATEGORIES` にも追加します
