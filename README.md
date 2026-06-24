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

If the generator contains TRMNL e-ink briefs in `content/trmnl-briefs/`, the
same publish command also copies the latest static display brief to:

```text
trmnl.html
```

and dated archives to:

```text
trmnl/YYYY-MM-DD.html
```

## Deploy

Push to `main` → GitHub Actions SSHes into the Andromeda droplet and runs `git pull`
in `/var/www/brief.robbymccullough.com`. Served by Caddy. See the fleet's `AGENTS.md`
for server details.

Normal daily publish:

```sh
python3 scripts/publish-daily-brief.py
git add .
git commit -m "Add brief for YYYY-MM-DD"
git push origin main
```

If plain `git push` routes through SSH and blocks on 1Password, either unlock
1Password and push over SSH, or push with the GitHub CLI token URL:

```sh
git push "https://x-access-token:$(gh auth token)@github.com/RobbyMcCullough/brief.robbymccullough.com.git" main
```

Verify after deploy:

```sh
curl -sI https://brief.robbymccullough.com/ | head -1
curl -sI https://brief.robbymccullough.com/briefs/YYYY-MM-DD.html | head -1
```
