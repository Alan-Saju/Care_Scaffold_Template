# Care Connect

Staff consultation workflow for CARE

A [CARE](https://github.com/ohcnetwork/care) backend plugin. It is an ordinary Django app,
pip-installed into core and registered through `plug_config.py`. Core contains no reference
to this package.

## Install (local development)

Place the plugin inside the backend checkout as a **real directory**. A symlink breaks
`docker build`, which cannot follow links out of the build context.

```bash
mv /path/to/care_connect $CARE_BE/care_connect
```

`care/plug_config.py`:

```python
care_connect = Plug(
    name="care_connect",
    package_name="care_connect",
    version="",
    configs={
        "CONNECT_ENABLED": True,
    },
)

plugs = [care_connect, ...]
```

Plugins are pip-installed at **image build time**, so a newly registered plug needs a rebuild:

```bash
cd $CARE_BE
make down      # safe stop. NOT `make teardown` — that deletes the database volume.
make build     # re-runs install_plugins.py
make up
make makemigrations && make migrate
```

`backend` and `celery` share one image, so a single rebuild covers both.

## API

Mounted automatically at `/api/care_connect/` by core's `config/urls.py`.

| Method | Path | Description |
| --- | --- | --- |
| GET | `/api/care_connect/config/` | Client-safe configuration |
| GET | `/api/care_connect/consultations/` | List staff consultations, optionally filtered by `facility` |
| POST | `/api/care_connect/consultations/` | Create a draft or scheduled consultation |
| PATCH | `/api/care_connect/consultations/{external_id}/` | Update consultation details or lifecycle status |
| DELETE | `/api/care_connect/consultations/{external_id}/` | Soft-delete a consultation |

## Settings

Resolution order: `PLUGIN_CONFIGS["care_connect"][key]` → environment variable → default.
See `care_connect/settings.py`.
