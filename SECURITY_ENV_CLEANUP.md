# 🔐 Env-file cleanup: what was done & what YOU still need to do

> **Status:** git history was cleaned **on this computer only**. Nothing has been pushed to GitHub yet.
> Until you finish **Step 2** (force-push), the leaked secrets are still visible on GitHub.

---

## ✅ What was already done (locally)

| | Change |
|---|---|
| 🧹 | `backend/.env`, `frontend/.env` and `frontend/.env.local` were **removed from every commit** on all 6 branches: `main`, `bhavna-branch`, `branch2`, `kartik-branch`, `reception`, `recovery-appointment`. |
| 🔁 | Leaked values that had also been copied into other files were **replaced with placeholders in every commit**. Those files were `IMPLEMENTATION_SUMMARY.md`, `PAYMENT_ARCHITECTURE.txt`, `RAZORPAY_PAYMENT_INTEGRATION.md`, `RAZORPAY_QUICK_REFERENCE.md`, `README_PAYMENT.md` and `backend/hospital_ops/settings.py`. The values were 3 MySQL passwords, the OpenWeather API key, and the Razorpay key ID and secret. |
| 📜 | **Every commit is still there.** Commit count per branch, messages, authors and dates are unchanged (verified: main 33, bhavna-branch 13, branch2 32, kartik-branch 34, reception 11, recovery-appointment 22). |
| 🧾 | `.gitignore` and `backend/.gitignore` now actually ignore `.env` files (the old rules were commented out). |
| 📄 | Safe templates: `backend/.env.example` and a new `frontend/.env.example`. |
| 💾 | Your real local `.env` files are still on disk. They are now untracked and ignored. |
| 🛟 | Full backup of the old history: `..\hospital-BACKUP-before-env-cleanup.bundle` (in the folder above the project). |

### ℹ️ Why the commit IDs (hashes) changed

A commit's hash is calculated from its files. Removing a file from a commit **always** gives it a new hash. There is no way around this. Every commit is still in history; only the IDs are new. This is why all teammates must re-clone (Step 3).

| Branch | Old tip (on GitHub now) | New tip (local) |
|---|---|---|
| main | `6f82f8e` | `4038459` |
| bhavna-branch | `66be4de` | `450a3de` |
| branch2 | `09759cc` | `3ab0590` |
| kartik-branch | `2c1753e` | `fa436a4` |
| reception | `bf962f2` | `3a849dc` |
| recovery-appointment | `c2c3e48` | `6ff329b` |

---

## 🚨 Step 1 — Rotate every leaked secret (most important)

Removing secrets from history does **not** make them safe. Anyone who cloned, forked or viewed the repo may already have them. Treat them as public and replace them:

- [ ] **Razorpay keys.** Razorpay Dashboard → *Account & Settings* → *API Keys* (Test mode) → **Regenerate key**.
- [ ] **OpenWeatherMap API key.** <https://home.openweathermap.org/api_keys> → create a new key → **delete the old one**.
- [ ] **MySQL passwords.** Kushal, Kartik and Sagar each committed their own. Each person changes theirs:
  ```sql
  ALTER USER 'root'@'localhost' IDENTIFIED BY 'a-new-strong-password';
  FLUSH PRIVILEGES;
  ```
- [ ] If any of those passwords is **reused anywhere else** (email, other accounts), change it there too. One of them looks like it is based on an email address.
- [ ] Put the new values in your local `backend/.env` only.
- [ ] Generate a real Django `SECRET_KEY` for your `.env`:
  ```bash
  python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
  ```

---

## 🚀 Step 2 — Push the cleaned history to GitHub

