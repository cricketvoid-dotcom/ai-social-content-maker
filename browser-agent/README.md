# ContentForge Restricted Chrome Agent

This local agent is the browser-automation layer for Creative Studio. It uses a dedicated Chrome profile and a dedicated workspace so automation does not use the user's normal Chrome profile.

## Current setup capabilities

- launches the installed Google Chrome channel through Playwright
- uses a dedicated `browser-agent/profile` directory
- allows navigation only to ChatGPT, Gemini, and Claude
- stores browser downloads in `browser-agent/workspace/output`
- accepts input images from `browser-agent/workspace/input`
- supports authorizing exactly two of the three providers
- keeps authorization state local and excludes it from Git
- never asks ContentForge for passwords, verification codes, cookies, or session tokens

## Authorize two accounts

1. Install Python 3.11+.
2. From this folder run:

```bash
python -m pip install -r requirements.txt
python -m playwright install chrome
python setup.py
```

3. Choose two providers when prompted.
4. A separate Chrome profile named `ContentForge Agent` opens the first provider.
5. Log in manually with the account you want ContentForge to use.
6. Return to the terminal and press Enter.
7. The second provider opens in the same dedicated profile; repeat the manual sign-in and press Enter.

The selected sessions are retained by Chrome inside `browser-agent/profile`. The local `auth-state.json` contains only provider authorization metadata; it does not contain credentials. Both are ignored by Git.

## Security boundary

This is a browser-level restriction, not an operating-system sandbox. Chrome still runs as a normal desktop process. Keep this dedicated profile free of personal accounts and sensitive browsing data.

The current allowlist is exactly:

- `chatgpt.com`
- `gemini.google.com`
- `claude.ai`

Provider-specific prompt, upload, generation, and download adapters are intentionally separate from authorization so each action can remain narrowly scoped.
