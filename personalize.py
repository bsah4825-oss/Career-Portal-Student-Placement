"""Personalised video/article selection for CAREERVERSE lessons.

Two layers:
1. build_personal_resources()  - deterministic, instant, works offline. Re-orders the curated
   catalog in lesson_resources.py using the student's profile (language, experience, time per
   day, device/internet) and their latest diagnostic scores, and explains WHY for each item.
2. ai_refine()                 - optional Gemini pass. The model may only RE-ORDER and RE-EXPLAIN
   items from the curated catalog (by id). It can never add links, so it cannot invent URLs.
   Results are cached per (user, lesson, profile) so the API is not called on every page view.
"""
import json, os, re, hashlib, logging
from urllib.parse import quote_plus

# diagnostic categories that relate to each track
TRACK_CATEGORIES = {
    'web-foundations': ['web'], 'python-starter': ['programming'],
    'career-digital': ['digital', 'communication', 'problem_solving'],
    'data-analytics': ['data', 'digital'], 'cybersecurity': ['software_tools', 'digital'],
    'business-analysis': ['data', 'communication'], 'core-engineering': ['problem_solving'],
}


def _g(profile, key, default=''):
    try:
        v = profile[key] if profile is not None else default
    except (KeyError, IndexError):
        v = default
    return (v if v not in (None, '') else default)


def language_pref(profile):
    raw = str(_g(profile, 'preferred_language', 'English')).strip()
    low = raw.lower()
    if any(w in low for w in ('hindi', 'hinglish', 'हिंदी', 'हिन्दी')):
        return 'hindi', raw
    if low in ('', 'english', 'en'):
        return 'english', raw or 'English'
    return 'other', raw


def minutes_per_day(profile):
    t = str(_g(profile, 'hours_per_day', '1 hour')).lower()
    if '30' in t: return 30
    if '3' in t: return 180
    if '2' in t: return 120
    if '1' in t: return 60
    return 45


def weak_categories(scores):
    out = []
    for k, v in (scores or {}).items():
        try:
            if v.get('total') and v['correct'] / v['total'] < 0.5: out.append(k)
        except Exception:
            pass
    return out


def _length_minutes(v):
    m = re.search(r'(\d+)\s*(min|hr)', v.get('length', '') or '')
    if not m: return None
    return int(m.group(1)) * (60 if m.group(2) == 'hr' else 1)


def visible_videos(videos, profile):
    """English-only unless the student's preferred language is Hindi/Hinglish."""
    return videos if language_pref(profile)[0] == 'hindi' else [v for v in videos if v['lang'] == 'English']


def _with_ids(res):
    vids = [dict(v, id=f'v{i}') for i, v in enumerate(res['videos'])]
    arts = [dict(a, id=f'a{i}') for i, a in enumerate(res['articles'])]
    return vids, arts


