#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import re
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent

SUBJECT_META = [
    {"id": "국어", "name": "국어", "group": "공통·필수", "emoji": "📖", "color": "#f76707", "file": "국어.md"},
    {"id": "수학", "name": "수학", "group": "공통·필수", "emoji": "📐", "color": "#1c7ed6", "file": "수학.md"},
    {"id": "영어", "name": "영어", "group": "공통·필수", "emoji": "🔤", "color": "#7048e8", "file": "영어.md"},
    {"id": "한국사", "name": "한국사", "group": "공통·필수", "emoji": "🏯", "color": "#c2255c", "file": "한국사.md"},
    {"id": "물리", "name": "물리학Ⅰ", "group": "과학탐구", "emoji": "🧲", "color": "#0ca678", "file": "물리.md"},
    {"id": "화학", "name": "화학Ⅰ", "group": "과학탐구", "emoji": "⚗️", "color": "#e67700", "file": "화학.md"},
    {"id": "생명과학", "name": "생명과학Ⅰ", "group": "과학탐구", "emoji": "🧬", "color": "#2f9e44", "file": "생명과학.md"},
    {"id": "지구과학", "name": "지구과학Ⅰ", "group": "과학탐구", "emoji": "🌏", "color": "#1098ad", "file": "지구과학.md"},
]

SYM = {
    'rightarrow': '→', 'to': '→', 'implies': '⟹', 'Rightarrow': '⇒',
    'leftrightarrow': '↔', 'uparrow': '↑', 'downarrow': '↓', 'leftarrow': '←',
    'Delta': 'Δ', 'delta': 'δ', 'cdot': '·', 'theta': 'θ', 'times': '×',
    'sum': 'Σ', 'propto': '∝', 'bigcirc': '◯', 'll': '≪', 'gg': '≫',
    'equiv': '≡', 'circ': '∘', 'pm': '±', 'mu': 'μ', 'lambda': 'λ',
    'triangle': '△', 'sim': '∼', 'nu': 'ν', 'neq': '≠', 'ne': '≠',
    'land': '∧', 'lor': '∨', 'int': '∫', 'bullet': '•', 'Phi': 'Φ',
    'phi': 'φ', 'vert': '|', 'sigma': 'σ', 'rho': 'ρ', 'tau': 'τ', 'epsilon': 'ε',
    'sin': 'sin', 'cos': 'cos', 'tan': 'tan', 'log': 'log', 'ln': 'ln', 'lim': 'lim',
    'alpha': 'α', 'beta': 'β', 'gamma': 'γ', 'pi': 'π', 'omega': 'ω', 'infty': '∞',
    'le': '≤', 'leq': '≤', 'ge': '≥', 'geq': '≥', 'approx': '≈',
    'therefore': '∴', 'because': '∵', 'cdots': '⋯', 'ldots': '…',
    'quad': '  ', 'qquad': '   ', ',': ' ', ';': ' ', ':': ' ', '!': '',
    ' ': ' ', '{': '{', '}': '}', '%': '%', '$': '$', '_': '_', '&': '&', '|': '‖'
}

SUP = {'0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴', '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹', '-': '⁻', '+': '⁺', 'n': 'ⁿ'}

def esc(s: str) -> str:
    return str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')

def hex_to_soft(hex_str: str, a: float) -> str:
    n = int(hex_str[1:], 16)
    return f"rgba({(n >> 16) & 255},{(n >> 8) & 255},{n & 255},{a})"

def tex2html(src: str) -> str:
    i = 0
    n = len(src)

    def read_arg(text_mode=False):
        nonlocal i
        while i < n and src[i] == ' ':
            i += 1
        if i < n and src[i] == '{':
            i += 1
            r = seq('}', text_mode)
            if i < n and src[i] == '}':
                i += 1
            return r
        if i < n and src[i] == '\\':
            return cmd()
        if i < n:
            c = src[i]
            i += 1
            return f"<i>{c}</i>" if re.match(r'[a-zA-Z]', c) and not text_mode else esc(c)
        return ''

    def cmd():
        nonlocal i
        i += 1
        m = re.match(r'^[a-zA-Z]+', src[i:])
        if m:
            name = m.group(0)
            i += len(name)
        else:
            name = src[i] if i < n else ''
            i += 1
        if name in ('text', 'mathrm', 'operatorname', 'textrm'):
            return '<span class="tx">' + read_arg(True) + '</span>'
        if name in ('mathbf', 'textbf', 'boldsymbol'):
            return '<b>' + read_arg() + '</b>'
        if name in ('frac', 'dfrac', 'tfrac'):
            a = read_arg()
            b = read_arg()
            return f'<span class="fr"><span class="nu">{a}</span><span class="de">{b}</span></span>'
        if name == 'vec':
            return '<span class="vec">' + read_arg() + '</span>'
        if name == 'sqrt':
            return '√<span style="text-decoration:overline">' + read_arg() + '</span>'
        if name in ('left', 'right'):
            return ''
        return esc(SYM.get(name, name))

    def seq(end=None, text_mode=False):
        nonlocal i
        out = ''
        while i < n and src[i] != end:
            c = src[i]
            if c == '\\':
                out += cmd()
            elif c == '^':
                i += 1
                out += '<sup>' + read_arg() + '</sup>'
            elif c == '_':
                i += 1
                out += '<sub>' + read_arg() + '</sub>'
            elif c == '{':
                i += 1
                out += seq('}', text_mode)
                if i < n and src[i] == '}':
                    i += 1
            elif text_mode:
                out += esc(c)
                i += 1
            elif c == ' ':
                i += 1
            elif re.match(r'[a-zA-Z]', c):
                out += f'<i>{c}</i>'
                i += 1
            elif c == ',':
                out += ', '
                i += 1
            elif re.match(r'[=+<>]', c) or (c == '-' and out):
                out += ' ' + esc(c) + ' '
                i += 1
            else:
                out += esc(c)
                i += 1
        return out

    res = seq(None)
    res = re.sub(r'(→|⟹|↔|≡|∝|×|≪|≠|∧|≤|≥)', r' \1 ', res)
    res = re.sub(r'\s{2,}', ' ', res).strip()
    return res

def tex2plain(src: str) -> str:
    h = tex2html(src)
    def repl_sup(m):
        t = re.sub(r'<[^>]+>', '', m.group(1))
        if all(ch in SUP for ch in t):
            return ''.join(SUP[ch] for ch in t)
        return f'^({t})'
    h = re.sub(r'<sup>(.*?)</sup>', repl_sup, h)
    h = re.sub(r'<span class="fr"><span class="nu">(.*?)</span><span class="de">(.*?)</span></span>', r'(\1)/(\2)', h)
    h = re.sub(r'<[^>]+>', '', h)
    return h.replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"').replace('&amp;', '&')

def math_html(tex: str, display: bool = False) -> str:
    cls = 'm md' if display else 'm'
    return f'<span class="{cls}" data-tex="{esc(tex)}">{tex2html(tex)}</span>'

def inline(t: str) -> str:
    ph = []
    def put(h):
        ph.append(h)
        return f'\u0000{len(ph)-1}\u0000'
    t = re.sub(r'`([^`]+)`', lambda m: put('<code>' + esc(m.group(1)) + '</code>'), t)
    t = re.sub(r'\$\$([^$]+)\$\$', lambda m: put(math_html(m.group(1), True)), t)
    t = re.sub(r'\$([^$]+?)\$', lambda m: put(math_html(m.group(1), False)), t)
    t = esc(t)
    t = re.sub(r'&lt;br\s*/?&gt;', '<br>', t)
    t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'(^|[^*\w])\*(?![\s*])([^*]+?)\*(?!\*)', r'\1<em>\2</em>', t)
    t = re.sub(r'\u0000(\d+)\u0000', lambda m: ph[int(m.group(1))], t)
    return t

def strip_md(s: str) -> str:
    s = s.replace('**', '')
    s = re.sub(r'\$([^$]+)\$', lambda m: tex2plain(m.group(1)), s)
    s = re.sub(r'<br\s*/?>', ' ', s)
    return s.strip()

LI_RE = re.compile(r'^(\s*)([*-]|\d+\.)\s+(.*)$')

class ParseCtx:
    def __init__(self, subj: str):
        self.subj = subj
        self.phase = 0
        self.cb = 0

def render_diagram(code: str, ctx: ParseCtx) -> str:
    code_plain = re.sub(r'\$([^$\n]+)\$', lambda m: tex2plain(m.group(1)), code)
    lines = code_plain.split('\n')
    if any(l.strip().startswith('□ ') for l in lines):
        out = '<div class="check-box-wrap"><div class="dg-bar"><span>☑️ 백지 유도 자가 점검 체크리스트</span><span class="cb-stat">직접 백지에 써본 뒤 체크하세요</span></div><div class="cb-body">'
        for l in lines:
            s = l.strip()
            if not s:
                continue
            if s.startswith('□ '):
                key = f"{ctx.subj}:cb:{ctx.cb}"
                ctx.cb += 1
                txt = esc(s[2:].strip())
                out += f'<label class="cb-item" data-cbkey="{esc(key)}"><input type="checkbox"><span>{txt}</span></label>'
            else:
                out += f'<div class="cb-group-title">{esc(s)}</div>'
        out += '</div></div>'
        return out
    return f'<figure class="diagram"><div class="dg-bar"><span>🗺️ 구조도 <span class="hint">· 옆으로 밀어서 보기 ↔</span></span></div><pre><code>{esc(code_plain)}</code></pre></figure>'

def render_list(lines):
    root = {'children': []}
    stack = [{'key': (-1, -1), 'node': root}]
    for l in lines:
        m = LI_RE.match(l)
        indent = len(m.group(1).replace('\t', '  '))
        ordered = bool(re.search(r'\d', m.group(2)))
        text = m.group(3)
        key = (indent, 0 if ordered else (1 if text.startswith('**') else 2))
        while len(stack) > 1 and stack[-1]['key'] >= key:
            stack.pop()
        node = {'ordered': ordered, 'num': int(m.group(2)[:-1]) if ordered else 1, 'text': text, 'children': []}
        stack[-1]['node']['children'].append(node)
        stack.append({'key': key, 'node': node})

    def build(nodes):
        html = ''
        k = 0
        while k < len(nodes):
            ord_flag = nodes[k]['ordered']
            start = nodes[k]['num']
            inner = ''
            while k < len(nodes) and nodes[k]['ordered'] == ord_flag:
                n = nodes[k]
                k += 1
                children_html = build(n['children']) if n['children'] else ''
                inner += f"<li>{inline(n['text'])}{children_html}</li>"
            if ord_flag:
                start_attr = f' start="{start}"' if start != 1 else ''
                html += f"<ol{start_attr}>{inner}</ol>"
            else:
                html += f"<ul>{inner}</ul>"
        return html

    return build(root['children'])

def split_row(r: str):
    r = r.strip()
    if r.startswith('|'):
        r = r[1:]
    if r.endswith('|'):
        r = r[:-1]
    cells = []
    cur = ''
    in_m = False
    in_c = False
    for k, c in enumerate(r):
        if c == '`' and not in_m:
            in_c = not in_c
        if c == '$' and not in_c and (k == 0 or r[k - 1] != '\\'):
            in_m = not in_m
        if c == '|' and not in_m and not in_c:
            cells.append(cur.strip())
            cur = ''
        else:
            cur += c
    cells.append(cur.strip())
    return cells

def cell_html(raw: str, subkey_prefix: str = '') -> str:
    pieces = [s.strip() for s in re.split(r'<br\s*/?>', raw) if s.strip()]
    if any(p.startswith('•') for p in pieces):
        out = ''
        open_ul = False
        idx = 0
        for p in pieces:
            if p.startswith('•'):
                if not open_ul:
                    out += '<ul class="cell-list">'
                    open_ul = True
                item_txt = inline(re.sub(r'^•\s*', '', p))
                if subkey_prefix:
                    out += f'<li class="sub-task" data-subkey="{esc(subkey_prefix + ":" + str(idx))}">{item_txt}</li>'
                    idx += 1
                else:
                    out += f'<li>{item_txt}</li>'
            else:
                if open_ul:
                    out += '</ul>'
                    open_ul = False
                out += f'<div class="cl">{inline(p)}</div>'
        if open_ul:
            out += '</ul>'
        return out
    if len(pieces) > 1:
        return ''.join(f'<div class="cl">{inline(p)}</div>' for p in pieces)
    return inline(raw)

def render_roadmap(head, body, ctx: ParseCtx) -> str:
    period_idx = next((i for i, h in enumerate(head) if '기간' in h), -1)
    gate_idx = next((i for i, h in enumerate(head) if '통과' in h), -1)
    h = '<div class="roadmap">'
    for n, r in enumerate(body):
        key = f"{ctx.subj}:{ctx.phase}"
        ctx.phase += 1
        t = re.sub(r'^\*\*|\*\*$', '', r[0] if r else '')
        m = re.match(r'^(Phase\s*\d+)\s*[:：]\s*(.*)$', t, re.I)
        badge = m.group(1) if m else f"{n + 1}단계"
        title = m.group(2) if m else t
        fields = ''
        for ci, hd in enumerate(head):
            if ci in (0, period_idx, gate_idx):
                continue
            val = r[ci] if ci < len(r) else ''
            fields += f'<div class="phase-field"><div class="pf-label">📝 {esc(strip_md(hd))}</div>{cell_html(val, key)}</div>'
        period_html = ''
        if period_idx >= 0 and period_idx < len(r):
            p_txt = re.sub(r'</?div[^>]*>', ' ', cell_html(r[period_idx]))
            period_html = f'<span class="period">⏱ {p_txt}</span>'
        gate_html = ''
        if gate_idx >= 0 and gate_idx < len(r):
            gate_html = f'<div class="phase-gate"><div class="pf-label">🚩 {esc(strip_md(head[gate_idx]))}</div>{cell_html(r[gate_idx])}</div>'
        h += f'<div class="phase" data-key="{esc(key)}"><div class="phase-rail"><span class="dot">{n + 1}</span></div><div class="phase-card"><div class="phase-top"><span class="phase-badge">{esc(badge)}</span>{period_html}</div><h4 class="phase-title">{inline(title)}</h4>{fields}{gate_html}</div></div>'
    h += '</div>'
    return h

def render_table(rows, ctx: ParseCtx) -> str:
    head = split_row(rows[0])
    start_row = 2 if len(rows) > 1 and re.match(r'^\|?\s*:?-{2,}', rows[1]) else 1
    body = [split_row(r) for r in rows[start_row:]]
    if head and head[0] == '단계' and any('통과' in h for h in head):
        return render_roadmap(head, body, ctx)
    wide = len(head) >= 6
    labels = [strip_md(h) for h in head]
    cls = 'wide' if wide else 'cardable'
    h = f'<div class="table-wrap {cls}"><table><thead><tr>' + ''.join(f'<th>{inline(c)}</th>' for c in head) + '</tr></thead><tbody>'
    for r in body:
        h += '<tr>'
        for ci in range(len(head)):
            c = r[ci] if ci < len(r) else ''
            h += f'<td data-label="{esc(labels[ci])}">{cell_html(c) if c else ""}</td>'
        h += '</tr>'
    h += '</tbody></table></div>'
    return h

def is_block_start(l: str) -> bool:
    s = l.strip()
    return bool(
        re.match(r'^#{1,3}\s', s)
        or s.startswith('```')
        or s.startswith('|')
        or re.match(r'^-{3,}$', s)
        or LI_RE.match(l)
        or re.match(r'^\$\$.*\$\$$', s)
    )

