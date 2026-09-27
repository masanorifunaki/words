# words

iOS アプリ「言葉ジグソー（仮）」の問題データを置くリポジトリ。`words.json` を GitHub Pages で配信し、アプリは起動時に `https://masanorifunaki.github.io/words/words.json` を取得する。

## 前提

- `main` へのマージがそのまま本番配信になる。Pages は `main` の `/` から自動でデプロイされ、アプリの再ビルドなしで全ユーザーに届く
- 壊れた JSON や誤った解説を配信すると、ユーザーに誤った日本語を教えることになる。コードより内容の正しさを優先する

## ブランチと PR

- 作業は必ず最新の `main` からブランチを切って始める。`main` へ直接 push しない

  ```bash
  git fetch origin && git switch -c <branch> origin/main
  ```

- ブランチ名は `add-words-<先頭の no>-<末尾の no>`（例: `add-words-51-55`）、修正は `fix-<id>`
- マージは PR 経由のみ。GitHub Actions の `Validate words.json` が通ってからマージする

## 検証（commit 前に必ず実行）

```bash
python3 scripts/validate_words.py
```

`N words OK` 以外が出たら commit しない。スクリプトは形式（JSON・連番・id 重複・空欄・text の長さ・category）しか見ないため、内容は次の「内容チェック」で確かめる。

## データのルール

- `no`: 1 からの連番。追加は末尾に足す。途中に挿入・削除して番号を振り直さない
- `id`: `reading` をヘボン式寄りのローマ字にし、単語を `-` でつなぐ小文字。アプリが解いた言葉の記録に使うため、公開後は変えない
- `text`: 20 文字以内。アプリは 20 文字を超える言葉を盤面に描けないため、配信されても出題しない。上限を変えるときは `scripts/validate_words.py` の `MAXIMUM_TEXT_LENGTH` と、アプリ側の `WordsRepository.maximumTextLength` をそろえる
- `category`: `ことわざ` / `慣用句` / `四字熟語` / `故事成語` / `言葉` / `副詞` のいずれか。増やすときは `scripts/validate_words.py` の `CATEGORIES` も直す
- `meaning` / `misunderstanding` / `note` は常体で書き、すべて「。」で終える
- `misunderstanding` は「〜だと思われがち。」「〜と言われがち。」の形にそろえる
- 語の引用は「」、書名は『』を使う

## 内容チェック

言葉を追加・修正したときは、該当エントリについて次をすべて確かめ、結果を PR 本文に書く。

1. 誤字・脱字: `text` / `reading` / 解説文に誤変換や脱字がない
2. 読み: `reading` が `text` の読みと一致し、`id` のローマ字とも対応している
3. 意味: `meaning` が国語辞典の本来の意味と一致している。辞書名を PR 本文に書く（例: 広辞苑 第七版、大辞林 第四版、デジタル大辞泉）
4. 誤用: `misunderstanding` が実際に広まっている誤用である。文化庁「国語に関する世論調査」に載っていれば調査年を書く
5. 対になっているか: `meaning` と `misunderstanding` が同じ観点（意味・表記・読み）で対比できている
6. 由来: `note` の語源・出典が辞書や原典で確かめられる。確かめられない説は書かないか「〜とされる」と書く
7. 辞書で扱いが割れる語: 近年は誤用も認める辞書がある場合（例: 的を得る）、`note` にその旨を書く
8. category: 形式に合っている（例: 四字熟語は漢字 4 字）

確かめられなかった項目は推測で埋めず、「未確認」として PR 本文に残す。