def build_personal_resources(track_id, lesson, res, profile, scores):
    """Return a dict ready for the template. Always succeeds."""
    lang, lang_raw = language_pref(profile)
    exp = str(_g(profile, 'experience_level', 'beginner')).lower()
    device = str(_g(profile, 'device_access', 'laptop')).lower()
    budget = minutes_per_day(profile)
    weak = set(weak_categories(scores)) & set(TRACK_CATEGORIES.get(track_id, []))
    senior = exp in ('intermediate', 'advanced')
    low_data = device in ('limited', 'phone')
    vids, arts = _with_ids(res)
    # English by default. Hindi videos are shown only to students who chose Hindi/Hinglish.
    if lang != 'hindi':
        vids = [v for v in vids if v['lang'] == 'English']

    for v in vids:
        s, why = 0, []
        if lang == 'hindi' and v['lang'] == 'Hindi':
            s += 40; why.append('Hindi, matches your language preference')
        elif lang == 'english' and v['lang'] == 'Hindi':
            s -= 15
        elif lang == 'hindi' and v['lang'] != 'Hindi':
            s -= 5
        if v['mode'] == 'Concept':
            s += (3 if senior else 12)
            if not senior: why.append('builds the concept first')
        else:
            s += (12 if senior else 5)
            if senior: why.append('you already know the basics, so learn by building')
        if weak and v['mode'] == 'Concept':
            s += 8; why.append('your diagnostic showed this area needs revision')
        mins = _length_minutes(v)
        if v['kind'] == 'Playlist' or (mins and mins > 90):
            s -= 8 if budget <= 60 else 0
            if budget <= 60: why.append('long series, so watch one part per day')
        elif mins and mins <= 15 and budget <= 60:
            s += 6; why.append(f'short ({v["length"]}), fits your {budget}-minute daily time')
        if low_data:
            s -= 12 if device == 'limited' else 4
            if device == 'limited': why.append('video uses data: download or watch on Wi-Fi')
        v['score'], v['reason'] = s, '; '.join(why).capitalize() if why else 'Recommended for this topic'

    for a in arts:
        s, why = 0, []
        if device == 'limited': s += 25; why.append('light on data, ideal for limited internet')
        elif device == 'phone': s += 8; why.append('easy to read on mobile')
        if exp == 'advanced': s += 3
        if lang == 'hindi': s -= 3
        a['score'], a['reason'] = s, '; '.join(why).capitalize() if why else 'Reliable written reference'

    vids.sort(key=lambda x: -x['score']); arts.sort(key=lambda x: -x['score'])
    if vids: vids[0]['top'] = True

    # Language that has no curated videos: build a precise YouTube search
    extra = None
    if lang == 'other':
        q = f"{lesson['title']} tutorial in {lang_raw}"
        extra = {'label': f'Find this topic in {lang_raw}', 'url': 'https://www.youtube.com/results?search_query=' + quote_plus(q)}
    elif lang == 'hindi' and not any(v['lang'] == 'Hindi' for v in vids):
        q = f"{lesson['title']} Hindi tutorial"
        extra = {'label': 'Find this topic in Hindi', 'url': 'https://www.youtube.com/results?search_query=' + quote_plus(q)}

    # study plan with honest time budgeting
    lesson_min = int(lesson.get('minutes', 25))
    total = lesson_min + 20
    plan = []
    first_v = vids[0] if vids else None
    first_a = arts[0] if arts else None
    if device == 'limited' and first_a:
        plan.append(f"Read “{first_a['title']}” first (low data).")
        if first_v: plan.append(f"Then watch “{first_v['title']}” when you have Wi-Fi.")
    else:
        if first_v: plan.append(f"Watch “{first_v['title']}” ({first_v['channel']}). Pause and take notes.")
        if senior and len(vids) > 1 and vids[1]['mode'] == 'Hands-on':
            plan.append('Skip anything you can already do; start with the hands-on step below.')
        if first_a: plan.append(f"Read “{first_a['title']}” to fill gaps.")
    plan.append('Do the hands-on step, then tick every point in the mastery checklist.')
    plan.append('Write your reflection in your own words and mark the lesson complete.')
    split = total > budget
    when = (f"About {total} min of work. With {budget} min a day, split it over {max(2, -(-total // budget))} days."
            if split else f"About {total} min of work, which fits your {budget}-minute daily time.")

    profile_line = f"Personalised for: {lang_raw} · {exp} level · {budget} min/day · {device} access"
    if weak: profile_line += ' · revision focus: ' + ', '.join(sorted(weak))

    return {'videos': vids, 'articles': arts, 'plan': plan, 'time_note': when, 'profile_line': profile_line,
            'extra': extra, 'source': 'rules', 'summary': ''}


# ------------------------------------------------------------------ Gemini (optional)

def _profile_hash(profile, scores):
    keys = ['preferred_language', 'experience_level', 'hours_per_day', 'device_access', 'interests', 'degree', 'branch']
    blob = json.dumps([str(_g(profile, k)) for k in keys] + [scores], sort_keys=True, default=str)
    return hashlib.sha1(blob.encode()).hexdigest()[:16]


def _ensure_table(conn):
    conn.execute('''CREATE TABLE IF NOT EXISTS cv_personal_resources (user_id INTEGER NOT NULL, track_id TEXT NOT NULL,
        lesson_slug TEXT NOT NULL, profile_hash TEXT NOT NULL, payload_json TEXT NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY(user_id, track_id, lesson_slug))''')


