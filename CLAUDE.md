# marvynmylk-site

Marvyn Mylk's link-in-bio site. `index.html` is the whole page; photos and covers are in `images/`. Netlify republishes automatically on every push to `main`.

## Rules

- **Always show Marvyn a preview before anything goes live.** Screenshot the changed sections at phone size and send them; push to `main` only after he approves. Pushing publishes the live site immediately. Preferred preview: update the private "Marvyn Mylk Site Preview" artifact (https://claude.ai/artifact/3PbtVw8Duj6k14NpmnVYYb) with the full page so he can scroll it live.
- **Keep the link preview in sync.** `images/share.jpg` is built from `images/profile.webp`, `images/purple-south-cover.jpg` and `images/monster-on-tv-cover.jpg`. Whenever any of those three change (or the headline changes), rebuild it with `python3 tools/make_share_image.py`, check it, and commit it in the same change.
- **The preview image is profile + both covers + headline only.** No subline, labels, handles or footer text.
- **Keep Tyler (Marvyn's partner) out of every image.** He doesn't want to be public. Crop or edit him out of any photo before it goes on the site.
- **No "AI tells" in design:** no small eyebrow labels, source footers, handle footers or page numbers.
- **Sign-up forms** post to Netlify Forms (form name `book-news`). Keep `data-netlify="true"`, the hidden `form-name` input and the `bot-field` honeypot on the sign-up form (one form, at the end of the page).
- The `og:url` and `og:image` tags use the absolute address `https://marvynmylk.netlify.app`. Update them if the site's address changes.
