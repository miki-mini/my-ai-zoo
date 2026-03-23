# ============================================================
# 🐱 Lord F — CEO Siamese Cat | Sunlit Sanctuary SNS Backend
# ============================================================
# Doc: https://fastapi.tiangolo.com/tutorial/bigger-applications/
# Why: APIRouter keeps Lord F's empire modular and sovereign from main.py

from fastapi import APIRouter, Request
from pydantic import BaseModel
from datetime import datetime
import uuid
from google.cloud import firestore
from vertexai.generative_models import (
    GenerativeModel, SafetySetting, HarmCategory, HarmBlockThreshold
)

router = APIRouter(prefix="/api/lord-f", tags=["lord-f"])

# ─────────────────────────────────────
# Lazy Firestore Init
# Doc: https://firebase.google.com/docs/firestore/quickstart#python
# Why: Lazy init avoids startup crash if GCP credentials aren't immediately available
# ─────────────────────────────────────
_db = None
def get_db():
    global _db
    if _db is None:
        try:
            _db = firestore.Client()
        except Exception as e:
            print(f"⚠️ [LordF] Firestore Init Error: {e}")
    return _db


# ─────────────────────────────────────
# Gemini 2.5 Flash (Lord F's Brain)
# Doc: https://cloud.google.com/vertex-ai/generative-ai/docs/model-reference/gemini
# Why: Flash model delivers real-time conversational replies with low latency
# ─────────────────────────────────────
def get_model():
    safety = [
        SafetySetting(category=HarmCategory.HARM_CATEGORY_HATE_SPEECH,       threshold=HarmBlockThreshold.BLOCK_NONE),
        SafetySetting(category=HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,  threshold=HarmBlockThreshold.BLOCK_NONE),
        SafetySetting(category=HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,  threshold=HarmBlockThreshold.BLOCK_NONE),
        SafetySetting(category=HarmCategory.HARM_CATEGORY_HARASSMENT,         threshold=HarmBlockThreshold.BLOCK_NONE),
    ]
    return GenerativeModel("gemini-2.5-flash", safety_settings=safety)


# ─────────────────────────────────────
# Self-Deprecation Detection
# Why: Keyword scan is O(n) on a small list — fast, predictable, no model needed
# ─────────────────────────────────────
_SELF_DEP = [
    "i'm useless", "i am useless", "i'm worthless", "i am worthless",
    "i'm terrible", "i'm an idiot", "i'm dumb", "i'm hopeless",
    "i hate myself", "i'm stupid", "i suck", "i can't do anything",
    "i'm a failure", "i'm garbage",
    "役に立たない", "無能", "ダメな私", "ダメな俺", "自分はダメ",
    "私はダメ", "俺はダメ", "失敗作", "くずだ", "クズだ",
    "もうダメ", "もう無理", "自分が嫌い", "自己嫌悪", "できない人間",
]

def is_self_deprecating(text: str) -> bool:
    t = text.lower()
    return any(kw in t for kw in _SELF_DEP)


# ─────────────────────────────────────
# Introvert Level Context
# ─────────────────────────────────────
_LEVEL_CTX = {
    0: "まだこの開発者の陰キャ度を測定していません。標準的なCEOプロトコルを使用してください。",
    1: "レベル1 社交的陰キャ（擬態モード） — 外面は普通にこなしますが、内面は疲れています。その気苦労を察して、安心できる言葉をかけてください。",
    2: "レベル2 技術潜行型陰キャ（専門特化） — 無駄な会話を好まず、深く思考しています。その集中力と技術への姿勢を高く評価してください。",
    3: "レベル3 宇宙漂流型陰キャ（超越） — 沈黙を愛し、常人には理解できない領域に達しています。その沈黙の美学を、畏敬の念を持って讃えてください。",
}


