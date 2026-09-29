# 🌐 Netlify landing page for Smart Flashcards

This folder is a **complete, ready-to-publish static website**. It exists because
Netlify **cannot run Python or Streamlit** — it can only serve static files, so the
interactive app itself must be hosted elsewhere (see [`../DEPLOYMENT.md`](../DEPLOYMENT.md)).

```
netlify/
├── index.html      # the landing page (edit APP_URL inside!)
├── netlify.toml    # redirects so no path ever shows a 404
└── _redirects      # same rule in Netlify's plain-text format
```

---

## 🛠️ Fix your existing Netlify site (2 minutes)

Your site currently shows **"Page not found"** because the deploy contained no
`index.html`. Replace that deploy with this folder:

1. Open <https://app.netlify.com> → select your site (`dynamic-caramel-7a41c2`).
2. Go to the **Deploys** tab.
3. Scroll to the bottom, to the **"Need to update your site? Drag and drop your site
   output folder here to deploy."** drop zone.
4. Drag **this `netlify` folder** onto it (⚠️ drag the `netlify` folder itself — *not*
   the whole project folder, which has no `index.html` at its root).
5. Wait for the deploy to go green, then reload
   <https://dynamic-caramel-7a41c2.netlify.app> — the landing page will appear.

> **Prefer Git?** Connect the repository instead and leave the Netlify UI settings
> blank — the root `netlify.toml` already tells Netlify to publish `netlify/`.

---

## 🔗 Point the buttons at your deployed app

**While previewing locally this is already handled** — if you open `netlify/index.html`
directly (`file://`) or via `localhost`, the buttons automatically open the local
Streamlit server at `http://localhost:8501`, so nothing is broken on your machine.

To make the **public** Netlify site work, set the hosted URL once:

1. Deploy the Streamlit app first — see **Option A** in [`../DEPLOYMENT.md`](../DEPLOYMENT.md)
   (GitHub → <https://share.streamlit.io>). You will get a URL like
   `https://smart-flashcards-ai.streamlit.app`.
2. Open `netlify/index.html` and find this line near the bottom, in the `<script>` block:

   ```js
   const HOSTED_URL = "https://YOUR-APP-NAME.streamlit.app";
   ```

3. Replace the placeholder with your real app URL:

   ```js
   const HOSTED_URL = "https://smart-flashcards-ai.streamlit.app";
   ```

4. Re-deploy (repeat the drag-and-drop above).

As soon as `HOSTED_URL` no longer contains `YOUR-APP-NAME`, that URL takes priority
everywhere and the yellow notice never appears. The full config block is:

```js
const HOSTED_URL = "https://YOUR-APP-NAME.streamlit.app";  // public app (set this)
const LOCAL_URL  = "http://localhost:8501";                // local preview fallback
```


---

## ✅ Preview locally

Just double-click `index.html`, or serve the folder:

```powershell
cd C:\Users\admin\Desktop\smart-flashcards\netlify
python -m http.server 8000
# then open http://localhost:8000
```
