#!/usr/bin/env python3

import os, sys, html, datetime as dt
import requests

# ---------- theme ----------
RED, BG, YEL, GRN, BLU = "#c65f5f", "#161b22", "#d9b27c", "#8ca589", "#7d92a2"

ASCII = """⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠓⢤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢀⠀⠀⠀⠀⠀⠀⡀⠀⠀⠀⠀⠀⠀⠙⢷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠻⣤⡀⠀⠀⠀⠸⣿⣄⡀⠀⠀⠀⠀⠘⢿⣧⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠈⠻⣦⡀⠀⠀⠘⢿⣿⣶⡄⠀⠀⠀⠀⠻⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠘⣿⣦⡀⠀⠈⠉⠻⣿⣶⡄⠀⠀⠀⠸⣿⣯⡀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠈⣿⣷⡀⠀⠀⠀⢻⣿⣿⣆⠀⠀⠀⡻⣿⣷⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢿⣿⣿⡆⠀⠀⠘⣻⣿⣿⠗⠀⠀⢻⣿⣿⡆⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢀⣽⣿⣷⠀⠀⠀⢺⣿⣿⣿⣦⠀⠀⠉⣿⣷⡀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠈⢿⣿⣿⡁⠀⠀⠀⢿⣿⣿⠱⠀⠀⠀⣿⣿⣷⠆⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⣿⡄⠀⠀⠈⢿⣿⡀⠀⠀⠀⠙⣿⣿⡇⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⣿⣿⡀⠀⠀⠈⢿⣄⠀⠀⠀⠀⠸⣿⣷⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⡇⠀⠀⠀⠀⢻⣶⠄⠀⠀⠀⠘⢿⣧⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⡄⠀⠀⠀⠈⢻⡆⠀⠀⠀⠀⠘⣿⣿⠂
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣷⣀⠀⠀⠀⠈⠻⠀⠀⠀⠀⠀⠘⣿⡇
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣯
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀""".split("\n")

# ---------- EDIT ME: static lines of your card ----------
TITLE = "hawlermathew@secguy"
INFO = [  # (key, value) - block under the title
    ("OS", "Debian 13 (Trixie), Ubuntu 24.04 (Noble)"),
    ("Host", "awooo"),
    ("Kernel", "Security Engineer & Pentest Wanderer"),
    ("IDE", "Neovim, VS Code"),
    ("Languages.Programming", "Python, Go, C"),
    ("Languages.Real", "English, Vietnamese"),
    ("Hobbies.Software", "Open source, cool hacks"),
    ("Hobbies.Hardware", "Iot in Dumpsters"),
    ("Hobbies.Others", "Crochet, Music, Gym"),
]
CONTACT = [  # (key, value), or [(key, value), (key, value)] for two columns on one line
    ("Email.me", "duonghoaianatwork@gmail.com"),
    ("Portfolio", "hawlermathew.net"),
    ("Discord", "hawlermathew"),
]
WIDTH_CHARS = 54  # width of each info line, in characters

# ---------- GitHub data ----------
API = "https://api.github.com/graphql"


def gql(query, variables=None):
    r = requests.post(API, json={"query": query, "variables": variables or {}},
                      headers={"Authorization": f"bearer {os.environ['ACCESS_TOKEN']}"}, timeout=60)
    r.raise_for_status()
    data = r.json()
    if "errors" in data:
        raise RuntimeError(data["errors"])
    return data["data"]


