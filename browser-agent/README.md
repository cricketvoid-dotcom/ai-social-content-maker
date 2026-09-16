# ContentForge Restricted Chrome Agent

This local agent is the browser-automation layer for Creative Studio. It uses a dedicated Chrome profile and a dedicated workspace so the automation does not use the user's normal Chrome profile.

## What V1 does

- launches Google Chrome through Playwright
- uses a dedicated `browser-agent/profile` directory
- stores downloads only in `browser-agent/workspace/output`
- accepts input images only from `browser-agent/workspace/input`
- blocks navigation outside an explicit allowlist
- keeps browser automation separate from the hosted ContentForge app
- leaves login to the user; the agent never receives or stores passwords

## Important security boundary

This is a browser-level restriction, not a full operating-system sandbox. Chrome itself runs as a normal desktop process. Do not treat this as equivalent to a VM or OS-level sandbox. Keep the dedicated Chrome profile free of personal accounts and sensitive data.

## Setup

1. Install Python 3.11+.
2. From this folder run:

```bash
python -m pip install -r requirements.txt
python -m playwright install chrome
```

3. Put a test product image in `workspace/input/`.
4. Run:

```bash
python agent.py --url https://example.com
```

For real providers, add their domain to `config.json` first. V1 intentionally does not automate arbitrary websites.

## Next step

Provider adapters will be added separately. Each adapter will have explicit allowed domains and narrowly-scoped actions such as opening the provider, uploading one selected image, entering a generated prompt, waiting for the result, and downloading it into the workspace.