def parse_doc(md: str, subj_id: str):
    ctx = ParseCtx(subj_id)
    lines = md.split('\n')
    doc = {'intro': '', 'sections': []}
    cur = None
    html = ''
    i = 0
    n = len(lines)

    def flush():
        nonlocal html
        if cur is not None:
            cur['html'] = html
        else:
            doc['intro'] = html
        html = ''

    while i < n:
        line = lines[i]
        s = line.strip()
        if not s or re.match(r'^-{3,}$', s):
            i += 1
            continue
        if re.match(r'^#\s+', s):
            # 최상단 H1 제목은 웹앱 상단 헤더로 자동 표시되므로 인트로 본문에서 안전하게 건너뜀
            i += 1
            continue
        if s.startswith('```'):
            buf = []
            i += 1
            while i < n and not lines[i].strip().startswith('```'):
                buf.append(lines[i])
                i += 1
            i += 1
            while buf and not buf[-1].strip():
                buf.pop()
            html += render_diagram('\n'.join(buf), ctx)
            continue
        m = re.match(r'^##\s+(.*)$', s)
        if m:
            flush()
            cur = {'title': m.group(1), 'html': ''}
            doc['sections'].append(cur)
            i += 1
            continue
        m = re.match(r'^###\s+(.*)$', s)
        if m:
            html += f"<h3>{inline(m.group(1))}</h3>"
            i += 1
            continue
        if re.match(r'^\$\$.*\$\$$', s):
            html += f'<div class="math-block">{math_html(s[2:-2], True)}</div>'
            i += 1
            continue
        if s.startswith('|'):
            rows = []
            while i < n and lines[i].strip().startswith('|'):
                rows.append(lines[i].strip())
                i += 1
            html += render_table(rows, ctx)
            continue
        if LI_RE.match(line):
            items = []
            while i < n:
                l = lines[i]
                if LI_RE.match(l):
                    items.append(l)
                    i += 1
                elif not l.strip():
                    j = i
                    while j < n and not lines[j].strip():
                        j += 1
                    if j < n and LI_RE.match(lines[j]):
                        i = j
                    else:
                        break
                else:
                    break
            html += render_list(items)
            continue
        buf = [s]
        i += 1
        while i < n and lines[i].strip() and not is_block_start(lines[i]):
            buf.append(lines[i].strip())
            i += 1
        html += f"<p>{inline(' '.join(buf))}</p>"

    flush()
    return doc

def first_sentence(html_str: str) -> str:
    t = re.sub(r'<[^>]+>', '', html_str).strip()
    m = re.match(r'^(.+?(?:니다|입니다)\.)', t)
    return m.group(1) if m else t[:120]

def build_static_home(subjects_data, parsed_docs) -> str:
    total_secs = sum(len(d["sections"]) for d in parsed_docs)
    groups = []
    for s, doc in zip(subjects_data, parsed_docs):
        g = next((x for x in groups if x["name"] == s["group"]), None)
        if not g:
            g = {"name": s["group"], "items": []}
            groups.append(g)
        g["items"].append((s, doc))

    out = f'<div class="home-hero"><h1>📚 수능 과목별 학습 가이드</h1><p>문제 풀이에 들어가기 전에 꼭 다져야 할 <b>과목 구조 · 핵심 개념 · 단계별 로드맵</b>을 한곳에 모았어요.</p><div class="hero-stats"><span class="pill">📘 {len(subjects_data)}개 과목</span><span class="pill">🧭 {total_secs}개 장</span></div></div>'
    for g in groups:
        icon = '🔬' if g["name"] == '과학탐구' else '⭐'
        out += f'<div class="group-title">{icon} {esc(g["name"])}</div><div class="cards">'
        for s, doc in g["items"]:
            out += f'<a class="s-card" href="#v-{s["id"]}" style="--c:{s["color"]}"><span class="emo">{s["emoji"]}</span><h3>{esc(s["name"])}</h3><p>{esc(first_sentence(doc["intro"]))}</p><div class="meta"><span>{len(doc["sections"])}개 장</span><span>로드맵 4단계</span></div></a>'
        out += '</div>'
    out += '<div class="group-title">🧭 모든 과목의 공통 학습 흐름</div><div class="flow"><div><b>과목 구조 파악</b><span>단원 사이의 연결(계통도)을 먼저 그려 전체 지도를 머릿속에 넣어요.</span></div><div><b>핵심 개념 체계화</b><span>정의·공식·개념어를 백지에 스스로 써 보며(백지 인출) 빈틈을 찾아요.</span></div><div><b>4단계 로드맵 실행</b><span>단계마다 ‘통과 기준(Gate)’을 넘었는지 확인하고 체크해요.</span></div><div><b>기출 분석 진입</b><span>점수보다 ‘왜 틀렸는지’의 원인을 분류·기록하며 기출을 반복해요.</span></div></div>'
    out += '<div class="tips"><b>💡 미리보기 모드</b><ul><li>지금은 JavaScript가 꺼진 미리보기(파일 앱 등)라서 <b>검색·암기 모드·체크리스트·메모장·다크 모드</b> 기능이 꺼져 있어요.</li><li>오른쪽 위 공유 버튼 → <b>Safari 또는 브라우저로 열기</b>를 하면 모든 인터랙티브 기능을 쓸 수 있어요.</li><li>과목 카드나 목차를 누르면 해당 위치로 이동해요.</li></ul></div>'
    return out