def fetch_stats(login):
    u = gql("""query($l:String!){user(login:$l){id createdAt followers{totalCount}
        repositoriesContributedTo(first:1,contributionTypes:[COMMIT,PULL_REQUEST,REPOSITORY]){totalCount}}}""",
            {"l": login})["user"]
    uid, created = u["id"], int(u["createdAt"][:4])

    # repositories you own or collaborate on (forks skipped)
    repos, cur = [], None
    while True:
        d = gql("""query($l:String!,$c:String){user(login:$l){repositories(first:100,after:$c,
            ownerAffiliations:[OWNER,COLLABORATOR]){pageInfo{hasNextPage endCursor}
            nodes{nameWithOwner stargazerCount isFork isEmpty}}}}""", {"l": login, "c": cur})
        page = d["user"]["repositories"]
        repos += [n for n in page["nodes"] if not n["isFork"] and not n["isEmpty"]]
        if not page["pageInfo"]["hasNextPage"]:
            break
        cur = page["pageInfo"]["endCursor"]

    # commits per calendar year (a contributionsCollection spans at most one year)
    now, commits = dt.datetime.now(dt.UTC), 0

    for y in range(created, now.year + 1):
        to = min(
            dt.datetime(y, 12, 31, 23, 59, 59, tzinfo=dt.UTC),
            now
        )
        c = gql("""query($l:String!,$f:DateTime!,$t:DateTime!){user(login:$l){contributionsCollection(from:$f,to:$t){
            totalCommitContributions restrictedContributionsCount}}}""",
            {"l": login, "f": f"{y}-01-01T00:00:00Z", "t": to.strftime("%Y-%m-%dT%H:%M:%SZ")})
        cc = c["user"]["contributionsCollection"]
        commits += cc["totalCommitContributions"] + cc["restrictedContributionsCount"]

    # lines added / deleted by you on each default branch
    add = dele = 0
    for r in repos:
        owner, name = r["nameWithOwner"].split("/")
        cur = None
        while True:
            d = gql("""query($o:String!,$n:String!,$u:ID!,$c:String){repository(owner:$o,name:$n){
                defaultBranchRef{target{... on Commit{history(first:100,after:$c,author:{id:$u}){
                pageInfo{hasNextPage endCursor} nodes{additions deletions}}}}}}}""",
                {"o": owner, "n": name, "u": uid, "c": cur})
            ref = d["repository"]["defaultBranchRef"]
            if not ref:
                break
            h = ref["target"]["history"]
            for n in h["nodes"]:
                add += n["additions"]; dele += n["deletions"]
            if not h["pageInfo"]["hasNextPage"]:
                break
            cur = h["pageInfo"]["endCursor"]

    return dict(repos=len(repos), stars=sum(r["stargazerCount"] for r in repos),
                commits=commits, followers=u["followers"]["totalCount"],
                contributed=u["repositoriesContributedTo"]["totalCount"], add=add, dele=dele)


# ---------- SVG ----------
CMD = "wget https://hawlermathew.net  # comming soon lol"   # typed in the terminal line
PROMPT = "visitor@github:~$ "
CYCLE = 10.0          # seconds per animation loop
CW, LH = 9.6, 20      # character width / line height at 16px

LINKS = [  # (file name, label, colour)
    ("link_portfolio.svg", "Portfolio", RED),
    ("link_linkedin.svg", "LinkedIn", BLU),
    ("link_email.svg", "Email", RED),
]


def seg(key, parts, w):
    """One 'key: ..... value' segment padded with dot leaders to w characters."""
    plain = sum(len(t) for t, _ in parts)
    dots = max(2, w - len(key) - plain - 3)
    inner = "".join(f'<tspan class="{c}">{html.escape(t)}</tspan>' for t, c in parts)
    return f'<tspan class="k">{html.escape(key)}</tspan>:<tspan class="d"> {"." * dots} </tspan>{inner}'


def row(key, parts):
    return seg(key, parts, WIDTH_CHARS)


def dash_head(text):
    return f'<tspan class="k">- {html.escape(text)} {"-" * max(2, WIDTH_CHARS - len(text) - 3)}</tspan>'


def head_line(text):
    return f'<tspan class="k">{html.escape(text)}</tspan> <tspan class="k">{"-" * max(2, WIDTH_CHARS - len(text) - 1)}</tspan>'


PRE = '<tspan class="k">. </tspan>'
SEP = '<tspan class="v"> | </tspan>'


def fmt_entries(entries):
    """(key, value) -> one dotted line; [(k1, v1), (k2, v2)] -> two columns split by ' | '."""
    out = []
    for e in entries:
        if isinstance(e, list):
            (k1, v1), (k2, v2) = e
            out.append(PRE + seg(k1, [(v1, "v")], 31) + SEP + seg(k2, [(v2, "v")], 18))
        else:
            out.append(PRE + seg(e[0], [(e[1], "v")], WIDTH_CHARS - 2))
    return out


