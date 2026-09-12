# Care Connect (frontend)

Staff consultation workflow for CARE

A [care_fe](https://github.com/ohcnetwork/care_fe) plugin, loaded at runtime through Vite
Module Federation. It is a separate build; it never imports from `care_fe`.

## Develop

```bash
npm install
npm run dev        # vite preview :4173  +  vite build --watch
```

Enable it in `care_fe/.env.local`:

```
REACT_ENABLED_APPS=ohcnetwork/care_connect_fe@localhost:4173/assets/remoteEntry.js
```

Then restart the `care_fe` dev server — `.env.local` is not hot-reloaded.

> There is no HMR across the federation boundary. After the plugin rebuilds, **hard-reload**
> `care_fe`.

## Structure

| Path | Purpose |
| --- | --- |
| `src/manifest.tsx` | The only module federation exposes. Routes, components, nav items, side-effect registrations. |
| `src/utils/api.ts` | Fetch client. Uses `window.CARE_API_URL` and the staff/OTP token, with the `/otp` prefix applied automatically. |
| `src/components/Page.tsx` | Tailwind scoping wrapper. Wrap every rendered root. |
| `public/locale/en.json` | i18n keys, all prefixed `connect__`. |

The facility home action opens `/connect?facility=<facility external id>`, where staff can
create and review consultations through the plugin API.

## Conventions

- Every entry in `components` and `routes` must be `lazy()` — the manifest chunk loads on
  every page of `care_fe`.
- Every user-facing string is `t("connect__key")`, defined in this repo's `en.json`.
  Never add keys to `care_fe`'s locale files.
- `cssCodeSplit: false` and remote CSS is not auto-injected: do not depend on packages that
  ship their own stylesheets.
- Prop types are structural mirrors of `care_fe/src/pluginTypes.ts`, never imports.
