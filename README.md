# Swedish Flashcards

This is a lightweight flashcard app designed for personal Swedish study on iPhone. It includes Swedish vocabulary and a second daily-sentence deck for common phrases.

## What is in it

- Swedish vocabulary deck with English meaning
- Daily sentence deck with Swedish sentence + English translation
- Flip-card study flow
- "Again", "I knew it", and "Next card" actions
- Study mode for only new words
- Installable PWA-style behavior for iPhone home screen

## GitHub Pages deployment

This app is ready to be hosted as a static site on GitHub Pages.

### Deploy steps

1. Push this folder to a GitHub repository.
2. In GitHub, open the repository.
3. Go to Settings → Pages.
4. Set the source to GitHub Actions.
5. Push a commit and the workflow in `.github/workflows/deploy-pages.yml` will publish the site automatically.

### Local preview

To test locally before publishing:

```bash
python -m http.server 8000
```

Then open:

```text
http://localhost:8000
```

## Important note

This app is a static web app, not a native iPhone app. It works best when hosted on a service that stays online, so it remains accessible even when your laptop is asleep or off.

## Notes

This is intentionally small and personal-use focused, which keeps it fast and simple to use while commuting or studying on the go.