def build_static_subjects(subjects_data, parsed_docs) -> str:
    out = ''
    for idx, (s, doc) in enumerate(zip(subjects_data, parsed_docs)):
        soft = hex_to_soft(s["color"], 0.13)
        secs_html = ''
        toc_chips = ''
        for n, sec in enumerate(doc["sections"]):
            mm = re.match(r'^(\d+)\.\s*(.*)$', sec["title"])
            num = mm.group(1) if mm else str(n + 1)
            title = mm.group(2) if mm else sec["title"]
            plain = strip_md(title)
            short_plain = re.sub(r'\s*\(.*?\)\s*', ' ', plain).strip()
            toc_chips += f'<a class="chip" href="#sec-{s["id"]}-{n}"><span class="n">{num}</span>{esc(short_plain)}</a>'
            is_road = 'class="roadmap"' in sec["html"]
            badge = '<span class="sec-badge">✅ 체크리스트</span>' if is_road else ''
            secs_html += f'<section class="sec" id="sec-{s["id"]}-{n}" data-n="{n}"><div class="sec-head"><span class="sec-num">{num}</span><span class="sec-title">{inline(title)}</span>{badge}</div><div class="sec-body">{sec["html"]}</div></section>'
        prev_s = subjects_data[idx - 1] if idx > 0 else None
        next_s = subjects_data[idx + 1] if idx + 1 < len(subjects_data) else None
        prev_html = f'<a class="prev" href="#v-{prev_s["id"]}"><small>← 이전 과목</small><b>{prev_s["emoji"]} {esc(prev_s["name"])}</b></a>' if prev_s else '<a class="prev" href="#home"><small>← 처음으로</small><b>🏠 과목 목록</b></a>'
        next_html = f'<a class="next" href="#v-{next_s["id"]}"><small>다음 과목 →</small><b>{next_s["emoji"]} {esc(next_s["name"])}</b></a>' if next_s else '<a class="next" href="#home"><small>처음으로 →</small><b>🏠 과목 목록</b></a>'
        out += f'<article class="view subject" id="v-{s["id"]}" style="--accent:{s["color"]};--accent-soft:{soft}"><div class="s-hero"><span class="tag">{esc(s["group"])}</span><h1><span>{s["emoji"]}</span>{esc(s["name"])}</h1><div class="intro">{doc["intro"]}</div></div><div class="layout"><nav class="toc" aria-label="목차"><div class="toc-scroll">{toc_chips}</div></nav><div class="content">{secs_html}<div class="pn">{prev_html}{next_html}</div></div></div></article>'
    return out

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="ko" class="no-js">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <meta name="robots" content="noindex, nofollow">
  <meta name="theme-color" content="#f6f7fb" media="(prefers-color-scheme: light)">
  <meta name="theme-color" content="#0f1218" media="(prefers-color-scheme: dark)">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="default">
  <meta name="apple-mobile-web-app-title" content="수능 가이드">
  <link rel="apple-touch-icon" href="apple-touch-icon.png">
  <link rel="icon" type="image/png" href="apple-touch-icon.png">
  <link rel="manifest" href="manifest.json">
  <title>수능 과목별 학습 가이드 (고2 맞춤형 업그레이드)</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css" crossorigin="anonymous">
  <style>
    :root {
      --fs: 17px;
      --bg: #f6f7fb;
      --card: #ffffff;
      --card2: #f9fafc;
      --text: #1f2430;
      --muted: #667085;
      --line: #e4e7ec;
      --shadow: 0 1px 2px rgba(16, 24, 40, .06), 0 4px 14px rgba(16, 24, 40, .06);
      --accent: #4c6ef5;
      --accent-soft: rgba(76, 110, 245, .12);
      --hh: 56px;
      --radius: 16px;
      --mono: "SF Mono", ui-monospace, Menlo, Consolas, "D2Coding", "Nanum Gothic Coding", monospace;
    }

    html[data-theme="dark"] {
      --bg: #0f1218;
      --card: #181c25;
      --card2: #1e2330;
      --text: #e6e8ee;
      --muted: #98a2b3;
      --line: #2a3040;
      --shadow: 0 1px 2px rgba(0, 0, 0, .4), 0 6px 18px rgba(0, 0, 0, .35);
      color-scheme: dark;
    }

    * {
      box-sizing: border-box
    }

    html {
      font-size: var(--fs);
      -webkit-text-size-adjust: 100%;
      scroll-behavior: smooth;
      overflow-x: hidden
    }

    body {
      margin: 0;
      background: var(--bg);
      color: var(--text);
      font-family: -apple-system, BlinkMacSystemFont, "Apple SD Gothic Neo", "Pretendard", "Noto Sans KR", "Malgun Gothic", "Segoe UI", Roboto, sans-serif;
      line-height: 1.75;
      word-break: keep-all;
      word-wrap: break-word;
      overflow-wrap: break-word;
      overflow-wrap: anywhere;
      -webkit-tap-highlight-color: transparent;
      padding-bottom: env(safe-area-inset-bottom);
      /* overflow-x:hidden 은 body를 스크롤 컨테이너로 만들어 Safari에서 sticky(상단바·목차)가 깨짐 → clip 사용 */
      overflow-x: clip
    }

    button {
      font: inherit;
      color: inherit;
      cursor: pointer
    }

    a {
      color: var(--accent)
    }

    strong {
      font-weight: 700;
      color: var(--text);
      background: linear-gradient(transparent 62%, var(--accent-soft) 62%)
    }

    em {
      font-style: normal;
      font-weight: 600;
      color: var(--accent)
    }

    code {
      font-family: var(--mono);
      font-size: .86em;
      background: var(--accent-soft);
      padding: .1em .38em;
      border-radius: 6px
    }

    /* ---------- App bar ---------- */
    .appbar {
      position: sticky;
      top: 0;
      z-index: 50;
      height: calc(var(--hh) + env(safe-area-inset-top));
      padding: env(safe-area-inset-top) max(10px, env(safe-area-inset-right)) 0 max(10px, env(safe-area-inset-left));
      display: flex;
      align-items: center;
      gap: 4px;
      background: color-mix(in srgb, var(--bg) 82%, transparent);
      background: var(--bg);
      -webkit-backdrop-filter: saturate(180%) blur(14px);
      backdrop-filter: saturate(180%) blur(14px);
      border-bottom: 1px solid var(--line)
    }

    @supports (backdrop-filter:blur(1px)) or (-webkit-backdrop-filter:blur(1px)) {
      .appbar {
        background: color-mix(in srgb, var(--bg) 80%, transparent)
      }
    }

    .appbar .title {
      flex: 1;
      min-width: 0;
      font-weight: 800;
      font-size: 1.02rem;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      display: flex;
      align-items: center;
      gap: .4em;
      background: none;
      border: 0;
      padding: 6px 4px;
      text-align: left
    }

    .icon-btn {
      width: 40px;
      height: 40px;
      flex: 0 0 auto;
      border: 0;
      border-radius: 12px;
      background: transparent;
      display: grid;
      place-items: center;
      font-size: 1.1rem;
      transition: background .15s, color .15s
    }

    .icon-btn:hover,
    .icon-btn:focus-visible {
      background: var(--accent-soft)
    }

    .icon-btn.active {
      background: var(--accent);
      color: #fff
    }

    .icon-btn svg {
      width: 21px;
      height: 21px;
      stroke: currentColor;
      fill: none;
      stroke-width: 2;
      stroke-linecap: round;
      stroke-linejoin: round
    }

    .fs-btn {
      font-weight: 800;
      font-size: .88rem
    }

    #readbar {
      position: fixed;
      left: 0;
      top: calc(var(--hh) + env(safe-area-inset-top) - 3px);
      height: 3px;
      width: 0;
      background: var(--accent);
      z-index: 60;
      transition: width .1s linear
    }

    main {
      max-width: 1180px;
      margin: 0 auto;
      padding: 0 max(16px, env(safe-area-inset-right)) 40px max(16px, env(safe-area-inset-left))
    }

    .view {
      display: none
    }

    .view.on {
      display: block;
      animation: fade .35s ease
    }

    @keyframes fade {
      from {
        opacity: 0;
        transform: translateY(8px)
      }

      to {
        opacity: 1;
        transform: none
      }
    }

    /* ---------- Home ---------- */
    .home-hero {
      margin: 22px 0 18px;
      padding: 28px 24px;
      border-radius: 24px;
      color: #fff;
      background: linear-gradient(135deg, #4c6ef5 0%, #7048e8 55%, #c2255c 100%);
      box-shadow: var(--shadow);
      position: relative;
      overflow: hidden
    }

    .home-hero::after {
      content: "";
      position: absolute;
      right: -60px;
      top: -60px;
      width: 220px;
      height: 220px;
      border-radius: 50%;
      background: rgba(255, 255, 255, .12)
    }

    .home-hero h1 {
      margin: 0 0 6px;
      font-size: 1.65rem;
      line-height: 1.3
    }

    .home-hero p {
      margin: 0;
      opacity: .93
    }

    .hero-stats {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      margin-top: 18px;
      position: relative;
      z-index: 1
    }

    .pill {
      display: inline-flex;
      align-items: center;
      gap: .4em;
      padding: .35em .8em;
      border-radius: 999px;
      background: rgba(255, 255, 255, .18);
      font-size: .86rem;
      font-weight: 600
    }

    .pill button,
    .pill input {
      background: transparent;
      border: 0;
      color: inherit;
      font: inherit;
      padding: 0
    }

    .pill.clickable {
      cursor: pointer;
      transition: background .15s
    }

    .pill.clickable:hover {
      background: rgba(255, 255, 255, .28)
    }

    .pill input[type=date] {
      -webkit-appearance: none;
      appearance: none;
      color-scheme: dark;
      display: inline-block;
      min-width: 7.5em;
      max-width: 9.5em;
      min-height: 1.5em;
      line-height: 1.5;
      padding: 0;
      margin: 0
    }

    .pill input[type=date]::-webkit-date-and-time-value {
      text-align: left;
      min-height: 1.5em
    }

    .overall {
      margin-top: 16px;
      position: relative;
      z-index: 1
    }

    .overall .bar {
      height: 10px;
      border-radius: 99px;
      background: rgba(255, 255, 255, .25);
      overflow: hidden
    }

    .overall .bar i {
      display: block;
      height: 100%;
      width: 0;
      background: #fff;
      border-radius: 99px;
      transition: width .6s ease
    }

    .overall small {
      display: block;
      margin-top: 6px;
      opacity: .92
    }

    .group-title {
      margin: 28px 4px 12px;
      font-size: 1.05rem;
      font-weight: 800;
      display: flex;
      align-items: center;
      gap: .5em
    }

    .group-title::after {
      content: "";
      flex: 1;
      height: 1px;
      background: var(--line)
    }

    .cards {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 14px
    }

    @media (max-width:1060px) {
      .cards {
        grid-template-columns: repeat(2, 1fr)
      }
    }

    .s-card {
      position: relative;
      text-align: left;
      border: 1px solid var(--line);
      background: var(--card);
      border-radius: var(--radius);
      padding: 18px 18px 16px;
      box-shadow: var(--shadow);
      transition: transform .18s ease, box-shadow .18s ease;
      overflow: hidden;
      isolation: isolate;
      will-change: transform;
      display: flex;
      flex-direction: column;
      gap: 8px;
      min-height: 190px
    }

    .s-card::before {
      content: "";
      position: absolute;
      inset: 0 0 auto 0;
      height: 5px;
      background: var(--c)
    }

    .s-card:hover {
      transform: translateY(-3px);
      box-shadow: 0 10px 26px rgba(16, 24, 40, .12)
    }

    .s-card:active {
      transform: scale(.98)
    }

    .s-card-top {
      display: flex;
      align-items: center;
      justify-content: space-between
    }

    .s-card .emo {
      font-size: 2rem;
      line-height: 1
    }

    .s-card .memo-dot {
      font-size: .76rem;
      font-weight: 700;
      padding: .15em .55em;
      border-radius: 99px;
      background: var(--accent-soft);
      color: var(--accent);
      display: none
    }

    .s-card .memo-dot.on {
      display: inline-block
    }

    .s-card h3 {
      margin: 0;
      font-size: 1.2rem
    }

    .s-card p {
      margin: 0;
      color: var(--muted);
      font-size: .88rem;
      line-height: 1.6;
      display: -webkit-box;
      -webkit-line-clamp: 3;
      -webkit-box-orient: vertical;
      overflow: hidden
    }

    .s-card .meta {
      margin-top: auto;
      display: flex;
      justify-content: space-between;
      font-size: .8rem;
      color: var(--muted);
      font-weight: 600
    }

    .mini-bar {
      height: 6px;
      border-radius: 99px;
      background: var(--line);
      overflow: hidden
    }

    .mini-bar i {
      display: block;
      height: 100%;
      width: 0;
      background: var(--c);
      transition: width .5s ease
    }

    .flow {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 12px;
      counter-reset: f
    }

    .flow div {
      background: var(--card);
      border: 1px solid var(--line);
      border-radius: var(--radius);
      padding: 16px;
      box-shadow: var(--shadow);
      position: relative
    }

    .flow div b {
      display: block;
      font-size: 1rem;
      margin-bottom: 4px
    }

    .flow div span {
      color: var(--muted);
      font-size: .88rem;
      line-height: 1.6;
      display: block
    }

    .flow div::before {
      counter-increment: f;
      content: counter(f);
      display: inline-grid;
      place-items: center;
      width: 28px;
      height: 28px;
      border-radius: 50%;
      background: #4c6ef5;
      color: #fff;
      font-weight: 800;
      font-size: .85rem;
      margin-bottom: 8px
    }

    .tips {
      margin-top: 14px;
      background: var(--card);
      border: 1px dashed var(--line);
      border-radius: var(--radius);
      padding: 14px 18px;
      color: var(--muted);
      font-size: .9rem
    }

    .tips ul {
      margin: .3em 0 0;
      padding-left: 1.2em
    }

    /* ---------- Subject ---------- */
    .s-hero {
      margin: 20px 0 14px;
      padding: 24px 22px;
      border-radius: 24px;
      background: var(--card);
      border: 1px solid var(--line);
      box-shadow: var(--shadow);
      position: relative;
      overflow: hidden
    }

    .s-hero::before {
      content: "";
      position: absolute;
      inset: 0;
      background: linear-gradient(135deg, var(--accent-soft), transparent 60%);
      pointer-events: none
    }

    .s-hero>* {
      position: relative
    }

    .s-hero .tag {
      display: inline-block;
      font-size: .78rem;
      font-weight: 700;
      color: var(--accent);
      background: var(--accent-soft);
      padding: .2em .7em;
      border-radius: 99px
    }

    .s-hero h1 {
      margin: 8px 0 10px;
      font-size: 1.75rem;
      line-height: 1.25;
      display: flex;
      align-items: center;
      gap: .35em
    }

    .s-hero .intro p {
      margin: .5em 0;
      font-size: 1rem
    }

    .s-hero .prog {
      display: flex;
      align-items: center;
      gap: 12px;
      margin-top: 14px;
      font-size: .86rem;
      font-weight: 600;
      color: var(--muted)
    }

    .s-hero .prog .mini-bar {
      flex: 1;
      --c: var(--accent)
    }

    .layout {
      display: block
    }

    .content {
      min-width: 0
    }

    .toc {
      position: sticky;
      top: calc(var(--hh) + env(safe-area-inset-top));
      z-index: 30;
      margin: 0 calc(-1 * max(16px, env(safe-area-inset-left)));
      padding: 8px max(16px, env(safe-area-inset-left));
      background: var(--bg);
      border-bottom: 1px solid var(--line);
      display: flex;
      gap: 8px;
      align-items: center
    }

    .toc-scroll {
      display: flex;
      gap: 8px;
      overflow-x: auto;
      scrollbar-width: none;
      flex: 1;
      scroll-behavior: smooth;
      -webkit-overflow-scrolling: touch
    }

    .toc-scroll::-webkit-scrollbar {
      display: none
    }

    .chip {
      flex: 0 0 auto;
      border: 1px solid var(--line);
      background: var(--card);
      border-radius: 999px;
      padding: .38em .9em;
      font-size: .84rem;
      font-weight: 600;
      white-space: nowrap;
      color: var(--muted);
      transition: all .2s
    }

    .chip.active {
      background: var(--accent);
      border-color: var(--accent);
      color: #fff
    }

    .chip .n {
      opacity: .7;
      margin-right: .3em
    }

    .toc-tools {
      display: flex;
      gap: 5px;
      flex: 0 0 auto
    }

    .toc-tools button {
      border: 1px solid var(--line);
      background: var(--card);
      border-radius: 10px;
      padding: .32em .65em;
      font-size: .78rem;
      font-weight: 700;
      color: var(--muted);
      white-space: nowrap;
      transition: all .15s
    }

    .toc-tools button.active {
      background: var(--accent);
      border-color: var(--accent);
      color: #fff
    }

    .toc-label {
      display: none
    }

    .sec {
      background: var(--card);
      border: 1px solid var(--line);
      border-radius: var(--radius);
      box-shadow: var(--shadow);
      margin: 16px 0;
      scroll-snap-margin-top: calc(var(--hh) + 70px);
      scroll-margin-top: calc(var(--hh) + 70px);
      overflow: hidden
    }

    .sec-head {
      width: 100%;
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 16px 18px;
      border: 0;
      background: transparent;
      text-align: left;
      font-size: 1.12rem;
      font-weight: 800;
      line-height: 1.45
    }

    .sec-num {
      flex: 0 0 auto;
      width: 34px;
      height: 34px;
      border-radius: 11px;
      display: grid;
      place-items: center;
      background: var(--accent);
      color: #fff;
      font-size: .95rem
    }

    .sec-title {
      flex: 1
    }

    .sec-badge {
      flex: 0 0 auto;
      font-size: .72rem;
      font-weight: 700;
      color: var(--accent);
      background: var(--accent-soft);
      padding: .15em .6em;
      border-radius: 99px
    }

    .chev {
      flex: 0 0 auto;
      width: 12px;
      height: 12px;
      border-right: 2.5px solid var(--muted);
      border-bottom: 2.5px solid var(--muted);
      transform: rotate(45deg);
      transition: transform .25s;
      margin: 0 4px 6px
    }

    .sec.collapsed .chev {
      transform: rotate(-45deg);
      margin-bottom: 0
    }

    .sec-body {
      padding: 0 20px 20px;
      border-top: 1px solid var(--line);
      overflow-x: auto
    }

    .sec.collapsed .sec-body {
      display: none
    }

    .sec-body>p {
      margin: 1em 0
    }

    .sec-body h3 {
      font-size: 1.05rem;
      margin: 1.6em 0 .7em;
      padding-left: .7em;
      border-left: 4px solid var(--accent);
      line-height: 1.5
    }

    .sec-body ul,
    .sec-body ol {
      padding-left: 1.35em;
      margin: .6em 0
    }

    .sec-body li {
      margin: .35em 0
    }

    .sec-body li::marker {
      color: var(--accent);
      font-weight: 700
    }

    .sec-body li>ul,
    .sec-body li>ol {
      margin: .3em 0 .6em
    }

    .sec-body li>ul>li {
      color: var(--text)
    }

    .sec-body>ul>li,
    .sec-body>ol>li {
      padding: 2px 0
    }

    .sec-body>ol>li>ul,
    .sec-body>ul>li>ul {
      background: var(--card2);
      border-radius: 12px;
      padding: .5em .8em .5em 1.8em;
      border: 1px solid var(--line)
    }

    .sec-body ul ul ul {
      background: none;
      border: 0;
      padding: 0 0 0 1.2em
    }

    /* diagram & interactive checklist */
    .diagram,
    .check-box-wrap {
      margin: 1.1em 0;
      border: 1px solid var(--line);
      border-radius: 14px;
      background: var(--card2);
      overflow: hidden
    }

    .dg-bar {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
      padding: 6px 10px 6px 14px;
      border-bottom: 1px solid var(--line);
      font-size: .78rem;
      font-weight: 700;
      color: var(--muted)
    }

    .dg-bar .hint {
      font-weight: 500;
      opacity: .85;
      display: none
    }

    .diagram.overflow .dg-bar .hint {
      display: inline
    }

    .dg-bar button {
      border: 1px solid var(--line);
      background: var(--card);
      border-radius: 8px;
      padding: .2em .6em;
      font-size: .76rem;
      font-weight: 700;
      color: var(--muted)
    }

    .diagram pre {
      margin: 0;
      padding: 14px 16px;
      overflow-x: auto;
      font-family: var(--mono);
      font-size: .8rem;
      line-height: 1.65;
      -webkit-overflow-scrolling: touch;
      tab-size: 2
    }

    .diagram.wrap pre {
      white-space: pre-wrap;
      word-break: break-all
    }

    .diagram code {
      background: none;
      padding: 0;
      font-size: inherit
    }

    .cb-body {
      padding: 10px 14px 14px
    }

    .cb-group-title {
      font-weight: 800;
      font-size: .88rem;
      color: var(--accent);
      margin: 12px 0 6px;
      padding: 0 2px
    }

    .cb-group-title:first-child {
      margin-top: 2px
    }

    .cb-item {
      display: flex;
      align-items: flex-start;
      gap: 10px;
      padding: 9px 12px;
      margin: 6px 0;
      background: var(--card);
      border: 1px solid var(--line);
      border-radius: 10px;
      cursor: pointer;
      font-size: .88rem;
      line-height: 1.5;
      transition: all .18s;
      user-select: none;
      -webkit-user-select: none
    }

    .cb-item:hover {
      border-color: var(--accent)
    }

    .cb-item input {
      width: 18px;
      height: 18px;
      margin: 2px 0 0;
      accent-color: var(--accent);
      flex: 0 0 auto
    }

    .cb-item.checked {
      background: var(--accent-soft);
      border-color: var(--accent)
    }

    .cb-item.checked span {
      text-decoration: line-through;
      opacity: .75
    }

    /* tables */
    .table-wrap {
      margin: 1.1em 0;
      overflow-x: auto;
      border: 1px solid var(--line);
      border-radius: 14px;
      -webkit-overflow-scrolling: touch
    }

    table {
      border-collapse: collapse;
      width: 100%;
      font-size: .9rem;
      line-height: 1.6
    }

    th,
    td {
      padding: 10px 12px;
      border-bottom: 1px solid var(--line);
      vertical-align: top;
      text-align: left
    }

    th {
      background: var(--accent-soft);
      font-weight: 800;
      white-space: nowrap;
      font-size: .85rem
    }

    tbody tr:last-child td {
      border-bottom: 0
    }

    tbody tr:nth-child(even) td {
      background: var(--card2)
    }

    td+td,
    th+th {
      border-left: 1px solid var(--line)
    }

    .wide table {
      min-width: 760px
    }

    .wide th,
    .wide td {
      white-space: nowrap;
      text-align: center
    }

    .cell-list {
      margin: 0 !important;
      padding-left: 1.1em !important
    }

    .cell-list li {
      margin: .15em 0 !important
    }

    .cl+.cl {
      margin-top: .45em
    }

    /* roadmap & interactive sub-tasks */
    .roadmap {
      margin: 1.2em 0;
      position: relative
    }

    .phase {
      display: grid;
      grid-template-columns: 40px 1fr;
      gap: 12px;
      position: relative
    }

    .phase-rail {
      position: relative;
      display: flex;
      justify-content: center
    }

    .phase-rail::before {
      content: "";
      position: absolute;
      top: 0;
      bottom: 0;
      width: 3px;
      background: var(--line);
      border-radius: 3px
    }

    .phase:first-child .phase-rail::before {
      top: 20px
    }

    .phase:last-child .phase-rail::before {
      bottom: calc(100% - 20px)
    }

    .dot {
      position: relative;
      margin-top: 8px;
      width: 34px;
      height: 34px;
      border-radius: 50%;
      display: grid;
      place-items: center;
      font-weight: 800;
      font-size: .9rem;
      background: var(--card);
      border: 3px solid var(--accent);
      color: var(--accent);
      transition: all .3s
    }

    .phase.done .dot {
      background: var(--accent);
      color: #fff
    }

    .phase.done .dot::after {
      content: "✓";
      position: absolute;
      inset: 0;
      display: grid;
      place-items: center;
      background: var(--accent);
      border-radius: 50%
    }

    .phase-card {
      background: var(--card2);
      border: 1px solid var(--line);
      border-radius: 14px;
      padding: 14px 16px;
      margin-bottom: 14px;
      transition: all .3s
    }

    .phase.done .phase-card {
      border-color: var(--accent);
      box-shadow: 0 0 0 3px var(--accent-soft)
    }

    .phase-top {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      align-items: center
    }

    .phase-badge {
      font-size: .75rem;
      font-weight: 800;
      color: #fff;
      background: var(--accent);
      padding: .15em .65em;
      border-radius: 99px
    }

    .period {
      font-size: .8rem;
      font-weight: 700;
      color: var(--muted);
      background: var(--card);
      border: 1px solid var(--line);
      padding: .1em .6em;
      border-radius: 99px
    }

    .phase-title {
      margin: 8px 0 6px;
      font-size: 1.02rem;
      line-height: 1.5
    }

    .pf-label {
      font-size: .76rem;
      font-weight: 800;
      color: var(--muted);
      letter-spacing: .02em;
      margin: 10px 0 4px
    }

    .phase-field {
      font-size: .92rem
    }

    .phase-field ul {
      margin: .2em 0
    }

    .phase-field .cell-list:has(.sub-task) {
      padding-left: 0 !important;
      list-style: none
    }

    .phase-field .sub-task {
      list-style: none;
      cursor: pointer;
      padding: 5px 8px;
      margin: 4px 0 !important;
      border-radius: 8px;
      background: var(--card);
      border: 1px solid var(--line);
      display: flex;
      align-items: flex-start;
      gap: 8px;
      user-select: none;
      -webkit-user-select: none;
      transition: all .15s
    }

    .phase-field .sub-task:hover {
      border-color: var(--accent)
    }

    .phase-field .sub-task::before {
      content: "☐";
      color: var(--accent);
      font-weight: 800;
      flex: 0 0 auto;
      line-height: 1.4
    }

    .phase-field .sub-task.checked {
      background: var(--accent-soft);
      border-color: var(--accent);
      text-decoration: line-through;
      color: var(--muted)
    }

    .phase-field .sub-task.checked::before {
      content: "☑️";
      text-decoration: none
    }

    .phase-gate {
      margin-top: 10px;
      padding: 10px 12px;
      border-radius: 12px;
      background: var(--accent-soft);
      font-size: .92rem
    }

    .phase-gate .pf-label {
      margin-top: 0;
      color: var(--accent)
    }

    .phase-check {
      margin-top: 12px;
      display: flex;
      align-items: center;
      gap: 10px;
      font-weight: 700;
      font-size: .92rem;
      cursor: pointer;
      user-select: none;
      -webkit-user-select: none;
      padding: 8px 10px;
      border-radius: 12px;
      border: 1.5px dashed var(--line)
    }

    .phase.done .phase-check {
      border-style: solid;
      border-color: var(--accent);
      color: var(--accent)
    }

    .phase-check input {
      width: 22px;
      height: 22px;
      accent-color: var(--accent);
      margin: 0
    }

    /* ---------- Quiz / Blind Mode (암기 테스트 모드) ---------- */
    .quiz-banner {
      display: none;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
      margin: 12px 0;
      padding: 10px 16px;
      border-radius: 14px;
      background: var(--accent-soft);
      border: 1px solid var(--accent);
      font-size: .88rem;
      font-weight: 600
    }

    body.quiz-mode .quiz-banner {
      display: flex
    }

    .quiz-banner-btns {
      display: flex;
      gap: 6px;
      flex: 0 0 auto
    }

    .quiz-banner-btns button {
      border: 1px solid var(--accent);
      background: var(--card);
      color: var(--accent);
      border-radius: 8px;
      padding: .25em .7em;
      font-size: .78rem;
      font-weight: 700
    }

    body.quiz-mode .quiz-mask {
      background: var(--accent) !important;
      color: transparent !important;
      border-radius: 6px;
      padding: .05em .3em;
      cursor: pointer;
      user-select: none;
      -webkit-user-select: none;
      transition: background .18s ease, color .18s ease;
      box-shadow: inset 0 0 0 1px var(--accent);
      display: inline-block;
      vertical-align: baseline
    }

    body.quiz-mode .quiz-mask * {
      color: transparent !important;
      opacity: 0 !important;
      transition: opacity .18s ease
    }

    body.quiz-mode .quiz-mask.revealed {
      background: var(--accent-soft) !important;
      color: var(--text) !important;
      box-shadow: inset 0 0 0 1px var(--accent)
    }

    body.quiz-mode .quiz-mask.revealed * {
      color: inherit !important;
      opacity: 1 !important
    }

    /* ---------- Subject Memo Box ---------- */
    .memo-sec {
      background: var(--card);
      border: 1px solid var(--line);
      border-radius: var(--radius);
      box-shadow: var(--shadow);
      margin: 16px 0;
      padding: 16px 20px
    }

    .memo-head {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
      margin-bottom: 8px;
      font-weight: 800;
      font-size: 1.02rem
    }

    .memo-head small {
      font-weight: 600;
      font-size: .78rem;
      color: var(--muted)
    }

    .memo-area {
      width: 100%;
      min-height: 92px;
      padding: 12px 14px;
      border-radius: 12px;
      border: 1px solid var(--line);
      background: var(--card2);
      color: var(--text);
      font: inherit;
      font-size: .9rem;
      line-height: 1.6;
      resize: vertical;
      outline: none;
      transition: border-color .2s
    }

    .memo-area:focus {
      border-color: var(--accent);
      box-shadow: 0 0 0 3px var(--accent-soft)
    }

    .math-block {
      margin: 1em 0;
      padding: 12px;
      text-align: center;
      overflow-x: auto;
      background: var(--card2);
      border-radius: 12px;
      border: 1px solid var(--line)
    }

    .m {
      font-family: "Times New Roman", "Cambria Math", serif
    }

    .m.k {
      font-family: inherit
    }

    .m i {
      font-style: italic
    }

    .m .tx {
      font-family: -apple-system, "Apple SD Gothic Neo", "Noto Sans KR", sans-serif;
      font-style: normal
    }

    .fr {
      display: inline-flex;
      flex-direction: column;
      vertical-align: middle;
      text-align: center;
      font-size: .85em;
      line-height: 1.2;
      margin: 0 .15em
    }

    .fr .nu {
      border-bottom: 1px solid currentColor;
      padding: 0 .2em
    }

    .fr .de {
      padding: 0 .2em
    }

    .vec {
      position: relative;
      display: inline-block
    }

    .vec::after {
      content: "→";
      position: absolute;
      left: 0;
      right: 0;
      top: -.85em;
      font-size: .7em;
      text-align: center
    }

    .katex {
      font-size: 1.06em
    }

    .katex-display {
      margin: .3em 0
    }

    .pn {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
      margin: 26px 0 10px
    }

    .pn button,
    .pn a {
      display: block;
      color: inherit;
      text-decoration: none;
      border: 1px solid var(--line);
      background: var(--card);
      border-radius: var(--radius);
      padding: 14px 16px;
      text-align: left;
      box-shadow: var(--shadow);
      min-height: 70px
    }

    .pn button small,
    .pn a small {
      display: block;
      color: var(--muted);
      font-size: .76rem;
      font-weight: 700
    }

    .pn button b,
    .pn a b {
      font-size: 1rem
    }

    .pn .next {
      text-align: right
    }

    .pn button:disabled {
      visibility: hidden
    }

    .flash {
      animation: flash 2.2s ease
    }

    @keyframes flash {

      0%,
      40% {
        background: rgba(255, 212, 59, .55);
        box-shadow: 0 0 0 4px rgba(255, 212, 59, .55)
      }

      100% {
        background: transparent;
        box-shadow: none
      }
    }

    /* ---------- Search & Backup Modals ---------- */
    .search {
      position: fixed;
      inset: 0;
      z-index: 100;
      background: rgba(10, 12, 18, .45);
      display: none;
      align-items: flex-start;
      justify-content: center;
      padding: calc(env(safe-area-inset-top) + 12px) 12px 12px;
      -webkit-backdrop-filter: blur(4px);
      backdrop-filter: blur(4px)
    }

    .search.on {
      display: flex
    }

    .search-box {
      width: 100%;
      max-width: 720px;
      max-height: 100%;
      display: flex;
      flex-direction: column;
      background: var(--card);
      border-radius: 20px;
      box-shadow: 0 20px 60px rgba(0, 0, 0, .3);
      overflow: hidden;
      border: 1px solid var(--line)
    }

    .search-in {
      display: flex;
      align-items: center;
      gap: 8px;
      flex: 0 0 auto;
      padding: 10px 10px 10px 16px;
      border-bottom: 1px solid var(--line)
    }

    .search-in input {
      flex: 1;
      border: 0;
      outline: 0;
      background: transparent;
      font-size: max(16px, 1.05rem);
      color: var(--text);
      padding: 8px 0;
      min-width: 0
    }

    .search-res {
      flex: 1 1 auto;
      min-height: 0;
      overflow-y: auto;
      padding: 6px 8px 12px;
      -webkit-overflow-scrolling: touch
    }

    .res-group {
      margin: 10px 6px 4px;
      font-size: .8rem;
      font-weight: 800;
      color: var(--muted)
    }

    .res {
      display: block;
      width: 100%;
      text-align: left;
      border: 0;
      background: transparent;
      border-radius: 12px;
      padding: 10px 12px;
      font-size: .9rem;
      line-height: 1.55
    }

    .res:hover,
    .res:focus-visible {
      background: var(--accent-soft)
    }

    .res small {
      display: block;
      color: var(--muted);
      font-weight: 700;
      font-size: .76rem;
      margin-bottom: 2px
    }

    .res mark {
      background: #ffe066;
      color: #000;
      border-radius: 3px;
      padding: 0 1px
    }

    .search-empty {
      padding: 28px 16px;
      text-align: center;
      color: var(--muted);
      font-size: .92rem
    }

    .quick {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      justify-content: center;
      margin-top: 12px
    }

    .backup-body {
      padding: 16px 18px;
      overflow-y: auto;
      font-size: .9rem
    }

    .backup-body textarea {
      width: 100%;
      height: 110px;
      padding: 10px 12px;
      border-radius: 12px;
      border: 1px solid var(--line);
      background: var(--card2);
      color: var(--text);
      font-family: var(--mono);
      font-size: .8rem;
      margin: 8px 0 12px;
      resize: vertical
    }

    .backup-actions {
      display: flex;
      flex-wrap: wrap;
      gap: 8px
    }

    .btn-act {
      border: 1px solid var(--line);
      background: var(--card2);
      padding: .45em .9em;
      border-radius: 10px;
      font-size: .85rem;
      font-weight: 700
    }

    .btn-act.pri {
      background: var(--accent);
      border-color: var(--accent);
      color: #fff
    }

    .btn-act.danger {
      color: #e03131;
      border-color: rgba(224, 49, 49, .35)
    }

    #totop {
      position: fixed;
      right: max(16px, env(safe-area-inset-right));
      bottom: calc(18px + env(safe-area-inset-bottom));
      z-index: 40;
      width: 48px;
      height: 48px;
      border-radius: 50%;
      border: 0;
      background: var(--accent);
      color: #fff;
      box-shadow: 0 6px 18px rgba(0, 0, 0, .25);
      font-size: 1.3rem;
      opacity: 0;
      pointer-events: none;
      transform: translateY(10px);
      transition: all .25s
    }

    #totop.on {
      opacity: 1;
      pointer-events: auto;
      transform: none
    }

    .toast {
      position: fixed;
      left: 50%;
      bottom: calc(84px + env(safe-area-inset-bottom));
      transform: translateX(-50%) translateY(20px);
      background: #1f2430;
      color: #fff;
      padding: 10px 18px;
      border-radius: 999px;
      font-size: .9rem;
      font-weight: 600;
      opacity: 0;
      pointer-events: none;
      transition: all .3s;
      z-index: 120;
      white-space: nowrap
    }

    .toast.on {
      opacity: 1;
      transform: translateX(-50%)
    }

    footer {
      text-align: center;
      color: var(--muted);
      font-size: .8rem;
      padding: 20px 0 30px
    }

    /* ---------- Static preview (JavaScript 꺼진 뷰어: 파일 앱 미리보기 등) ---------- */
    a.s-card,
    a.chip {
      color: var(--text);
      text-decoration: none
    }

    a.chip {
      color: var(--muted)
    }

    .no-js .view {
      display: block
    }

    .no-js .view.subject {
      margin-top: 36px;
      padding-top: 4px;
      border-top: 2px dashed var(--line)
    }

    .no-js .view.subject,
    .no-js #home {
      scroll-margin-top: calc(var(--hh) + 8px)
    }

    .no-js .appbar .icon-btn,
    .no-js #totop,
    .no-js #readbar {
      display: none
    }

    .no-js .sec-head {
      cursor: default
    }

    /* ---------- Responsive ---------- */
    @media (max-width:760px) {
      :root {
        --hh: 54px
      }

      .home-hero {
        padding: 22px 18px;
        border-radius: 20px
      }

      .home-hero h1 {
        font-size: 1.4rem
      }

      .s-hero {
        padding: 20px 16px;
        border-radius: 20px
      }

      .s-hero h1 {
        font-size: 1.45rem
      }

      .sec-head {
        padding: 14px 14px;
        font-size: 1.02rem;
        gap: 10px
      }

      .sec-num {
        width: 30px;
        height: 30px;
        font-size: .85rem;
        border-radius: 9px
      }

      .sec-badge {
        display: none
      }

      .sec-body {
        padding: 0 14px 16px
      }

      .sec-body>ol>li>ul,
      .sec-body>ul>li>ul {
        padding-left: 1.5em
      }

      .cards {
        grid-template-columns: 1fr 1fr;
        gap: 10px
      }

      .s-card {
        min-height: 0;
        padding: 14px 14px 12px
      }

      .s-card p {
        -webkit-line-clamp: 2;
        font-size: .82rem
      }

      .s-card .emo {
        font-size: 1.6rem
      }

      .s-card h3 {
        font-size: 1.05rem
      }

      .phase {
        grid-template-columns: 30px 1fr;
        gap: 8px
      }

      .dot {
        width: 28px;
        height: 28px;
        font-size: .8rem;
        border-width: 2.5px
      }

      .phase-card {
        padding: 12px 13px
      }

      .diagram pre {
        font-size: .72rem;
        padding: 12px
      }

      .quiz-banner {
        flex-direction: column;
        align-items: flex-start
      }

      /* table -> cards */
      .cardable {
        border: 0;
        overflow: visible
      }

      .cardable table,
      .cardable tbody,
      .cardable tr,
      .cardable td {
        display: block;
        width: 100%
      }

      .cardable thead {
        display: none
      }

      .cardable tr {
        border: 1px solid var(--line);
        border-radius: 14px;
        margin: 0 0 12px;
        overflow: hidden;
        background: var(--card)
      }

      .cardable tbody tr:nth-child(even) td {
        background: transparent
      }

      .cardable td {
        border: 0 !important;
        border-top: 1px solid var(--line) !important;
        padding: 10px 14px
      }

      .cardable td:first-child {
        border-top: 0 !important;
        background: var(--accent-soft) !important;
        font-weight: 700;
        font-size: .98rem
      }

      .cardable td:not(:first-child)::before {
        content: attr(data-label);
        display: block;
        font-size: .74rem;
        font-weight: 800;
        color: var(--accent);
        margin-bottom: 2px
      }

      .cardable td:empty {
        display: none
      }
    }

    @media (max-width:380px) {
      .cards {
        grid-template-columns: 1fr
      }
    }

    @media (prefers-reduced-motion:reduce) {
      * {
        animation: none !important;
        transition: none !important;
        scroll-behavior: auto !important
      }
    }

    @media print {

      html,
      html[data-theme="dark"] {
        --bg: #ffffff;
        --card: #ffffff;
        --card2: #f9fafc;
        --text: #1f2430;
        --muted: #555e6d;
        --line: #d0d5dd;
        color-scheme: light
      }

      .appbar,
      .toc,
      #totop,
      .pn,
      .phase-check,
      .dg-bar button,
      #readbar,
      .search,
      .quiz-banner,
      .memo-sec {
        display: none !important
      }

      .view {
        display: block !important
      }

      #home {
        display: none !important
      }

      .sec.collapsed .sec-body {
        display: block
      }

      .sec {
        break-inside: auto;
        box-shadow: none
      }

      body {
        background: #fff;
        color: #1f2430
      }
    }
  </style>
