# Deploying ADAPT-D as a static site on Cloudflare Pages

This app now runs entirely in the browser via **stlite** (Streamlit compiled to
WebAssembly). There is no server process, nothing sleeps, and hosting on
Cloudflare Pages is free and always-on.

## What changed from the original repo

- **`index.html`** (new) — the stlite wrapper. It loads the Streamlit runtime in
  the browser and mounts `app.py`, the `tabs/` modules, `config.py`,
  `data_loader.py`, and the `data/` files.
- **`data/shap_data_prototype.csv.gz`** (replaces `shap_data_prototype.csv`) —
  the SHAP data, rounded and gzip-compressed: **7.7 MB → 0.30 MB**. Schema is
  unchanged.
- **`data_loader.py`** — `load_shap()` now reads the `.gz` file, with a fallback
  so it works no matter how the host serves the file.

Nothing else changed. `app.py` already referenced only the six tabs you kept.

## Option A — Connect your GitHub repo (recommended; auto-deploys on push)

1. Push this updated folder to your `ghazalbs/ADAPT-D` repo on the `main`
   branch. Make sure the old `data/shap_data_prototype.csv` is deleted and the
   new `data/shap_data_prototype.csv.gz` plus `index.html` are committed.
2. In the Cloudflare dashboard go to **Workers & Pages → Create → Pages →
   Connect to Git**, and pick the `ADAPT-D` repository.
3. On the build-settings screen:
   - **Framework preset:** None
   - **Build command:** *(leave empty — there is no build step)*
   - **Build output directory:** `/`
4. Click **Save and Deploy**. After a minute you get a live URL like
   `https://adapt-d.pages.dev`.
5. Every future `git push` to `main` redeploys automatically.

## Option B — Direct upload (no Git)

1. Zip this folder's contents (or use the provided zip).
2. In Cloudflare: **Workers & Pages → Create → Pages → Upload assets**.
3. Drag in the folder, keeping the structure (`index.html` at the top level,
   with `tabs/` and `data/` as subfolders). Deploy.

## Custom domain (optional)

Since your DNS is already on Cloudflare: open the Pages project → **Custom
domains → Set up a custom domain**, enter your domain or subdomain, and
Cloudflare wires up the DNS and SSL automatically.

## What to expect

- **First load is slow** (a few seconds to ~20s): the browser downloads the
  Python runtime and the pandas/numpy/plotly wheels. This is cached afterwards,
  so repeat visits and other users with a warm cache load quickly.
- The app then runs locally in each visitor's browser — no server cost, no
  idle-sleep, no cold starts.

## Troubleshooting

- **A data file 404s / "file not found" error:** the `data/` or `tabs/`
  folder structure wasn't preserved on upload. Re-upload keeping subfolders.
- **Stuck on the loading spinner:** open the browser console (F12). A red error
  usually points to a Python package that isn't available in Pyodide. The
  current requirements (`plotly`, `pandas`, `numpy`) are all supported.
- **You add a new Python file or data file later:** add a matching entry to the
  `files: { ... }` map in `index.html`, otherwise stlite won't mount it.
- **Local testing before deploy:** from this folder run
  `python3 -m http.server 8000` and open `http://localhost:8000/`. Opening
  `index.html` directly with `file://` will *not* work — it must be served over
  HTTP.

## Still want the VPS version too?

The repo also still works as a normal server app (`streamlit run app.py`) using
`requirements.txt`, if you ever want to run it on your DigitalOcean or Hostinger
VPS instead. The static build above is the cheaper, always-on option.