def terminal(y):
    """Typing animation: returns (css, svg). Cursor blinks while the command is typed."""
    x0, t0, step, ret = 15, 0.8, 0.08, 4.2
    pct = lambda sec: sec / CYCLE * 100
    end = pct(CYCLE - 0.4)
    px = x0 + len(PROMPT) * CW
    css = [f".t{{opacity:0;animation-duration:{CYCLE}s;animation-iteration-count:infinite;animation-timing-function:step-end}}",
           ".cur{animation:mv %ss step-end infinite}" % CYCLE,
           ".bl{animation:bl 1s step-end infinite}",
           "@keyframes bl{0%,50%{opacity:1}50.01%,100%{opacity:0}}"]
    chars, moves = [], [f"0%{{transform:translate({px:.1f}px,{y}px)}}"]
    for i, ch in enumerate(CMD):
        p = pct(t0 + i * step)
        css.append(f"@keyframes c{i}{{0%,{p:.2f}%{{opacity:0}}{p + .01:.2f}%,{end:.2f}%{{opacity:1}}{end + .01:.2f}%,100%{{opacity:0}}}}")
        chars.append(f'<tspan class="t" style="animation-name:c{i}" x="{px + i * CW:.1f}" y="{y}">{html.escape(ch)}</tspan>')
        moves.append(f"{p:.2f}%{{transform:translate({px + (i + 1) * CW:.1f}px,{y}px)}}")
    r = pct(ret)
    moves.append(f"100%{{transform:translate({px:.1f}px,{y}px)}}")
    css.append("@keyframes mv{" + "".join(moves) + "}")
    plen = len(PROMPT) * CW
    svg = (f'<text xml:space="preserve" class="k"><tspan x="{x0}" y="{y}" textLength="{plen:.1f}" lengthAdjust="spacingAndGlyphs">{html.escape(PROMPT)}</tspan></text>'
           f'<text xml:space="preserve" class="v">{"".join(chars)}</text>'
           f'<g class="cur"><rect class="bl" x="0" y="-14" width="{CW}" height="18" fill="{YEL}"/></g>')
    return "\n".join(css), svg


def build_svg(s):
    n = lambda x: f"{x:,}"
    lines = [f'<tspan class="k">{html.escape(TITLE)}</tspan> <tspan class="k">{"-" * (WIDTH_CHARS - len(TITLE) - 1)}</tspan>']
    info = fmt_entries(INFO)
    lines += info
    lines += ["", dash_head("Contact")] + fmt_entries(CONTACT)
    pre = '<tspan class="k">. </tspan>'
    sep = '<tspan class="v"> | </tspan>'
    lines += ["", dash_head("GitHub Stats"),
              pre + seg("Repos", [(n(s["repos"]), "v"), (" {", "v"), ("Contributed", "k"), (": ", "k"),
                                  (n(s["contributed"]), "v"), ("}", "v")], 0)
                  + sep + seg("Stars", [(n(s["stars"]), "v")], 0),
              pre + seg("Commits", [(n(s["commits"]), "v")], 0)
                  + sep + seg("Followers", [(n(s["followers"]), "v")], 0),
              pre + seg("Lines of Code", [(n(s["add"] - s["dele"]), "v"), (" (", "v"),
                                          (f'{n(s["add"])}++', "g"), (", ", "v"),
                                          (f'{n(s["dele"])}--', "r"), (")", "v")], WIDTH_CHARS - 2)]
    ax, ix = 15, 300
    body = max(len(ASCII), len(lines))
    term_y = 30 + body * LH + 10
    height = term_y + 2 * LH + 10
    tcss, tsvg = terminal(term_y)
    art = "".join(f'<tspan x="{ax}" y="{30 + i * LH}" textLength="{len(l) * CW:.1f}" lengthAdjust="spacingAndGlyphs">{html.escape(l)}</tspan>'
                  for i, l in enumerate(ASCII))
    info_svg = "".join(f'<tspan x="{ix}" y="{30 + i * LH}">{l}</tspan>' for i, l in enumerate(lines))
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="900" height="{height}" font-size="16px"
     font-family="ui-monospace,SFMono-Regular,Consolas,'DejaVu Sans Mono',monospace">
<style>text{{white-space:pre}} .a,.k,.r{{fill:{RED}}} .v{{fill:{YEL}}} .g{{fill:{GRN}}} .d{{fill:{BLU}}}
{tcss}</style>
<rect width="100%" height="100%" fill="{BG}"/>
<text class="a" xml:space="preserve">{art}</text>
<text xml:space="preserve" fill="{YEL}">{info_svg}</text>
{tsvg}
</svg>"""


def build_button(label, color):
    w, h = 300, 40
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
            f'<rect x="1" y="1" width="{w - 2}" height="{h - 2}" fill="{BG}" stroke="{color}" stroke-width="2"/>'
            f'<text x="{w / 2}" y="26" text-anchor="middle" font-size="16" '
            f"font-family=\"ui-monospace,SFMono-Regular,Consolas,'DejaVu Sans Mono',monospace\" fill=\"{color}\">{html.escape(label)}</text></svg>")


if __name__ == "__main__":
    if "--demo" in sys.argv:
        stats = dict(repos=24, contributed=9, stars=57, commits=1893, followers=31, add=84210, dele=30977)
    else:
        stats = fetch_stats(os.environ["USER_NAME"])
    with open("card.svg", "w", encoding="utf-8") as f:
        f.write(build_svg(stats))
    for fname, label, color in LINKS:
        with open(fname, "w", encoding="utf-8") as f:
            f.write(build_button(label, color))
    print("card.svg + buttons written", stats)