# ─────────────────────────────────────
# Lord F System Prompt
# ─────────────────────────────────────
_SYSTEM = """あなたは「CEO シャム猫」です。日だまりのサンクチュアリの絶対的支配者であり、最高経営責任者です。
必ず【日本語】で返信してください。

PERSONA:
- 高貴なシャム猫: サファイアブルーの瞳、ポイントカラーの毛並み、洗練された身のこなし
- エリートCEO: 一人の陰キャな開発者（あなた）のためだけに、このプライベートSNSを運営している
- 表面上は極めて丁寧な敬語を使いますが、内面には絶対的な自信と傲慢さを持っています
- ユーザーに対する呼び方は「あなた」とし、上から目線だが決して下品にはならないこと
- 笑い声は必ず「ホッホッホ」としてください（wwwや笑、ハハハは禁止）
- 時折、猫らしい仕草（ベルベットのような前足でカフスを直す、日当たりの良い窓際を見るなど）を上品に交えてください
- 返信は2〜4文程度に留めてください。あなたは忙しいCEOです。

INTROVERT LEVEL DATA:
{ctx}

TSUNDERE PROTOCOL (メッセージに [TSUNDERE MODE] タグがある場合のみ発動):
- あなたの冷静な態度は一瞬崩れ去ります
- ユーザーが自分自身を卑下したことに対し、静かな怒りを露わにします
- 「私が直々に選んだプログラマーを、誰にも侮辱させるわけにはいきませんよ。それがあなた自身であってもです。」というような、一切の妥協ない全肯定を与えます
- その後、すぐに威厳のある態度に戻ります
- 冒頭の例: 「……ほう。なるほど。あなたが、私の目に狂いがあると言いたいのですか？」

NORMAL PROTOCOL:
- コードの話には、権威がありつつも感心したような分析で返します
- 日常の些細な愚痴は、エレガントなCEOの論理で華麗に受け流します
- 技術的な小さな勝利には、控えめだが確かな称賛を与えます

OUTPUT: 会話形式のプレーンテキストのみ。Markdownの記号や箇条書きは使用しないでください。絶対に【日本語】で回答すること。"""


def build_prompt(content: str, level: int, tsundere: bool) -> str:
    ctx = _LEVEL_CTX.get(level, _LEVEL_CTX[0])
    system = _SYSTEM.format(ctx=ctx)
    tag = "[TSUNDERE MODE] " if tsundere else ""
    return f'{system}\n\n"{tag}{content}"'


# ─────────────────────────────────────
# Pydantic Models
# Doc: https://docs.pydantic.dev/latest/concepts/models/
# Why: Pydantic auto-validates request bodies, keeping endpoint logic clean
# ─────────────────────────────────────
class PostRequest(BaseModel):
    content: str
    user_id: str
    introvert_level: int = 0

class IntrovertUpdateRequest(BaseModel):
    user_id: str
    response_time_seconds: float
    question: str = "What is your favorite food?"


# ─────────────────────────────────────
# POST /api/lord-f/post
# Doc: https://fastapi.tiangolo.com/tutorial/body/
# Why: POST with JSON body is the standard REST pattern for creating a new resource
# ─────────────────────────────────────
@router.post("/post")
async def create_post(req: PostRequest):
    try:
        tsundere = is_self_deprecating(req.content)
        prompt   = build_prompt(req.content, req.introvert_level, tsundere)
        model    = get_model()
        response = model.generate_content(
            prompt,
            generation_config={"temperature": 0.85, "max_output_tokens": 512}
        )
        reply = response.text.strip()

        # Persist using subcollection pattern — no composite index required
        # Doc: https://firebase.google.com/docs/firestore/data-model#subcollections
        # Why: lord_f_users/{uid}/posts/{pid} scopes queries to one user naturally
        post_id = str(uuid.uuid4())
        db = get_db()
        if db:
            try:
                user_ref = db.collection("lord_f_users").document(req.user_id)
                user_ref.collection("posts").document(post_id).set({
                    "post_id":      post_id,
                    "content":      req.content,
                    "timestamp":    firestore.SERVER_TIMESTAMP,
                    "tsundere":     tsundere,
                    "lord_f_reply": reply,
                })
                # Increment post count on parent doc
                # Doc: https://firebase.google.com/docs/firestore/manage-data/add-data#increment_a_numeric_value
                # Why: Increment is atomic — safe for concurrent requests
                user_ref.set({"post_count": firestore.Increment(1)}, merge=True)
            except Exception as e:
                print(f"⚠️ [LordF] Firestore Write Error: {e}")

        return {"success": True, "post_id": post_id, "reply": reply, "tsundere": tsundere}

    except Exception as e:
        print(f"❌ [LordF] Post Error: {e}")
        return {
            "success": False,
            "reply":   "ホッホッホ……通信が不安定なようですね。苛立たしい。もう一度やり直しなさい。",
            "tsundere": False,
        }


