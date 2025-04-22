import os
import datetime
import json
import requests

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro-latest:generateContent"
USED_FILE = "used_meiba_gemini.json"
POSTS_DIR = "_posts"

def generate_post():
    today = datetime.datetime.now().strftime("%Y-%m-%d")

    # 使用済み読み込み
    if os.path.exists(USED_FILE):
        with open(USED_FILE, "r", encoding="utf-8") as f:
            used = json.load(f)
    else:
        used = []

    avoid_list = ", ".join(used)

    prompt = f"""
あなたは日本競馬の評論家です。以下の条件に従って、実在した名馬に関する読み応えのあるブログ記事を生成してください。

【条件】
- 必ず実在した競走馬（架空の馬は禁止）
- 以下の馬は過去に記事化されています：{avoid_list}
- 新たな馬を選び、過去の馬と重複しないこと
- 日本語で、Markdown形式
- 記事冒頭に「# 馬名 - タイトル説明文」と見出し付きで書いてください
- 全体で5000字以上
- 以下の構成を満たしてください：

## 構成項目（すべて300字以上）
1. 馬の概要（血統、戦績、主な勝鞍）
2. 成績と活躍エピソード（図表があれば出力）
3. ライバル馬との対決
4. 騎手や調教師との関係性
5. ファンに愛された理由、引退後の話
6. おもしろハプニングや逸話
7. 編集後記（個人的な視点からの総括）

## 表現
- 表や箇条書き、番号付きリストで見やすく整理
- 図解風に「展開」「世代構成」などがあれば積極的に表現

記事の最後に「関連画像を生成してください：馬名のイラスト風画像」と一言追加
"""

    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.7, "maxOutputTokens": 4096}
    }

    response = requests.post(f"{GEMINI_API_URL}?key={GEMINI_API_KEY}", headers=headers, json=payload)
    if response.status_code != 200:
        raise Exception("Gemini API error:", response.text)

    text = response.json()["candidates"][0]["content"]["parts"][0]["text"]
    lines = text.split("\n")
    first_line = lines[0].replace("#", "").strip()
    body = "\n".join(lines[1:]).strip()

    title = first_line
    horse_name = title.split("-")[0].strip()
    filename = f"{POSTS_DIR}/{today}-{horse_name.replace(' ', '_')}.md"

    os.makedirs(POSTS_DIR, exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"""---
title: "{title}"
date: {today}
layout: post
description: "名馬『{horse_name}』の伝説と魅力を深堀り"
---

{body}
""")

    used.append(horse_name)
    with open(USED_FILE, "w", encoding="utf-8") as f:
        json.dump(used, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    generate_post()
