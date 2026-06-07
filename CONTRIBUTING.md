# Contributing

## Branch workflow

This repo uses a protected `main` branch. All changes go through a pull request.

```
main        ← protected, deploy-ready at all times
  └── dev   ← integration branch, PRs merge here first
       └── feature/your-feature   ← your work branch
```

## How to make a change

**Step 1 — Create a feature branch from dev**
```bash
git checkout dev
git pull origin dev
git checkout -b feature/your-feature-name
```

**Step 2 — Make your changes and commit**
```bash
git add .
git commit -m "feat: describe what you did"
git push -u origin feature/your-feature-name
```

**Step 3 — Open a pull request**
- Go to github.com/ganeshputran/ai-devops-bot
- Click **Compare & pull request**
- Set base: `main`, compare: `feature/your-feature-name`
- The CI pipeline runs automatically:
  - ✅ 15 pytest tests must pass
  - 🤖 Gemini AI reviews your code diff
  - 🤖 Gemini AI explains any failures

**Step 4 — Merge after CI passes**
- Check the AI code review comment on the PR
- Merge when all checks are green

---

## Commit message format

```
feat:     new feature
fix:      bug fix
docs:     documentation only
refactor: code change with no new feature or fix
test:     adding or updating tests
chore:    maintenance (deps, config, CI)
```

## Branch naming

```
feature/add-docker-support
fix/dashboard-404
docs/update-readme
refactor/gemini-utils-cleanup
```

---

## What the CI pipeline checks on every PR

| Check | What it does |
|-------|-------------|
| pytest (15 tests) | Must pass — blocks merge if any fail |
| Coverage threshold | Must be ≥ 80% |
| AI failure explainer | Posts plain-English fix if tests fail |
| AI code reviewer | Reviews all changed .py .yml .html .js files |
| Docker build | Builds image to verify Dockerfile is valid |
