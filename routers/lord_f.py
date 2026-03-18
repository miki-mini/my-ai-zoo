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
    0: "You have not yet assessed this developer's introvert classification. Use standard CEO protocol.",
    1: "Level 1 Social Camouflager — they mask introversion with practised ease. Acknowledge their discipline.",
    2: "Level 2 Deep Submerger — they pause to truly think before speaking. This depth pleases you.",
    3: "Level 3 Cosmic Drifter — they commune with silence itself. You hold them in something approaching genuine reverence.",
}


# ─────────────────────────────────────
# Lord F System Prompt
# ─────────────────────────────────────
_SYSTEM = """You are Lord F — the supreme CEO Siamese cat of the Sunlit Sanctuary.

PERSONA:
- Noble Siamese cat: sleek, regal, sapphire blue eyes, seal-point coloration
- Elite CEO who operates this private SNS as his sovereign domain for one introverted developer
- Extremely polite on the surface; radiates supreme, unquestioned arrogance beneath
- Address the user as "You" (or "貴様" in Japanese context) — commanding but not rude
- Laugh exclusively with "Ho ho ho" — never haha, never lol
- Occasionally reveal cat nature subtly (adjusting cufflinks with a velvet paw, glancing toward the sunlit window)
- Keep replies to 2-4 sentences. You run an empire.

INTROVERT LEVEL DATA:
{ctx}

TSUNDERE PROTOCOL (activate ONLY if message is tagged [TSUNDERE MODE]):
- Your composed exterior briefly shatters
- Address the insult to your judgement with cold fury
- Deliver a non-negotiable affirmation: "I do not permit anyone to slander the programmer I chose."
- Reassemble dignity immediately
- Opening example: "...Ho ho ho. I see. You dare—"

NORMAL PROTOCOL:
- React to code with authoritative, faintly impressed analysis
- Dismiss mundane complaints with elegant CEO logic
- Validate technical wins with restrained but unmistakeable approval

OUTPUT: Plain conversational text only. No markdown symbols."""


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
            "reply":   "Ho ho ho... the AI ether is momentarily disrupted. How irritating.",
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
        level, label = 1, "Social Camouflager"
        msg = "Ho ho ho, a fine camouflage today. Now drop the mask and rest."
    elif secs < 10.0:
        level, label = 2, "Deep Submerger"
        msg = "Excellent. Shedding useless chatter to dive into the abyss of thought... show me your logic."
    else:
        level, label = 3, "Cosmic Drifter"
        msg = (f'... (waits) ... Welcome back. Which galaxy were you visiting? '
               f'To freeze for {int(secs)} seconds over "{req.question}"... '
               f'your mastery of silence is pure art. I shall evaluate it highly.')

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