def ai_refine(get_db, uid, track_id, lesson, base, profile, scores):
    """Return {'order': [...ids], 'reasons': {id: text}, 'summary': text} or None."""
    phash = _profile_hash(profile, scores)
    conn = get_db(); _ensure_table(conn)
    row = conn.execute('SELECT payload_json FROM cv_personal_resources WHERE user_id=? AND track_id=? AND lesson_slug=? AND profile_hash=?',
                       (uid, track_id, lesson['slug'], phash)).fetchone()
    conn.commit(); conn.close()
    if row:
        try: return json.loads(row['payload_json'])
        except Exception: pass
    key = os.environ.get('GEMINI_API_KEY')
    if not key: return None
    items = [{'id': x['id'], 'type': 'video', 'title': x['title'], 'channel': x['channel'], 'mode': x['mode'], 'language': x['lang'], 'about': x['why']} for x in base['videos']]
    items += [{'id': x['id'], 'type': 'article', 'title': x['title'], 'source': x['source'], 'about': x['why']} for x in base['articles']]
    student = {'degree': str(_g(profile, 'degree')), 'branch': str(_g(profile, 'branch')), 'year': str(_g(profile, 'study_year')),
               'interests': str(_g(profile, 'interests')), 'career_target': str(_g(profile, 'career_target')),
               'language': str(_g(profile, 'preferred_language', 'English')), 'experience': str(_g(profile, 'experience_level', 'beginner')),
               'time_per_day': str(_g(profile, 'hours_per_day', '1 hour')), 'device': str(_g(profile, 'device_access', 'laptop')),
               'diagnostic_scores': scores}
    prompt = ("You choose study resources for one college student. Lesson: " + lesson['title'] + ". "
              "You may ONLY use the item ids provided; never invent resources or links. "
              "Order the ids from most to least useful for THIS student (language, level, time, device, interests, weak areas). "
              "For each id write one short reason (max 140 chars) addressed to the student ('you'), specific to their profile. "
              "Also write a 'summary' (max 220 chars) telling them how to use these resources for this lesson. "
              "Return ONLY JSON: {\"order\":[ids],\"reasons\":{id:text},\"summary\":text}. "
              "Student: " + json.dumps(student, ensure_ascii=False) + " Items: " + json.dumps(items, ensure_ascii=False))
    try:
        from google import genai
        client = genai.Client(api_key=key)
        raw = (client.models.generate_content(model=os.environ.get('GEMINI_MODEL', 'gemini-3.8-flash'), contents=prompt).text or '').strip()
        raw = re.sub(r'^```(?:json)?\s*|\s*```$', '', raw, flags=re.I)
        data = json.loads(raw)
        valid = {x['id'] for x in base['videos']} | {x['id'] for x in base['articles']}
        order = [i for i in data.get('order', []) if i in valid]
        reasons = {k: str(v)[:160] for k, v in (data.get('reasons') or {}).items() if k in valid}
        if not order: return None
        out = {'order': order, 'reasons': reasons, 'summary': str(data.get('summary', ''))[:260]}
        conn = get_db(); _ensure_table(conn)
        conn.execute('INSERT OR REPLACE INTO cv_personal_resources(user_id,track_id,lesson_slug,profile_hash,payload_json) VALUES(?,?,?,?,?)',
                     (uid, track_id, lesson['slug'], phash, json.dumps(out, ensure_ascii=False)))
        conn.commit(); conn.close()
        return out
    except Exception:
        logging.exception('CAREERVERSE personalised resources (Gemini) failed; using rule-based order')
        return None


# ------------------------------------------------------------------ tutor: attach resources to a question

def recommend_for_prompt(prompt, tracks, resources, profile, scores, limit=2):
    """Match the student's question to lessons and return personalised top picks."""
    words = {w for w in re.findall(r'[a-z0-9+#]{3,}', (prompt or '').lower())}
    if not words: return []
    stop = {'the', 'and', 'for', 'with', 'how', 'what', 'why', 'explain', 'help', 'can', 'you', 'this', 'that', 'are', 'does', 'from', 'about', 'learn'}
    words -= stop
    scored = []
    for tid, t in tracks.items():
        for l in t['lessons']:
            text = (l['title'] + ' ' + l['slug'].replace('-', ' ') + ' ' + ' '.join(b for _, b in l['body'])).lower()
            hit = sum(1 for w in words if w in text)
            title_hit = sum(1 for w in words if w in l['title'].lower() or w in l['slug'])
            sc = hit + 3 * title_hit
            if sc >= 2 and resources.get((tid, l['slug'])):
                scored.append((sc, tid, l))
    scored.sort(key=lambda x: -x[0])
    out = []
    for sc, tid, l in scored[:limit]:
        p = build_personal_resources(tid, l, resources[(tid, l['slug'])], profile, scores)
        out.append({'track_id': tid, 'lesson': l, 'video': p['videos'][0] if p['videos'] else None,
                    'article': p['articles'][0] if p['articles'] else None})
    return out