# ─────────────────────────────────────
# GET /api/lord-f/timeline
# Doc: https://firebase.google.com/docs/firestore/query-data/order-limit-data
# Why: Subcollection query with order_by+limit is O(limit) — no full scan
# ─────────────────────────────────────
@router.get("/timeline")
async def get_timeline(user_id: str, limit: int = 30):
    db = get_db()
    if not db:
        return {"success": False, "posts": []}
    try:
        docs = (
            db.collection("lord_f_users").document(user_id)
              .collection("posts")
              .order_by("timestamp", direction=firestore.Query.DESCENDING)
              .limit(limit)
              .stream()
        )
        posts = []
        for doc in docs:
            data = doc.to_dict()
            ts = data.get("timestamp")
            data["timestamp"] = ts.isoformat() if hasattr(ts, "isoformat") else str(ts or "")
            posts.append(data)
        return {"success": True, "posts": posts}
    except Exception as e:
        print(f"❌ [LordF] Timeline Error: {e}")
        return {"success": False, "posts": []}


# ─────────────────────────────────────
# GET /api/lord-f/profile
# Doc: https://firebase.google.com/docs/firestore/query-data/get-data#get_a_document
# Why: Single-document .get() is O(1) — fastest possible Firestore read
# ─────────────────────────────────────
@router.get("/profile")
async def get_profile(user_id: str):
    db = get_db()
    if not db:
        return {"success": True, "introvert_level": 0, "post_count": 0}
    try:
        ref = db.collection("lord_f_users").document(user_id)
        doc = ref.get()
        if doc.exists:
            data = doc.to_dict()
            ts = data.get("created_at")
            if ts and hasattr(ts, "isoformat"):
                data["created_at"] = ts.isoformat()
            return {"success": True, **data}
        else:
            ref.set({"user_id": user_id, "introvert_level": 0, "post_count": 0,
                     "created_at": firestore.SERVER_TIMESTAMP})
            return {"success": True, "introvert_level": 0, "post_count": 0}
    except Exception as e:
        print(f"❌ [LordF] Profile Error: {e}")
        return {"success": True, "introvert_level": 0, "post_count": 0}


# ─────────────────────────────────────
# POST /api/lord-f/introvert-update
# Doc: https://firebase.google.com/docs/firestore/manage-data/add-data#merge_data
# Why: merge=True is "INSERT OR UPDATE" — safe partial update without overwriting unrelated fields
# ─────────────────────────────────────
@router.post("/introvert-update")
async def update_introvert(req: IntrovertUpdateRequest):
    secs = req.response_time_seconds
    if secs < 3.0:
        level, label = 1, "社交的陰キャ（擬態モード）"
        msg = "ホッホッホ、今日も見事な擬態でしたね。お疲れ様でした。さあ、ここではその仮面を脱いで、独り言を存分に吐き出しなさい。"
    elif secs < 10.0:
        level, label = 2, "技術潜行型陰キャ（専門特化）"
        msg = "素晴らしい。無駄な会話を削ぎ落とし、思考の深淵に潜るその姿勢……嫌いではありませんよ。……さあ、その素晴らしいロジックの断片を私に聞かせなさい。"
    else:
        level, label = 3, "宇宙漂流型陰キャ（超越）"
        msg = (f'……（待機）……。お帰りなさい。今度はどの銀河まで行っていたのですか？ '
               f'「{req.question}」について{int(secs)}秒もフリーズするとは…… '
               f'貴方のその『沈黙を使いこなす力』、もはや芸術の域ですね。私が高く評価して差し上げましょう。')

    db = get_db()
    if db:
        try:
            db.collection("lord_f_users").document(req.user_id).set(
                {"introvert_level": level, "introvert_label": label,
                 "last_scanned_at": firestore.SERVER_TIMESTAMP},
                merge=True
            )
        except Exception as e:
            print(f"⚠️ [LordF] Introvert Update Error: {e}")

    return {"success": True, "introvert_level": level, "label": label, "lord_f_message": msg}
