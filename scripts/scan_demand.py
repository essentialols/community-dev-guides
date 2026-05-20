#!/usr/bin/env python3
"""Scan Reddit for high-engagement threads that could become new guides.

Outputs:
- GITHUB_OUTPUT: has_signals=true/false, count=N
- /tmp/issue_body.md: formatted issue body for GitHub Actions
"""

import json
import os
import sys
import time
import urllib.request
import urllib.error

USER_AGENT = "CommunityDevGuides/1.0"

SUBREDDITS = [
    "LocalLLaMA", "webdev", "devops", "python",
    "nextjs", "golang", "rust", "kubernetes",
]

EXISTING_TOPICS = [
    "48gb vram", "quantization", "platform engineering",
    "modular monolith", "entry level dev", "infrastructure as code",
]

MIN_COMMENTS = 20
MIN_SCORE = 15


def scan_subreddit(sub: str, limit: int = 25) -> list[dict]:
    url = f"https://www.reddit.com/r/{sub}/top.json?t=week&limit={limit}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            results = []
            for post in data["data"]["children"]:
                d = post["data"]
                if d.get("num_comments", 0) >= MIN_COMMENTS and d.get("score", 0) >= MIN_SCORE:
                    title = d.get("title", "")
                    if any(t in title.lower() for t in EXISTING_TOPICS):
                        continue
                    results.append({
                        "sub": sub,
                        "title": title[:100],
                        "comments": d["num_comments"],
                        "score": d["score"],
                        "url": f"https://reddit.com{d['permalink']}",
                    })
            return results
    except (urllib.error.HTTPError, urllib.error.URLError) as e:
        print(f"Warning: r/{sub} failed: {e}", file=sys.stderr)
        return []


def main():
    signals = []
    for sub in SUBREDDITS:
        print(f"Scanning r/{sub}...", file=sys.stderr)
        signals.extend(scan_subreddit(sub))
        time.sleep(2)

    signals.sort(key=lambda s: s["comments"], reverse=True)
    top = signals[:5]

    output_file = os.environ.get("GITHUB_OUTPUT", "/dev/stdout")

    if top:
        body = "## Top Demand Signals This Week\n\n"
        body += "Potential new guide topics based on high-engagement Reddit threads:\n\n"
        for i, s in enumerate(top, 1):
            body += f"{i}. **r/{s['sub']}** ({s['comments']} comments, {s['score']} upvotes)\n"
            body += f"   {s['title']}\n"
            body += f"   {s['url']}\n\n"
        body += "To create a guide from any of these, run:\n"
        body += "```\npython3 scripts/batch_publish.py --count 1\n```\n"

        with open("/tmp/issue_body.md", "w") as f:
            f.write(body)

        with open(output_file, "a") as f:
            f.write(f"has_signals=true\n")
            f.write(f"count={len(top)}\n")

        print(f"Found {len(top)} demand signals", file=sys.stderr)
    else:
        with open(output_file, "a") as f:
            f.write("has_signals=false\n")
        print("No strong signals this week", file=sys.stderr)


if __name__ == "__main__":
    main()