1. **Tell your team first.** Ask everyone to push any pending work now, then stop pushing until you're done.
2. If `main` (or any branch) is protected: GitHub → *Settings* → *Branches* → temporarily **allow force pushes**.
3. From the project folder, run the commands below.

   `--force-with-lease` only overwrites a branch if it is still at the old commit shown in the table above. If a teammate pushed something new in the meantime, the push is **rejected** instead of deleting their work. If that happens, see *Troubleshooting*.

   ```bash
   git push origin --force-with-lease=main:6f82f8e5b09759610867a60df6333e40841932ad main
   git push origin --force-with-lease=bhavna-branch:66be4dec06edd9cec650afc03816e1ec7d08d2f1 bhavna-branch
   git push origin --force-with-lease=branch2:09759cc50afb3fdbee04d3b90e669e4d15c5cd1a branch2
   git push origin --force-with-lease=kartik-branch:2c1753e2fcbaac8f88a04b6d297ee5f25b47fe31 kartik-branch
   git push origin --force-with-lease=reception:bf962f2e9b6ebad40ca790285a6f92e476c27365 reception
   git push origin --force-with-lease=recovery-appointment:c2c3e48c5dc78cc72dbc0399d6175c4797742b9f recovery-appointment
   ```
4. Turn branch protection back on.
5. Check on GitHub that `backend/.env` no longer appears in any commit.

### Then commit the new UI / README / gitignore work (a normal commit on top)

```bash
git add -A
git status          # make sure NO .env or .env.local files are listed
git commit -m "Modern UI redesign with animations, updated README, fix env handling"
git push origin main
```

---

## 👥 Step 3 — Every teammate must re-clone

Old clones still contain the secrets and the **old** history. If anyone pulls, merges or pushes from an old clone, the leaked files come back.

**No unpushed work?** Delete the old folder and clone again:

```bash
git clone https://github.com/kushal-s0/Hospital-Operations-Sync-Platform.git
```

**Have unpushed commits?** Move them over as patches:

```bash
# inside the OLD clone, on your branch
git format-patch origin/<your-branch>..HEAD -o ../my-patches

# fresh clone
git clone https://github.com/kushal-s0/Hospital-Operations-Sync-Platform.git
cd Hospital-Operations-Sync-Platform
git checkout <your-branch>
git am ../my-patches/*.patch
```

> ❌ Do **not** run `git pull` in an old clone. It merges the old history (and the secrets) back in.

Everyone then creates their own env files from the templates:

```bash
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

---

## 🧽 Step 4 — Clean up what GitHub still remembers

- [ ] **Forks:** GitHub → *Insights* → *Forks*. Forks keep the old history; ask their owners to delete them or re-fork.
- [ ] **Pull requests:** closed and open PRs that point at old commits keep those commits viewable.
- [ ] **Cached commits:** old commits can stay reachable by their hash for a while. You can ask [GitHub Support](https://support.github.com/contact) to *remove cached views and run garbage collection* for the repository. Mention the old commit IDs from the table above.

Because the secrets were rotated in Step 1, anything left in these places is harmless.

---

## 🗑️ Step 5 — Delete the backup (after everything works)

`..\hospital-BACKUP-before-env-cleanup.bundle` contains the **old secrets**. Once the push worked and the team has re-cloned, delete it:

```powershell
Remove-Item "..\hospital-BACKUP-before-env-cleanup.bundle"
```

---

## 🔍 Other things worth checking

- **`dump.sql` is committed.** Make sure it contains only fake/sample data. No real patient information or real password hashes.
- **Demo passwords** (e.g. `admin123`) appear in `start.bat`, `QUICKSTART.md` and the `backend/*.py` helper scripts. They are fine for local development, but change them on any real deployment.
- **Before deploying:** set `DEBUG=False`, use a unique `SECRET_KEY`, and restrict `ALLOWED_HOSTS` / CORS in `settings.py`.
- **Optional:** add a secret scanner so this can't happen again, e.g. [gitleaks](https://github.com/gitleaks/gitleaks) as a pre-commit hook.

---

## 🛠️ Troubleshooting

**A push was rejected with "stale info".** Someone pushed new commits to that branch after the cleanup. Don't use plain `--force`. First fetch their work:
```bash
git fetch origin <branch>
git log --oneline <old-tip-from-table>..origin/<branch>   # the new commits
```
Copy those commits onto the cleaned branch with `git cherry-pick <commit>`. Check they don't re-add any `.env` file, then run the `--force-with-lease` push again with the new expected value.

**Something went wrong and you need the old history back:**
```bash
git clone "..\hospital-BACKUP-before-env-cleanup.bundle" hospital-restored
```

**Check that the cleaned history is really clean:**
```bash
git log --all --oneline -- backend/.env frontend/.env frontend/.env.local   # should print nothing
```
