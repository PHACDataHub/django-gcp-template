# Django-Jinja GCP template
This is a stripped-down version of the llm-playground repo, intended to serve as a template for other PHAC Django applications on GCP.

I somewhat followed the tutorial at https://cloud.google.com/python/django/appengine to deploy to GCP App Engine.

Some aspects of this repo are based on other PHAC Django projects, e.g. the base Jinja template.

## Setup

Clone this repo. Create a venv in the repo root and activate it. Using Python 3.11, `pip install -r requirements.txt`.

## Customizing to your own project / app name

(TODO)

## Issues and fixes vs. GCP tutorial

### Secrets

Creating the secret required some fiddling due to org-level settings.

Also the secret came out in UTF-16 and wouldn't decode. Set the SECRET_KEY manually in the gcp.env before running the following commands.
```bash
gcloud secrets create django_settings --data-file gcp.env --locations=us-east1 --replication-policy=user-managed
gcloud secrets add-iam-policy-binding django_settings --member serviceAccount:<gcp-project-name>@appspot.gserviceaccount.com --role roles/secretmanager.secretAccessor
```

To update the gcp.env used in App Engine, first delete it with `gcloud secrets delete django_settings` then re-run the commands above.

Note that there is a `gcp.env` and a local `.env`. More about this later.

### APPENGINE_URL env variable

The tutorial says to update the `APPENGINE_URL` in `app.yaml` to `https://<project-name>.uc.r.appspot.com`. However, if you have deployed to a region other than US central ("uc") then this will fail. Ensure to copy the actual URL from your browser's address bar. In my case, it was "ue" (US East), not "uc".

### Sending emails to GC addresses

Sending login emails through SMTP (SendGrid) works for gmail addresses, but is blocked by GC M365 filtering.

A second option is to use GC Notify for email sending. But GC Notify emails *also* get sent to Junk Mail by M365. And the M365 link checking invalidates the magic links unless you disable a number of security features in `settings.py`:

```python
MAGICLINK_TOKEN_USES = 3  # M365 "clicks" links to check them, so must be > 1
MAGICLINK_REQUIRE_SAME_IP = False  # Otherwise M365 checks will invalidate token
MAGICLINK_REQUIRE_SAME_BROWSER = False  # As above
```

The third method (that actually works!) is to use Power Automate to send the email. These go straight to the inbox within a few seconds. Sometimes the M365 link-checking seems to invalidate the link from this method, so best to leave the settings as above.

### requirements.txt

GCP expects requirements.txt to be in the root of the django project, rather than in the repo root.

## .env

The `.env` files should be in the repo root directory. It is not used directly for GCP, but rather the contents of the file are stored in a secret. The file is almost the same for both local dev and GCP secret.

Here's the GCP version (which I call `gcp.env`). There is an example file included in this repo. Just rename it to `gcp.env` and fill in the values.

```env
DATABASE_URL=postgres://(get this from gcp...)
GS_BUCKET_NAME=(create a bucket for document uploads in GCP storage)
SECRET_KEY=...(something random)
GC_NOTIFY_API_KEY=...
GC_NOTIFY_TEMPLATE_ID=...
POWER_AUTOMATE_URL=https://...

MAGICLINK_METHOD=power_automate  # One of power_automate, django_smtp, gc_notify
ALLOWED_EMAIL_DOMAINS=phac-aspc.gc.ca  # Comma separated list of allowable email domains for users
```

For local development, copy the file and save as `.env`, then uncomment the line:

```
USE_CLOUD_SQL_AUTH_PROXY=True
```

Before running the django server, start the cloud-sql-proxy as described in the tutorial. I needed to add the `-g` flag:

```
cloud-sql-proxy -g <GCP-project-name>:<GCP-region>:<SQL-instance-ID>
```