</head>

<body>
  <div id="readbar"></div>
  <header class="appbar">
    <button class="icon-btn" id="homeBtn" aria-label="홈으로" title="홈"><svg viewBox="0 0 24 24">
        <path d="M3 11l9-8 9 8" />
        <path d="M5 10v10h14V10" />
      </svg></button>
    <button class="title" id="appTitle">📚 수능 학습 가이드</button>
    <button class="icon-btn" id="quizBtn" aria-label="암기 테스트 모드" title="빈칸 암기 모드 (단축키 Q)">🙈</button>
    <button class="icon-btn fs-btn" id="fsDown" aria-label="글자 작게" title="글자 작게"><span>가<sub
          style="font-size:.6em">−</sub></span></button>
    <button class="icon-btn fs-btn" id="fsUp" aria-label="글자 크게" title="글자 크게"><span>가<sup
          style="font-size:.6em">+</sup></span></button>
    <button class="icon-btn" id="themeBtn" aria-label="다크 모드 전환" title="다크 모드">🌙</button>
    <button class="icon-btn" id="searchBtn" aria-label="검색" title="검색 ( / )"><svg viewBox="0 0 24 24">
        <circle cx="11" cy="11" r="7" />
        <path d="M20 20l-3.5-3.5" />
      </svg></button>
  </header>

  <main>
    <section id="home" class="view"><!--STATIC:home-->__STATIC_HOME__<!--/STATIC:home--></section>
    <section id="subjects"><!--STATIC:subjects-->__STATIC_SUBJECTS__<!--/STATIC:subjects--></section>
    <footer>현재 폴더의 과목별 학습 자료(.md 8개)를 바탕으로 만든 문서입니다 · 체크 표시와 메모는 이 기기에 자동 저장돼요</footer>
  </main>

  <div class="search" id="search" role="dialog" aria-modal="true" aria-label="검색">
    <div class="search-box">
      <div class="search-in">
        <span aria-hidden="true">🔍</span>
        <input id="q" type="search" placeholder="키워드 검색 (예: 객관적 상관물, 조건 번역, 엘니뇨)" autocomplete="off" enterkeyhint="search">
        <button class="icon-btn" id="searchClose" aria-label="닫기">✕</button>
      </div>
      <div class="search-res" id="results"></div>
    </div>
  </div>

  <div class="search" id="backupModal" role="dialog" aria-modal="true" aria-label="학습 기록 백업 및 복원">
    <div class="search-box">
      <div class="search-in">
        <span>💾 <b>학습 기록 백업 · 복원 · 초기화</b></span>
        <button class="icon-btn" id="backupClose" aria-label="닫기" style="margin-left:auto">✕</button>
      </div>
      <div class="backup-body">
        <p style="margin:0 0 6px;color:var(--muted)">체크리스트 진행률, 세부 과제, 백지 유도, 시험일(D-Day), 과목별 메모 데이터가 아래 코드에 담겨 있습니다. 복사해 두면 스마트폰·태블릿·PC 어디서든 이어서 쓸 수 있어요.</p>
        <textarea id="backupData" spellcheck="false" aria-label="백업 데이터 코드"></textarea>
        <div class="backup-actions">
          <button type="button" class="btn-act pri" id="btnCopyBackup">📋 백업 코드 복사</button>
          <button type="button" class="btn-act" id="btnApplyBackup">📥 붙여넣은 코드로 복원</button>
          <button type="button" class="btn-act danger" id="btnResetAll" style="margin-left:auto">🗑️ 기록 전체 초기화</button>
        </div>
      </div>
    </div>
  </div>

  <button id="totop" aria-label="맨 위로">↑</button>
  <div class="toast" id="toast"></div>

  <script>
    const SUBJECTS = __SUBJECTS_JSON__;
    (function () {
      'use strict';
      const $ = (s, r = document) => r.querySelector(s);
      const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
      const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
      const store = {
        get(k, d) { try { const v = localStorage.getItem('sg:' + k); return v === null ? d : JSON.parse(v); } catch (e) { return d; } },
        set(k, v) { try { localStorage.setItem('sg:' + k, JSON.stringify(v)); } catch (e) { } }
      };
      function hexToSoft(hex, a) { const n = parseInt(hex.slice(1), 16); return `rgba(${n >> 16 & 255},${n >> 8 & 255},${n & 255},${a})`; }

      /* ================= TeX fallback (오프라인일 때 사용) ================= */
      const SYM = {
        rightarrow: '→', to: '→', implies: '⟹', Rightarrow: '⇒', leftrightarrow: '↔', uparrow: '↑', downarrow: '↓', leftarrow: '←',
        Delta: 'Δ', delta: 'δ', cdot: '·', theta: 'θ', times: '×', sum: 'Σ', propto: '∝', bigcirc: '◯', ll: '≪', gg: '≫', equiv: '≡', circ: '∘', pm: '±',
        mu: 'μ', lambda: 'λ', triangle: '△', sim: '∼', nu: 'ν', neq: '≠', ne: '≠', land: '∧', lor: '∨', int: '∫', bullet: '•', Phi: 'Φ', phi: 'φ', vert: '|',
        sigma: 'σ', rho: 'ρ', tau: 'τ', epsilon: 'ε',
        sin: 'sin', cos: 'cos', tan: 'tan', log: 'log', ln: 'ln', lim: 'lim', alpha: 'α', beta: 'β', gamma: 'γ', pi: 'π', omega: 'ω', infty: '∞',
        le: '≤', leq: '≤', ge: '≥', geq: '≥', approx: '≈', therefore: '∴', because: '∵', cdots: '⋯', ldots: '…', quad: '  ', qquad: '   ',
        ',': ' ', ';': ' ', ':': ' ', '!': '', ' ': ' ', '{': '{', '}': '}', '%': '%', '$': '$', '_': '_', '&': '&', '|': '‖'
      };
      function tex2html(src) {
        let i = 0;
        function readArg(textMode) {
          while (src[i] === ' ') i++;
          if (src[i] === '{') { i++; const r = seq('}', textMode); i++; return r; }
          if (src[i] === '\\\\') return cmd();
          const c = src[i++] || '';
          return /[a-zA-Z]/.test(c) && !textMode ? '<i>' + c + '</i>' : esc(c);
        }
        function cmd() {
          i++;
          const m = /^[a-zA-Z]+/.exec(src.slice(i));
          let name; if (m) { name = m[0]; i += name.length; } else { name = src[i++]; }
          switch (name) {
            case 'text': case 'mathrm': case 'operatorname': case 'textrm': return '<span class="tx">' + readArg(true) + '</span>';
            case 'mathbf': case 'textbf': case 'boldsymbol': return '<b>' + readArg() + '</b>';
            case 'frac': case 'dfrac': case 'tfrac': { const a = readArg(), b = readArg(); return `<span class="fr"><span class="nu">${a}</span><span class="de">${b}</span></span>`; }
            case 'vec': return '<span class="vec">' + readArg() + '</span>';
            case 'sqrt': return '√<span style="text-decoration:overline">' + readArg() + '</span>';
            case 'left': case 'right': return '';
            default: return SYM[name] !== undefined ? esc(SYM[name]) : esc(name);
          }
        }
        function seq(end, textMode) {
          let out = '';
          while (i < src.length && src[i] !== end) {
            const c = src[i];
            if (c === '\\\\') out += cmd();
            else if (c === '^') { i++; out += '<sup>' + readArg() + '</sup>'; }
            else if (c === '_') { i++; out += '<sub>' + readArg() + '</sub>'; }
            else if (c === '{') { i++; out += seq('}', textMode); i++; }
            else if (textMode) { out += esc(c); i++; }
            else if (c === ' ') { i++; }
            else if (/[a-zA-Z]/.test(c)) { out += '<i>' + c + '</i>'; i++; }
            else if (c === ',') { out += ', '; i++; }
            else if (/[=+<>]/.test(c) || c === '-' && out) { out += ' ' + esc(c) + ' '; i++; }
            else { out += esc(c); i++; }
          }
          return out;
        }
        return seq(undefined).replace(/(→|⟹|↔|≡|∝|×|≪|≠|∧|≤|≥)/g, ' $1 ').replace(/\\s{2,}/g, ' ').trim();
      }
      const SUP = { '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴', '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹', '-': '⁻', '+': '⁺', 'n': 'ⁿ' };
      function tex2plain(src) {
        return tex2html(src)
          .replace(/<sup>(.*?)<\\/sup>/g, (m, s) => { const t = s.replace(/<[^>]+>/g, ''); return [...t].every(ch => SUP[ch]) ? [...t].map(ch => SUP[ch]).join('') : '^(' + t + ')'; })
          .replace(/<span class="fr"><span class="nu">(.*?)<\\/span><span class="de">(.*?)<\\/span><\\/span>/g, '($1)/($2)')
          .replace(/<[^>]+>/g, '').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&amp;/g, '&');
      }
      function math(tex, display) {
        return `<span class="m${display ? ' md' : ''}" data-tex="${esc(tex)}">${tex2html(tex)}</span>`;
      }

      /* ================= Markdown parser ================= */
      function inline(t) {
        const ph = [];
        const put = h => '\\u0000' + (ph.push(h) - 1) + '\\u0000';
        t = t.replace(/`([^`]+)`/g, (m, c) => put('<code>' + esc(c) + '</code>'));
        t = t.replace(/\\$\\$([^$]+)\\$\\$/g, (m, c) => put(math(c, true)));
        t = t.replace(/\\$([^$]+?)\\$/g, (m, c) => put(math(c, false)));
        t = esc(t).replace(/&lt;br\\s*\\/?&gt;/g, '<br>');
        t = t.replace(/\\*\\*(.+?)\\*\\*/g, '<strong>$1</strong>');
        t = t.replace(/(^|[^*\\w])\\*(?![\\s*])([^*]+?)\\*(?!\\*)/g, '$1<em>$2</em>');
        t = t.replace(/\\u0000(\\d+)\\u0000/g, (m, i) => ph[+i]);
        return t;
      }
      const stripMd = s => s.replace(/\\*\\*/g, '').replace(/\\$([^$]+)\\$/g, (m, c) => tex2plain(c)).replace(/<br\\s*\\/?>/g, ' ').trim();
      const LI = /^(\\s*)([*-]|\\d+\\.)\\s+(.*)$/;

      let ctx = { subj: '', phase: 0, cb: 0 };

      function diagram(code) {
        code = code.replace(/\\$([^$\\n]+)\\$/g, (m, c) => tex2plain(c));
        const lines = code.split('\\n');
        if (lines.some(l => l.trim().startsWith('□ '))) {
          let out = '<div class="check-box-wrap"><div class="dg-bar"><span>☑️ 백지 유도 자가 점검 체크리스트</span><span class="cb-stat">직접 백지에 써본 뒤 체크하세요</span></div><div class="cb-body">';
          for (const l of lines) {
            const s = l.trim();
            if (!s) continue;
            if (s.startsWith('□ ')) {
              const key = ctx.subj + ':cb:' + (ctx.cb++);
              out += `<label class="cb-item" data-cbkey="${esc(key)}"><input type="checkbox"><span>${esc(s.slice(2).trim())}</span></label>`;
            } else {
              out += `<div class="cb-group-title">${esc(s)}</div>`;
            }
          }
          return out + '</div></div>';
        }
        return `<figure class="diagram"><div class="dg-bar"><span>🗺️ 구조도 <span class="hint">· 옆으로 밀어서 보기 ↔</span></span><button type="button" class="dg-wrap">줄바꿈</button></div><pre><code>${esc(code)}</code></pre></figure>`;
      }

      function list(lines) {
        const root = { children: [] };
        const stack = [{ key: [-1, -1], node: root }];
        const cmp = (a, b) => a[0] !== b[0] ? a[0] - b[0] : a[1] - b[1];
        for (const l of lines) {
          const m = LI.exec(l);
          const indent = m[1].replace(/\\t/g, '  ').length;
          const ordered = /\\d/.test(m[2]);
          const text = m[3];
          const key = [indent, ordered ? 0 : (text.startsWith('**') ? 1 : 2)];
          while (stack.length > 1 && cmp(stack[stack.length - 1].key, key) >= 0) stack.pop();
          const node = { ordered, num: ordered ? parseInt(m[2], 10) : 1, text, children: [] };
          stack[stack.length - 1].node.children.push(node);
          stack.push({ key, node });
        }
        return renderList(root.children);
      }
      function renderList(nodes) {
        let html = '', k = 0;
        while (k < nodes.length) {
          const ord = nodes[k].ordered, start = nodes[k].num;
          let inner = '';
          while (k < nodes.length && nodes[k].ordered === ord) {
            const n = nodes[k++];
            inner += `<li>${inline(n.text)}${n.children.length ? renderList(n.children) : ''}</li>`;
          }
          html += ord ? `<ol${start !== 1 ? ` start="${start}"` : ''}>${inner}</ol>` : `<ul>${inner}</ul>`;
        }
        return html;
      }

      function splitRow(r) {
        r = r.trim(); if (r.startsWith('|')) r = r.slice(1); if (r.endsWith('|')) r = r.slice(0, -1);
        const cells = []; let cur = '', inM = false, inC = false;
        for (let k = 0; k < r.length; k++) {
          const c = r[k];
          if (c === '`' && !inM) inC = !inC;
          if (c === '$' && !inC && r[k - 1] !== '\\\\') inM = !inM;
          if (c === '|' && !inM && !inC) { cells.push(cur.trim()); cur = ''; } else cur += c;
        }
        cells.push(cur.trim());
        return cells;
      }
      function cellHtml(raw, subPrefix) {
        const pieces = raw.split(/<br\\s*\\/?>/).map(s => s.trim()).filter(Boolean);
        if (pieces.some(p => p.startsWith('•'))) {
          let out = '', open = false, idx = 0;
          for (const p of pieces) {
            if (p.startsWith('•')) {
              if (!open) { out += '<ul class="cell-list">'; open = true; }
              const txt = inline(p.replace(/^•\\s*/, ''));
              if (subPrefix) out += `<li class="sub-task" data-subkey="${esc(subPrefix + ':' + (idx++))}">${txt}</li>`;
              else out += `<li>${txt}</li>`;
            } else {
              if (open) { out += '</ul>'; open = false; }
              out += `<div class="cl">${inline(p)}</div>`;
            }
          }
          return out + (open ? '</ul>' : '');
        }
        if (pieces.length > 1) return pieces.map(p => `<div class="cl">${inline(p)}</div>`).join('');
        return inline(raw);
      }
      function table(rows) {
        const head = splitRow(rows[0]);
        const body = rows.slice(/^\\|?\\s*:?-{2,}/.test(rows[1] || '') ? 2 : 1).map(splitRow);
        if (head[0] === '단계' && head.some(h => h.includes('통과'))) return roadmap(head, body);
        const wide = head.length >= 6;
        const labels = head.map(stripMd);
        let h = `<div class="table-wrap ${wide ? 'wide' : 'cardable'}"><table><thead><tr>${head.map(c => `<th>${inline(c)}</th>`).join('')}</tr></thead><tbody>`;
        for (const r of body) {
          h += '<tr>' + head.map((_, ci) => { const c = r[ci] || ''; return `<td data-label="${esc(labels[ci])}">${c ? cellHtml(c) : ''}</td>`; }).join('') + '</tr>';
        }
        return h + '</tbody></table></div>';
      }
      function roadmap(head, body) {
        const periodIdx = head.findIndex(h => h.includes('기간'));
        const gateIdx = head.findIndex(h => h.includes('통과'));
        let h = '<div class="roadmap">';
        body.forEach((r, n) => {
          const key = ctx.subj + ':' + (ctx.phase++);
          const t = (r[0] || '').replace(/^\\*\\*|\\*\\*$/g, '');
          const m = /^(Phase\\s*\\d+)\\s*[:：]\\s*(.*)$/i.exec(t);
          const badge = m ? m[1] : `${n + 1}단계`, title = m ? m[2] : t;
          let fields = '';
          head.forEach((hd, ci) => {
            if (ci === 0 || ci === periodIdx || ci === gateIdx) return;
            fields += `<div class="phase-field"><div class="pf-label">📝 ${esc(stripMd(hd))} <small style="font-weight:500;opacity:.8">(클릭해 개별 체크)</small></div>${cellHtml(r[ci] || '', key)}</div>`;
          });
          h += `<div class="phase" data-key="${esc(key)}">
      <div class="phase-rail"><span class="dot">${n + 1}</span></div>
      <div class="phase-card">
        <div class="phase-top"><span class="phase-badge">${esc(badge)}</span>${periodIdx >= 0 ? `<span class="period">⏱ ${cellHtml(r[periodIdx] || '').replace(/<\\/?div[^>]*>/g, ' ')}</span>` : ''}</div>
        <h4 class="phase-title">${inline(title)}</h4>
        ${fields}
        ${gateIdx >= 0 ? `<div class="phase-gate"><div class="pf-label">🚩 ${esc(stripMd(head[gateIdx]))}</div>${cellHtml(r[gateIdx] || '')}</div>` : ''}
        <label class="phase-check"><input type="checkbox"> <span>이 단계 통과했어요!</span></label>
      </div></div>`;
        });
        return h + '</div>';
      }
      function isBlockStart(l) {
        const s = l.trim();
        return /^#{2,3}\\s/.test(s) || s.startsWith('```') || s.startsWith('|') || /^-{3,}$/.test(s) || LI.test(l) || /^\\$\\$.*\\$\\$$/.test(s);
      }
      function parseDoc(md) {
        const lines = md.split('\\n');
        const doc = { intro: '', sections: [] };
        let cur = null, html = '', i = 0, m;
        const flush = () => { if (cur) cur.html = html; else doc.intro = html; html = ''; };
        while (i < lines.length) {
          const line = lines[i], s = line.trim();
          if (!s || /^-{3,}$/.test(s)) { i++; continue; }
          if (s.startsWith('```')) {
            const buf = []; i++;
            while (i < lines.length && !lines[i].trim().startsWith('```')) { buf.push(lines[i]); i++; }
            i++;
            while (buf.length && !buf[buf.length - 1].trim()) buf.pop();
            html += diagram(buf.join('\\n')); continue;
          }
          if ((m = /^##\\s+(.*)$/.exec(s))) { flush(); cur = { title: m[1], html: '' }; doc.sections.push(cur); i++; continue; }
          if ((m = /^###\\s+(.*)$/.exec(s))) { html += `<h3>${inline(m[1])}</h3>`; i++; continue; }
          if (/^\\$\\$.*\\$\\$$/.test(s)) { html += `<div class="math-block">${math(s.slice(2, -2), true)}</div>`; i++; continue; }
          if (s.startsWith('|')) {
            const rows = [];
            while (i < lines.length && lines[i].trim().startsWith('|')) { rows.push(lines[i].trim()); i++; }
            html += table(rows); continue;
          }
          if (LI.test(line)) {
            const items = [];
            while (i < lines.length) {
              const l = lines[i];
              if (LI.test(l)) { items.push(l); i++; }
              else if (!l.trim()) {
                let j = i; while (j < lines.length && !lines[j].trim()) j++;
                if (j < lines.length && LI.test(lines[j])) i = j; else break;
              } else break;
            }
            html += list(items); continue;
          }
          const buf = [s]; i++;
          while (i < lines.length && lines[i].trim() && !isBlockStart(lines[i])) { buf.push(lines[i].trim()); i++; }
          html += `<p>${inline(buf.join(' '))}</p>`;
        }
        flush();
        return doc;
      }

      /* ================= Build DOM ================= */
      const subjEl = $('#subjects');
      subjEl.innerHTML = '';   // 정적 프리렌더(미리보기용) 제거 후 다시 그림
      document.documentElement.classList.remove('no-js');
      const byId = {};
      const memos = store.get('memo', {});

      SUBJECTS.forEach((s, idx) => {
        ctx = { subj: s.id, phase: 0, cb: 0 };
        const doc = parseDoc(s.md);
        s.doc = doc; s.idx = idx; byId[s.id] = s;
        const soft = hexToSoft(s.color, .13);
        const art = document.createElement('article');
        art.className = 'view subject'; art.id = 'v-' + s.id;
        art.style.setProperty('--accent', s.color); art.style.setProperty('--accent-soft', soft);
        const secs = doc.sections.map((sec, n) => {
          const mm = /^(\\d+)\\.\\s*(.*)$/.exec(sec.title);
          const num = mm ? mm[1] : String(n + 1), title = mm ? mm[2] : sec.title;
          sec.plain = stripMd(title); sec.num = num;
          const isRoad = sec.html.includes('class="roadmap"');
          return `<section class="sec" id="sec-${s.id}-${n}" data-n="${n}">
      <button class="sec-head" type="button" aria-expanded="true"><span class="sec-num">${num}</span><span class="sec-title">${inline(title)}</span>${isRoad ? '<span class="sec-badge">✅ 체크리스트</span>' : ''}<span class="chev" aria-hidden="true"></span></button>
      <div class="sec-body">${sec.html}</div></section>`;
        }).join('');
        const prev = SUBJECTS[idx - 1], next = SUBJECTS[idx + 1];
        art.innerHTML = `
    <div class="s-hero">
      <span class="tag">${esc(s.group)}</span>
      <h1><span>${s.emoji}</span>${esc(s.name)}</h1>
      <div class="intro">${doc.intro}</div>
      <div class="prog"><span class="prog-txt">로드맵 0/0</span><div class="mini-bar"><i></i></div></div>
    </div>
    <div class="layout">
      <nav class="toc" aria-label="목차">
        <div class="toc-label">목차</div>
        <div class="toc-scroll">${doc.sections.map((sec, n) => `<button class="chip" type="button" data-n="${n}"><span class="n">${sec.num}</span>${esc(sec.plain.replace(/\\s*\\(.*?\\)\\s*/g, ' ').trim())}</button>`).join('')}</div>
        <div class="toc-tools">
          <button type="button" class="quiz-toggle" title="핵심 키워드와 수식을 가려 셀프 테스트합니다 (단축키 Q)">🙈 암기 모드</button>
          <button type="button" class="fold-all">모두 접기</button>
        </div>
      </nav>
      <div class="quiz-banner">
        <span>🙈 <b>빈칸 암기 테스트 모드 켜짐</b> · 가려진 파란색 빈칸을 눌러 정답을 확인해 보세요!</span>
        <div class="quiz-banner-btns">
          <button type="button" class="quiz-reveal-all">👀 모두 보기</button>
          <button type="button" class="quiz-hide-all">🙈 모두 가리기</button>
        </div>
      </div>
      <div class="content">${secs}
        <section class="memo-sec" aria-label="나만의 과목 메모장">
          <div class="memo-head">
            <span>📝 ${esc(s.name)} 나만의 약점 · 오답 메모장</span>
            <small class="memo-status">입력 즉시 이 기기에 자동 저장됩니다</small>
          </div>
          <textarea class="memo-area" data-memo="${esc(s.id)}" placeholder="이 과목에서 자주 틀리는 개념, 내신 시험 범위, 기출 오답 원인을 자유롭게 적어두세요. (검색창에서도 함께 검색됩니다!)">${esc(memos[s.id] || '')}</textarea>
        </section>
        <div class="pn">
          <button type="button" class="prev" ${prev ? `data-go="${prev.id}"` : 'disabled'}><small>← 이전 과목</small><b>${prev ? prev.emoji + ' ' + esc(prev.name) : ''}</b></button>
          <button type="button" class="next" ${next ? `data-go="${next.id}"` : 'disabled'}><small>다음 과목 →</small><b>${next ? next.emoji + ' ' + esc(next.name) : ''}</b></button>
        </div>
      </div>
    </div>`;
        subjEl.appendChild(art);
        s.el = art;
        s.phases = $$('.phase', art);
        s.subTasks = $$('.sub-task', art);
        s.cbItems = $$('.cb-item', art);
        setupQuizMasks(art);
      });

      /* ---------- Setup Quiz Mode Masks ---------- */
      function setupQuizMasks(art) {
        $$('.sec-body', art).forEach(body => {
          if (body.querySelector('.roadmap')) return;
          // 1) 표의 2번째 열 이후에 나오는 strong 및 주요 수식(.m)
          $$('tbody td:not(:first-child) strong, tbody td:not(:first-child) .m', body).forEach(el => {
            if (el.closest('strong') && el.tagName !== 'STRONG') return;
            const txt = el.textContent.trim();
            if (/^[→↑↓↔△⟹,()\\s+-]+$/.test(txt)) return;
            el.classList.add('quiz-mask');
          });
          // 2) 본문 문단 및 리스트의 핵심 strong (단, 맨 앞 소제목 라벨 '구조:', '1단계:' 등은 힌트로 남김)
          $$('p strong, li strong, .math-block .m', body).forEach(el => {
            if (el.closest('table') || el.closest('.phase-card')) return;
            const txt = el.textContent.trim();
            if (txt.endsWith(':') || txt.endsWith('：')) return;
            const parent = el.parentElement;
            if (parent && (parent.tagName === 'LI' || parent.tagName === 'P')) {
              const firstNode = parent.childNodes[0];
              if (firstNode === el && (txt.includes('(') || txt.length <= 12) && (el.nextSibling && /^\\s*[:：]/.test(el.nextSibling.textContent || ''))) return;
            }
            el.classList.add('quiz-mask');
          });
        });
      }

      /* ---------- Home ---------- */
      function firstSentence(html) {
        const d = document.createElement('div'); d.innerHTML = html;
        const t = d.textContent.trim();
        const m = /^(.+?(?:니다|입니다)\\.)/.exec(t);
        return m ? m[1] : t.slice(0, 120);
      }
      function buildHome() {
        const groups = [];
        SUBJECTS.forEach(s => { let g = groups.find(x => x.name === s.group); if (!g) groups.push(g = { name: s.group, items: [] }); g.items.push(s); });
        $('#home').innerHTML = `
    <div class="home-hero">
      <h1>📚 수능 과목별 학습 가이드</h1>
      <p>문제 풀이에 들어가기 전에 꼭 다져야 할 <b>과목 구조 · 핵심 개념 · 단계별 로드맵</b>을 한곳에 모았어요.</p>
      <div class="hero-stats">
        <span class="pill">📘 ${SUBJECTS.length}개 과목</span>
        <span class="pill">🧭 ${SUBJECTS.reduce((a, s) => a + s.doc.sections.length, 0)}개 장</span>
        <span class="pill">🗓️ <span id="dday">시험일:</span> <input type="date" id="examDate" aria-label="시험일 설정"></span>
        <button type="button" class="pill clickable" id="backupBtn" title="학습 기록 백업 및 복원">💾 기록 백업·복원</button>
      </div>
      <div class="overall"><div class="bar"><i id="overallBar"></i></div><small id="overallTxt"></small></div>
    </div>
    ${groups.map(g => `<div class="group-title">${g.name === '과학탐구' ? '🔬' : '⭐'} ${esc(g.name)}</div>
      <div class="cards">${g.items.map(s => `
        <button class="s-card" type="button" data-go="${s.id}" style="--c:${s.color}">
          <div class="s-card-top"><span class="emo">${s.emoji}</span><span class="memo-dot ${(memos[s.id] || '').trim() ? 'on' : ''}" data-memodot="${s.id}">📝 메모</span></div>
          <h3>${esc(s.name)}</h3>
          <p>${esc(firstSentence(s.doc.intro))}</p>
          <div class="mini-bar"><i data-prog="${s.id}"></i></div>
          <div class="meta"><span>${s.doc.sections.length}개 장</span><span data-progtxt="${s.id}">0/0 단계</span></div>
        </button>`).join('')}</div>`).join('')}
    <div class="group-title">🧭 모든 과목의 공통 학습 흐름</div>
    <div class="flow">
      <div><b>과목 구조 파악</b><span>단원 사이의 연결(계통도)을 먼저 그려 전체 지도를 머릿속에 넣어요.</span></div>
      <div><b>핵심 개념 체계화</b><span>정의·공식·개념어를 백지에 스스로 써 보며(백지 인출) 빈틈을 찾아요.</span></div>
      <div><b>4단계 로드맵 실행</b><span>단계마다 ‘통과 기준(Gate)’을 넘었는지 확인하고 세부 과제를 체크해요.</span></div>
      <div><b>기출 분석 진입</b><span>점수보다 ‘왜 틀렸는지’의 원인을 분류·기록하며 기출을 반복해요.</span></div>
    </div>
    <div class="group-title">🎯 고2 맞춤 학사일정 운영 & 탐구 선택 전략</div>
    <section class="sec collapsed" id="home-guide-1">
      <button class="sec-head" type="button" aria-expanded="false"><span class="sec-num">📅</span><span class="sec-title">고2 시기별(학기 중 내신 vs 방학) 로드맵 운영 가이드</span><span class="sec-badge">필독 팁</span><span class="chev" aria-hidden="true"></span></button>
      <div class="sec-body">
        <p>고등학교 2학년은 <strong>학교 내신(수Ⅰ·수Ⅱ·과탐Ⅰ)이 곧 수능 시험 범위와 직결되는 가장 중요한 황금기</strong>입니다. 각 과목의 4단계 로드맵을 시기별로 아래와 같이 나누어 운영하세요.</p>
        <div class="table-wrap cardable">
          <table>
            <thead><tr><th>시기 구분</th><th>핵심 목표</th><th>과목별 시간 배분 & 로드맵 실행 전략</th></tr></thead>
            <tbody>
              <tr>
                <td data-label="시기 구분"><strong>① 방학 집중기</strong><br>(여름방학 4주 / 겨울방학 8주)</td>
                <td data-label="핵심 목표"><strong>국·수·영 기본기 Phase 1~3 완주</strong></td>
                <td data-label="과목별 시간 배분 & 로드맵 실행 전략"><ul class="cell-list">
                  <li><strong>황금 시간 배분:</strong> 수학(45%) : 국어(25%) : 영어(15%) : 과탐(15%)</li>
                  <li>내신 압박이 없는 방학 동안 <strong>수학 고1 빈틈 메우기 & 백지 유도(Phase 1~2)</strong>, <strong>국어 문법·문학 개념어(Phase 1~2)</strong>를 집중 돌파합니다.</li>
                </ul></td>
              </tr>
              <tr>
                <td data-label="시기 구분"><strong>② 학기 중 평상시</strong><br>(개학 ~ 시험 4주 전)</td>
                <td data-label="핵심 목표"><strong>내신 진도 = 수능 기출 3점·4점 병행</strong></td>
                <td data-label="과목별 시간 배분 & 로드맵 실행 전략"><ul class="cell-list">
                  <li>학교 진도에 맞춰 수Ⅰ·수Ⅱ 및 과탐Ⅰ의 해당 단원 <strong>수능·평가원 3점 및 쉬운 4점 기출(Phase 2~3)</strong>을 함께 풉니다.</li>
                  <li>국어(비문학 2지문)와 영어(단어 40개 + 독해 3지문)는 매일 40분씩 <strong>고정 루틴</strong>으로 감각을 유지합니다.</li>
                </ul></td>
              </tr>
              <tr>
                <td data-label="시기 구분"><strong>③ 내신 시험 직전</strong><br>(시험 D-4주 ~ D-Day)</td>
                <td data-label="핵심 목표"><strong>학교 내신 시험 범위 100% 올인</strong></td>
                <td data-label="과목별 시간 배분 & 로드맵 실행 전략"><ul class="cell-list">
                  <li>교과서, 학교 부교재, 프린트, 내신 기출 변형 문제 반복 풀이에 100% 집중합니다.</li>
                  <li>이 시기에 꼼꼼히 다진 수Ⅰ·수Ⅱ·과탐Ⅰ 내신 공부가 고3 수능의 가장 탄탄한 밑거름이 됩니다.</li>
                </ul></td>
              </tr>
              <tr>
                <td data-label="시기 구분"><strong>④ 모의고사 주간</strong><br>(3·6·9·11월 학력평가)</td>
                <td data-label="핵심 목표"><strong>실전 시간 배분 & 오답 원인 기록</strong></td>
                <td data-label="과목별 시간 배분 & 로드맵 실행 전략"><ul class="cell-list">
                  <li>당일 채점 후 점수에만 일희일비하지 말고, 각 과목 페이지 하단 <strong>‘나만의 오답 메모장’에 틀린 원인(개념 빈틈 vs 시간 부족 vs 실수)을 기록</strong>합니다.</li>
                </ul></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </section>
    <section class="sec collapsed" id="home-guide-2">
      <button class="sec-head" type="button" aria-expanded="false"><span class="sec-num">🔬</span><span class="sec-title">고2 → 고3 과학탐구 2과목 최종 선택 기준 가이드</span><span class="sec-badge">진로·선택</span><span class="chev" aria-hidden="true"></span></button>
      <div class="sec-body">
        <p>고2 내신에서는 과학탐구 3~4과목을 모두 공부하지만, <strong>고2 겨울방학 전에는 고3 수능에서 응시할 최종 2과목을 확정</strong>하여 선택과 집중을 해야 합니다.</p>
        <div class="table-wrap cardable">
          <table>
            <thead><tr><th>과목</th><th>과목 성격 & 장단점</th><th>1등급 결정 킬러 파트</th><th>이런 성향의 학생에게 강력 추천!</th></tr></thead>
            <tbody>
              <tr>
                <td data-label="과목"><strong>🧲 물리학Ⅰ</strong></td>
                <td data-label="과목 성격 & 장단점">암기량이 4과목 중 가장 적고 원리가 명확함. 초반 역학 진입장벽만 넘으면 고3 때 시간 여유가 가장 큰 효자 과목.</td>
                <td data-label="1등급 결정 킬러 파트">1단원 역학 (복합 도르래, 빗면 역학적 에너지 보존) 2~3문항</td>
                <td data-label="이런 성향의 학생에게 강력 추천!">지엽적 암기를 싫어하고, <strong>수학적 직관·그래프 해석·도형 비례식</strong>을 좋아하는 학생</td>
              </tr>
              <tr>
                <td data-label="과목"><strong>⚗️ 화학Ⅰ</strong></td>
                <td data-label="과목 성격 & 장단점">논리적 규칙성이 뚜렷하고 단원 간 연결이 깔끔함. 단, 30분 안에 계산을 끝내야 하는 타임어택 압박이 있음.</td>
                <td data-label="1등급 결정 킬러 파트">1단원 화학 반응 양적 관계 & 4단원 중화 반응 양적 관계</td>
                <td data-label="이런 성향의 학생에게 강력 추천!"><strong>빠르고 정확한 분수·비례식 암산</strong>에 강하고, 원소 주기율 퍼즐 추론에 흥미가 있는 학생</td>
              </tr>
              <tr>
                <td data-label="과목"><strong>🧬 생명과학Ⅰ</strong></td>
                <td data-label="과목 성격 & 장단점">응시자 수가 많아 등급 컷과 표본이 안정적임. 비유전(14문항)을 10분 내에 끊고 유전 퍼즐을 푸는 시간 관리가 핵심.</td>
                <td data-label="1등급 결정 킬러 파트">4단원 유전 (가계도 추론, 세포 분열 DNA 상대량, 돌연변이)</td>
                <td data-label="이런 성향의 학생에게 강력 추천!"><strong>꼼꼼한 개념 암기력</strong>과 <strong>경우의 수(귀류법) 논리 퍼즐 추리력</strong>을 고루 갖춘 학생 (의약학 계열 선호도 1위)</td>
              </tr>
              <tr>
                <td data-label="과목"><strong>🌏 지구과학Ⅰ</strong></td>
                <td data-label="과목 성격 & 장단점">복잡한 수식 계산이 가장 적고 응시자 수가 압도적 1위(깔개 표본 풍부). 단, 꼼꼼한 자료 해석과 지엽적 개념 점검 필수.</td>
                <td data-label="1등급 결정 킬러 파트">고지자기 복각 해석, 외계 행성 시선 속도, 낯선 관측 그래프 해석</td>
                <td data-label="이런 성향의 학생에게 강력 추천!">계산 타임어택 부담을 줄이고 싶고, <strong>성실한 암기와 입체적 그림·그래프 독해</strong>에 강한 학생 (대부분 이공계생의 기본 1픽)</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </section>
    <div class="tips"><b>💡 업그레이드된 기능 이렇게 활용하세요</b>
      <ul>
        <li>상단 바의 <b>🙈 (단축키 Q)</b>를 누르면 핵심 키워드와 공식이 파란 빈칸으로 가려져 <b>셀프 암기 테스트</b>를 할 수 있어요.</li>
        <li>수학 3장의 <b>☑️ 백지 유도 체크리스트</b>와 각 과목 로드맵의 <b>세부 실행 과제 항목</b>을 직접 눌러 하나씩 완료 체크해 보세요.</li>
        <li>각 과목 맨 아래 <b>📝 나만의 약점·오답 메모장</b>에 시험 범위나 오답 포인트를 적어두면 자동 저장되고 🔍 검색에서도 찾아져요.</li>
        <li>상단 <b>💾 기록 백업·복원</b> 버튼으로 스마트폰·태블릿·PC 간 학습 기록을 자유롭게 옮길 수 있어요.</li>
      </ul>
    </div>`;
        const ex = $('#examDate');
        ex.value = store.get('exam', '');
        ex.addEventListener('change', () => { store.set('exam', ex.value); updateDday(); });
        $('#backupBtn').onclick = openBackup;
        updateDday();
      }
      function updateDday() {
        const v = store.get('exam', ''), el = $('#dday');
        if (!el) return;
        if (!v) { el.textContent = '시험일:'; return; }
        const today = new Date(); today.setHours(0, 0, 0, 0);
        const d = Math.round((new Date(v + 'T00:00:00') - today) / 864e5);
        el.textContent = d > 0 ? `D-${d}` : d === 0 ? 'D-DAY!' : `D+${-d}`;
      }
      buildHome();

      /* ---------- Progress (Phase, Sub-tasks, White-paper Checkboxes) ---------- */
      let done = store.get('done', {});
      let subDone = store.get('subdone', {});
      let cbDone = store.get('cbdone', {});

      function refreshProgress() {
        let all = 0, allDone = 0, subAll = 0, subCnt = 0;
        SUBJECTS.forEach(s => {
          const total = s.phases.length;
          const cnt = s.phases.filter(p => done[p.dataset.key]).length;
          const sTotal = s.subTasks.length;
          const sCnt = s.subTasks.filter(li => subDone[li.dataset.subkey]).length;
          all += total; allDone += cnt;
          subAll += sTotal; subCnt += sCnt;
          // 진행률 바는 Phase 완료 비중(70%) + 세부 과제 비중(30%) 또는 더 높은 값으로 자연스럽게 반영
          const pct = total ? Math.round((cnt / total * 0.7 + (sTotal ? sCnt / sTotal * 0.3 : cnt / total * 0.3)) * 100) : 0;
          $$(`[data-prog="${s.id}"]`).forEach(el => el.style.width = pct + '%');
          $$(`[data-progtxt="${s.id}"]`).forEach(el => el.textContent = `${cnt}/${total} 단계 · 과제 ${sCnt}/${sTotal}`);
          $('.prog-txt', s.el).textContent = `로드맵 ${cnt}/${total} 단계 · 세부 과제 ${sCnt}/${sTotal}`;
          $('.prog .mini-bar i', s.el).style.width = pct + '%';

          if (s.cbItems.length) {
            const cbCnt = s.cbItems.filter(it => cbDone[it.dataset.cbkey]).length;
            $$('.cb-stat', s.el).forEach(st => st.textContent = `달성 ${cbCnt}/${s.cbItems.length} (${Math.round(cbCnt / s.cbItems.length * 100)}%)`);
          }
          $$(`[data-memodot="${s.id}"]`).forEach(dot => dot.classList.toggle('on', !!(memos[s.id] || '').trim()));
        });
        const p = all ? Math.round(allDone / all * 100) : 0;
        $('#overallBar').style.width = p + '%';
        $('#overallTxt').textContent = `전체 로드맵 ${p}% (${allDone}/${all} 단계 완료 · 세부 실행 과제 ${subCnt}/${subAll}개 달성)`;
      }

      SUBJECTS.forEach(s => {
        s.phases.forEach(p => {
          const cb = $('.phase-check input', p);
          cb.checked = !!done[p.dataset.key];
          p.classList.toggle('done', cb.checked);
          cb.addEventListener('change', () => {
            if (cb.checked) done[p.dataset.key] = Date.now(); else delete done[p.dataset.key];
            store.set('done', done);
            p.classList.toggle('done', cb.checked);
            refreshProgress();
            if (cb.checked) {
              const left = s.phases.filter(x => !done[x.dataset.key]).length;
              toast(left ? `🎉 잘했어요! ${s.name} 남은 단계 ${left}개` : `🏆 ${s.name} 로드맵 완주! 정말 멋져요`);
            }
          });
        });

        s.subTasks.forEach(li => {
          const k = li.dataset.subkey;
          li.classList.toggle('checked', !!subDone[k]);
          li.addEventListener('click', e => {
            if (e.target.classList.contains('quiz-mask') && document.body.classList.contains('quiz-mode')) return;
            if (subDone[k]) delete subDone[k]; else subDone[k] = Date.now();
            store.set('subdone', subDone);
            li.classList.toggle('checked', !!subDone[k]);
            // 해당 Phase의 모든 세부 과제가 체크되었으면 Phase 체크박스도 자동 체크
            const phaseEl = li.closest('.phase');
            if (phaseEl) {
              const allSubs = $$('.sub-task', phaseEl);
              const allChecked = allSubs.length > 0 && allSubs.every(x => subDone[x.dataset.subkey]);
              if (allChecked && !done[phaseEl.dataset.key]) {
                const pcb = $('.phase-check input', phaseEl);
                pcb.checked = true;
                pcb.dispatchEvent(new Event('change'));
                return;
              }
            }
            refreshProgress();
          });
        });

        s.cbItems.forEach(lbl => {
          const k = lbl.dataset.cbkey;
          const inp = $('input', lbl);
          inp.checked = !!cbDone[k];
          lbl.classList.toggle('checked', inp.checked);
          inp.addEventListener('change', () => {
            if (inp.checked) cbDone[k] = Date.now(); else delete cbDone[k];
            store.set('cbdone', cbDone);
            lbl.classList.toggle('checked', inp.checked);
            refreshProgress();
            if (inp.checked) {
              const left = s.cbItems.filter(x => !cbDone[x.dataset.cbkey]).length;
              if (left === 0) toast(`🏆 ${s.name} 백지 유도 체크리스트 100% 완성!`);
            }
          });
        });

        const memoArea = $('.memo-area', s.el);
        const memoStat = $('.memo-status', s.el);
        let mT;
        memoArea.addEventListener('input', () => {
          memos[s.id] = memoArea.value;
          store.set('memo', memos);
          memoStat.textContent = '저장 중...';
          clearTimeout(mT);
          mT = setTimeout(() => {
            memoStat.textContent = memoArea.value.trim() ? `✓ 자동 저장됨 (${memoArea.value.length}자)` : '입력 즉시 이 기기에 자동 저장됩니다';
            refreshProgress();
          }, 300);
        });
      });
      refreshProgress();

      let toastT;
      function toast(msg) { const t = $('#toast'); t.textContent = msg; t.classList.add('on'); clearTimeout(toastT); toastT = setTimeout(() => t.classList.remove('on'), 2200); }

      /* ---------- Quiz Mode (빈칸 암기 테스트) ---------- */
      let quizMode = false;
      function toggleQuizMode(force) {
        quizMode = typeof force === 'boolean' ? force : !quizMode;
        document.body.classList.toggle('quiz-mode', quizMode);
        $('#quizBtn').classList.toggle('active', quizMode);
        $$('.quiz-toggle').forEach(b => {
          b.classList.toggle('active', quizMode);
          b.textContent = quizMode ? '🙈 암기 켜짐' : '🙈 암기 모드';
        });
        if (!quizMode) $$('.quiz-mask.revealed').forEach(el => el.classList.remove('revealed'));
        toast(quizMode ? '🙈 빈칸 암기 모드 켜짐! 파란 칸을 눌러 정답을 확인하세요' : '👀 암기 모드 해제');
      }
      $('#quizBtn').onclick = () => toggleQuizMode();

      /* ---------- Routing ---------- */
      let current = null, observer = null;
      function show(id, secN, focusEl) {
        $$('.view').forEach(v => v.classList.remove('on'));
        const s = byId[id];
        if (!s) {
          current = null;
          $('#home').classList.add('on');
          document.documentElement.style.setProperty('--accent', '#4c6ef5');
          document.documentElement.style.setProperty('--accent-soft', 'rgba(76,110,245,.12)');
          $('#appTitle').textContent = '📚 수능 학습 가이드';
          document.title = '수능 과목별 학습 가이드';
          window.scrollTo(0, 0); refreshProgress(); updateBar();
          return;
        }
        current = s;
        s.el.classList.add('on');
        document.documentElement.style.setProperty('--accent', s.color);
        document.documentElement.style.setProperty('--accent-soft', hexToSoft(s.color, .13));
        $('#appTitle').textContent = `${s.emoji} ${s.name}`;
        document.title = `${s.name} · 수능 학습 가이드`;
        setupObserver(s);
        requestAnimationFrame(() => {
          checkOverflow(s.el);
          if (focusEl) { const sec = focusEl.closest('.sec'); if (sec) expand(sec, true); focusEl.scrollIntoView({ block: 'center' }); focusEl.classList.remove('flash'); void focusEl.offsetWidth; focusEl.classList.add('flash'); }
          else if (secN != null) { const sec = $(`#sec-${s.id}-${secN}`); if (sec) { expand(sec, true); sec.scrollIntoView(); } }
          else window.scrollTo(0, 0);
          updateBar();
        });
      }
      let pendingFocus = null;
      function nav(h, focusEl) {
        pendingFocus = focusEl || null;
        if (location.hash === h || decodeURIComponent(location.hash) === decodeURIComponent(h)) route();
        else location.hash = h;   // hashchange -> route()
      }
      function go(id, secN) {
        nav(id ? `#/s/${encodeURIComponent(id)}${secN != null ? '/' + secN : ''}` : '#/');
      }
      function route() {
        let h = location.hash.slice(1);
        try { h = decodeURIComponent(h); } catch (e) { }
        const m = /^\\/s\\/([^/]+)(?:\\/(\\d+))?/.exec(h);
        const f = pendingFocus; pendingFocus = null;
        show(m ? m[1] : null, m && m[2] != null ? +m[2] : null, f);
      }
      window.addEventListener('hashchange', route);

      document.addEventListener('click', e => {
        if (quizMode) {
          const qm = e.target.closest('.quiz-mask');
          if (qm) { e.stopPropagation(); qm.classList.toggle('revealed'); return; }
        }
        const qt = e.target.closest('.quiz-toggle');
        if (qt) { toggleQuizMode(); return; }
        const qRev = e.target.closest('.quiz-reveal-all');
        if (qRev && current) { $$('.quiz-mask', current.el).forEach(el => el.classList.add('revealed')); return; }
        const qHide = e.target.closest('.quiz-hide-all');
        if (qHide && current) { $$('.quiz-mask', current.el).forEach(el => el.classList.remove('revealed')); return; }

        const g = e.target.closest('[data-go]');
        if (g) { go(g.dataset.go); return; }
        const chip = e.target.closest('.toc .chip');
        if (chip && current) { const sec = $(`#sec-${current.id}-${chip.dataset.n}`); if (sec) { expand(sec, true); sec.scrollIntoView({ behavior: 'smooth' }); } return; }
        const head = e.target.closest('.sec-head');
        if (head) { const sec = head.parentElement; expand(sec, sec.classList.contains('collapsed')); updateFoldBtn(); return; }
        const wrap = e.target.closest('.dg-wrap');
        if (wrap) { const f = wrap.closest('.diagram'); f.classList.toggle('wrap'); wrap.textContent = f.classList.contains('wrap') ? '원래대로' : '줄바꿈'; checkOverflow(f.parentElement); return; }
        const fold = e.target.closest('.fold-all');
        if (fold && current) { const anyOpen = $$('.sec', current.el).some(s => !s.classList.contains('collapsed')); $$('.sec', current.el).forEach(s => expand(s, !anyOpen)); updateFoldBtn(); return; }
      });
      function expand(sec, open) { sec.classList.toggle('collapsed', !open); $('.sec-head', sec).setAttribute('aria-expanded', String(open)); if (open) checkOverflow(sec); }
      function updateFoldBtn() { if (!current) return; const anyOpen = $$('.sec', current.el).some(s => !s.classList.contains('collapsed')); $('.fold-all', current.el).textContent = anyOpen ? '모두 접기' : '모두 펼치기'; }
      $('#homeBtn').onclick = () => go(null);
      $('#appTitle').onclick = () => current ? window.scrollTo({ top: 0, behavior: 'smooth' }) : null;

      function setupObserver(s) {
        if (observer) observer.disconnect();
        if (!('IntersectionObserver' in window)) return;
        const chips = $$('.chip', s.el), bar = $('.toc-scroll', s.el);
        observer = new IntersectionObserver(entries => {
          entries.forEach(en => {
            if (!en.isIntersecting) return;
            const n = en.target.dataset.n;
            chips.forEach(c => c.classList.toggle('active', c.dataset.n === n));
            const c = chips[+n];
            if (c && bar.scrollWidth > bar.clientWidth) bar.scrollTo({ left: c.offsetLeft - bar.clientWidth / 2 + c.clientWidth / 2, behavior: 'smooth' });
          });
        }, { rootMargin: '-25% 0px -65% 0px' });
        $$('.sec', s.el).forEach(sec => observer.observe(sec));
      }

      function checkOverflow(root) {
        $$('.diagram', root || document).forEach(f => { const pre = $('pre', f); f.classList.toggle('overflow', pre.scrollWidth > pre.clientWidth + 2); });
      }
      let rT; window.addEventListener('resize', () => { clearTimeout(rT); rT = setTimeout(() => checkOverflow(current && current.el), 150); });

      /* ---------- Scroll: reading bar & to-top ---------- */
      function updateBar() {
        const h = document.documentElement.scrollHeight - innerHeight;
        $('#readbar').style.width = current && h > 0 ? (scrollY / h * 100) + '%' : '0';
        $('#totop').classList.toggle('on', scrollY > 600);
      }
      window.addEventListener('scroll', updateBar, { passive: true });
      $('#totop').onclick = () => window.scrollTo({ top: 0, behavior: 'smooth' });

      /* ---------- Font size & theme ---------- */
      let fs = store.get('fs', 17);
      const applyFs = () => document.documentElement.style.setProperty('--fs', fs + 'px');
      applyFs();
      $('#fsUp').onclick = () => { fs = Math.min(23, fs + 1); applyFs(); store.set('fs', fs); toast(`글자 크기 ${fs}`); checkOverflow(current && current.el); };
      $('#fsDown').onclick = () => { fs = Math.max(13, fs - 1); applyFs(); store.set('fs', fs); toast(`글자 크기 ${fs}`); checkOverflow(current && current.el); };
      let theme = store.get('theme', matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
      const applyTheme = () => { document.documentElement.dataset.theme = theme; $('#themeBtn').textContent = theme === 'dark' ? '☀️' : '🌙'; };
      applyTheme();
      $('#themeBtn').onclick = () => { theme = theme === 'dark' ? 'light' : 'dark'; applyTheme(); store.set('theme', theme); };

      /* ---------- Backup / Restore Modal ---------- */
      const backupModal = $('#backupModal'), backupData = $('#backupData');
      function openBackup() {
        const payload = {
          exam: store.get('exam', ''),
          done: store.get('done', {}),
          subdone: store.get('subdone', {}),
          cbdone: store.get('cbdone', {}),
          memo: store.get('memo', {})
        };
        backupData.value = JSON.stringify(payload);
        backupModal.classList.add('on');
        document.body.style.overflow = 'hidden';
      }
      function closeBackup() { backupModal.classList.remove('on'); document.body.style.overflow = ''; }
      $('#backupClose').onclick = closeBackup;
      backupModal.addEventListener('click', e => { if (e.target === backupModal) closeBackup(); });
      $('#btnCopyBackup').onclick = () => {
        backupData.select();
        if (navigator.clipboard) navigator.clipboard.writeText(backupData.value);
        else document.execCommand('copy');
        toast('📋 백업 코드가 클립보드에 복사되었어요!');
      };
      $('#btnApplyBackup').onclick = () => {
        try {
          const obj = JSON.parse(backupData.value.trim());
          if (!obj || typeof obj !== 'object') throw new Error('Invalid');
          if (obj.exam !== undefined) store.set('exam', obj.exam);
          if (obj.done) store.set('done', obj.done);
          if (obj.subdone) store.set('subdone', obj.subdone);
          if (obj.cbdone) store.set('cbdone', obj.cbdone);
          if (obj.memo) store.set('memo', obj.memo);
          closeBackup();
          toast('📥 기록 복원 완료! 화면을 새로고침합니다.');
          setTimeout(() => location.reload(), 600);
        } catch (e) {
          toast('⚠️ 올바른 백업 코드 형식이 아니에요.');
        }
      };
      $('#btnResetAll').onclick = () => {
        if (!confirm('모든 체크리스트와 메모 기록을 초기화할까요?')) return;
        ['exam', 'done', 'subdone', 'cbdone', 'memo'].forEach(k => localStorage.removeItem('sg:' + k));
        closeBackup();
        toast('🗑️ 모든 기록이 초기화되었어요.');
        setTimeout(() => location.reload(), 500);
      };

      /* ---------- Search ---------- */
      const index = [];
      const SYNONYMS = {
        '자유물체도': '힘 표시하기',
        '패러프레이징': '말바꿔쓰기',
        '백지 인출': '백지',
        '백지인출': '백지'
      };
      SUBJECTS.forEach(s => {
        $$('.sec', s.el).forEach(sec => {
          const n = +sec.dataset.n, secTitle = s.doc.sections[n].plain;
          $$('h3, .sec-body > p, li, tr, .diagram, .check-box-wrap, .phase-card', sec).forEach(el => {
            if (el.closest('.phase-card') && el !== el.closest('.phase-card')) return;
            if (el.tagName === 'LI' && el.closest('td')) return;
            if (el.tagName === 'TR' && el.parentElement.tagName === 'THEAD') return;
            let text;
            if (el.tagName === 'LI') text = Array.from(el.childNodes).filter(c => c.nodeName !== 'UL' && c.nodeName !== 'OL').map(c => c.textContent).join('');
            else if (el.tagName === 'TR') text = $$('td', el).map(td => td.textContent).join(' · ');
            else if (el.classList.contains('phase-card')) text = $$('.phase-title, .phase-field, .phase-gate', el).map(x => x.textContent).join(' · ');
            else text = el.textContent;
            text = text.replace(/\\s+/g, ' ').trim();
            if (text) index.push({ s, n, secTitle, el, text, low: text.toLowerCase() });
          });
        });
        $$('.intro p', s.el).forEach(el => { const text = el.textContent.replace(/\\s+/g, ' ').trim(); index.push({ s, n: -1, secTitle: '개요', el, text, low: text.toLowerCase() }); });
      });
      const searchEl = $('#search'), q = $('#q'), results = $('#results');
      let found = [];
      function openSearch() { searchEl.classList.add('on'); q.value = ''; renderResults(''); setTimeout(() => q.focus(), 30); document.body.style.overflow = 'hidden'; }
      function closeSearch() { searchEl.classList.remove('on'); document.body.style.overflow = ''; }
      function renderResults(query) {
        let normQ = query.trim();
        Object.keys(SYNONYMS).forEach(k => { if (normQ.includes(k)) normQ = normQ.replace(k, SYNONYMS[k]); });
        const terms = normQ.toLowerCase().split(/\\s+/).filter(Boolean);
        if (!terms.length) {
          const sug = ['객관적 상관물', '고전시가', '조건 번역', '말바꿔쓰기', '어법', '신간회', '열역학', '전하량 보존', '근수축', '엘니뇨'];
          results.innerHTML = `<div class="search-empty">전 과목 개념·공식·실전 예시·내 메모를 한 번에 찾아볼 수 있어요.<div class="quick">${sug.map(w => `<button class="chip" type="button" data-q="${w}">${w}</button>`).join('')}</div></div>`;
          return;
        }
        // 사용자 메모 검색 결과 포함
        const memoHits = [];
        SUBJECTS.forEach(s => {
          const mTxt = (memos[s.id] || '').trim();
          if (mTxt && terms.every(t => mTxt.toLowerCase().includes(t))) {
            memoHits.push({ s, n: -2, secTitle: '📝 나만의 메모장', el: $('.memo-sec', s.el), text: mTxt, low: mTxt.toLowerCase() });
          }
        });
        found = memoHits.concat(index.filter(it => terms.every(t => it.low.includes(t)))).slice(0, 80);
        if (!found.length) { results.innerHTML = `<div class="search-empty">‘${esc(query)}’에 대한 결과가 없어요.</div>`; return; }
        const re = new RegExp('(' + terms.map(t => t.replace(/[.*+?^${}()|[\\]\\\\]/g, '\\\\$&')).join('|') + ')', 'gi');
        let html = `<div class="res-group">검색 결과 ${found.length}${found.length === 80 ? '+' : ''}건</div>`, last = null;
        found.forEach((it, k) => {
          if (it.s !== last) { html += `<div class="res-group">${it.s.emoji} ${esc(it.s.name)}</div>`; last = it.s; }
          const pos = Math.max(0, it.low.indexOf(terms[0]) - 40);
          let snip = (pos > 0 ? '…' : '') + it.text.slice(pos, pos + 150) + (it.text.length > pos + 150 ? '…' : '');
          html += `<button class="res" type="button" data-k="${k}"><small>${it.n >= 0 ? (it.n + 1) + '장 · ' : ''}${esc(it.secTitle)}</small>${esc(snip).replace(re, '<mark>$1</mark>')}</button>`;
        });
        results.innerHTML = html;
      }
      let sT; q.addEventListener('input', () => { clearTimeout(sT); sT = setTimeout(() => renderResults(q.value.trim()), 120); });
      results.addEventListener('click', e => {
        const sq = e.target.closest('[data-q]');
        if (sq) { q.value = sq.dataset.q; renderResults(q.value); return; }
        const r = e.target.closest('.res'); if (!r) return;
        const it = found[+r.dataset.k];
        closeSearch();
        nav(`#/s/${encodeURIComponent(it.s.id)}`, it.el);
      });
      $('#searchBtn').onclick = openSearch;
      $('#searchClose').onclick = closeSearch;
      searchEl.addEventListener('click', e => { if (e.target === searchEl) closeSearch(); });
      document.addEventListener('keydown', e => {
        if (e.key === 'Escape') {
          if (searchEl.classList.contains('on')) closeSearch();
          if (backupModal.classList.contains('on')) closeBackup();
        } else if (e.key === '/' && !searchEl.classList.contains('on') && !backupModal.classList.contains('on') && !/INPUT|TEXTAREA/.test(document.activeElement.tagName)) {
          e.preventDefault(); openSearch();
        } else if ((e.key === 'q' || e.key === 'Q') && !searchEl.classList.contains('on') && !backupModal.classList.contains('on') && !/INPUT|TEXTAREA/.test(document.activeElement.tagName)) {
          e.preventDefault(); toggleQuizMode();
        }
      });

      /* ---------- KaTeX (온라인일 때 수식을 더 예쁘게) ---------- */
      window.__katexReady = function () {
        if (!window.katex) return;
        $$('.m').forEach(el => {
          try { el.innerHTML = katex.renderToString(el.dataset.tex, { throwOnError: false, displayMode: el.classList.contains('md'), strict: 'ignore', output: 'html' }); el.classList.add('k'); } catch (e) { }
        });
        checkOverflow(current && current.el);
      };

      route();
      if (window.katex) window.__katexReady();
      if ('serviceWorker' in navigator && location.protocol.startsWith('http')) {
        navigator.serviceWorker.register('./sw.js').catch(() => {});
      }
    })();
  </script>
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js" crossorigin="anonymous"
    onload="window.__katexReady && window.__katexReady()"></script>
</body>

</html>
"""

def generate_icon_png(path: Path):
    import struct, zlib, math
    w, h = 180, 180
    rows = []
    cx, cy = w / 2.0, h / 2.0
    for y in range(h):
        row = bytearray([0])  # filter type 0
        for x in range(w):
            # Indigo-blue gradient background
            t = (x + y) / (w + h)
            r = int(37 * (1 - t) + 79 * t)
            g = int(99 * (1 - t) + 70 * t)
            b = int(235 * (1 - t) + 229 * t)
            d = math.hypot(x - cx, y - cy)
            # Draw bullseye target rings in white/gold
            if 50 <= d <= 62 or 26 <= d <= 36:
                r, g, b = 255, 255, 255
            elif d < 14:
                r, g, b = 251, 191, 36
            row.extend((r, g, b, 255))
        rows.append(bytes(row))
    raw = b"".join(rows)
    def chunk(tag, data):
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xffffffff)
    png = (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(raw, 9))
        + chunk(b"IEND", b"")
    )
    path.write_bytes(png)

def main():
    subjects_data = []
    parsed_docs = []
    for meta in SUBJECT_META:
        md_path = WORKSPACE / meta["file"]
        md_text = md_path.read_text(encoding="utf-8").strip()
        subjects_data.append({
            "id": meta["id"],
            "name": meta["name"],
            "group": meta["group"],
            "emoji": meta["emoji"],
            "color": meta["color"],
            "md": md_text
        })
        parsed_docs.append(parse_doc(md_text, meta["id"]))

    static_home = build_static_home(subjects_data, parsed_docs)
    static_subjects = build_static_subjects(subjects_data, parsed_docs)
    subjects_json = json.dumps(subjects_data, ensure_ascii=False)

    final_html = (
        HTML_TEMPLATE
        .replace("__STATIC_HOME__", static_home)
        .replace("__STATIC_SUBJECTS__", static_subjects)
        .replace("__SUBJECTS_JSON__", subjects_json)
    )

    out_path = WORKSPACE / "수능_학습가이드.html"
    out_path.write_text(final_html, encoding="utf-8")
    index_path = WORKSPACE / "index.html"
    index_path.write_text(final_html, encoding="utf-8")

    generate_icon_png(WORKSPACE / "apple-touch-icon.png")

    manifest = {
        "name": "수능 과목별 학습 가이드 (고2 맞춤형)",
        "short_name": "수능 가이드",
        "description": "고등학교 2학년 내신·수능 1등급을 위한 전 과목 실전 학습 가이드",
        "start_url": "./index.html",
        "display": "standalone",
        "background_color": "#f6f7fb",
        "theme_color": "#2563eb",
        "icons": [
            {"src": "apple-touch-icon.png", "sizes": "180x180", "type": "image/png"}
        ]
    }
    (WORKSPACE / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    import hashlib
    content_hash = hashlib.sha256(final_html.encode("utf-8")).hexdigest()[:8]

    sw_code = f"""const CACHE_NAME = 'csat-guide-{content_hash}';
const ASSETS = [
  './',
  './index.html',
  './manifest.json',
  './apple-touch-icon.png',
  'https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css',
  'https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js'
];
self.addEventListener('install', e => {{
  e.waitUntil(caches.open(CACHE_NAME).then(c => c.addAll(ASSETS)).then(() => self.skipWaiting()));
}});
self.addEventListener('activate', e => {{
  e.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))).then(() => self.clients.claim()));
}});
self.addEventListener('fetch', e => {{
  if (e.request.method !== 'GET') return;
  e.respondWith(
    fetch(e.request).then(res => {{
      if (res && res.status === 200) {{
        const clone = res.clone();
        caches.open(CACHE_NAME).then(c => c.put(e.request, clone));
      }}
      return res;
    }}).catch(() => caches.match(e.request))
  );
}});
"""
    (WORKSPACE / "sw.js").write_text(sw_code, encoding="utf-8")
    (WORKSPACE / ".nojekyll").write_text("", encoding="utf-8")
    if not (WORKSPACE / ".gitignore").exists():
        (WORKSPACE / ".gitignore").write_text("__pycache__/\n*.pyc\n", encoding="utf-8")

    print(f"Successfully generated {out_path} and {index_path} (hash: {content_hash}, {len(final_html):,} chars, {len(final_html.encode('utf-8')):,} bytes)")

if __name__ == "__main__":
    main()
