# brief.robbymccullough.com

Static site for daily AI-generated briefs (HTML / images).

The live homepage is always the latest brief:

```text
index.html
```

Past briefs live as date-named static pages:

```text
briefs/YYYY-MM-DD.html
```

## Publish from the personal-brand generator

From this repo:

```sh
python3 scripts/publish-daily-brief.py
```

That script builds:

```text
/Users/mybbor/Library/CloudStorage/Dropbox/AI/personal-brand/daily-brief-site
```

Then it copies the generated latest brief to `index.html` and copies older
briefs to `briefs/YYYY-MM-DD.html`. By default, the latest brief is not also
duplicated in `briefs/`; tomorrow's run will archive it under its date.

## Deploy

Push to `main` → GitHub Actions SSHes into the Andromeda droplet and runs `git pull`
in `/var/www/brief.robbymccullough.com`. Served by Caddy. See the fleet's `AGENTS.md`
for server details.
