构建：

```bash
docker build -t cj-cronjob:latest .
```

运行：

```bash
REPO_HOST=ghcr.1ms.run
VERSION=v0.2.3

cp .env.example .env

docker pull "$REPO_HOST/jiehui555/cj-cronjob:$VERSION"
docker run -d --env-file .env "$REPO_HOST/jiehui555/cj-cronjob:$VERSION"
```
