# brief.robbymccullough.com

Static site for daily AI-generated briefs (HTML / images). Currently a placeholder.

## Deploy

Push to `main` → GitHub Actions SSHes into the Andromeda droplet and runs `git pull`
in `/var/www/brief.robbymccullough.com`. Served by Caddy. See the fleet's `AGENTS.md`
for server details.
