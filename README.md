打包：

```bash
docker build -t cj-auto-report .
```

运行：

```bash
#!/bin/bash

# 环境变量
BASE_URL=http://192.168.0.xx:8089
BOT_USERNAME=机器人
BOT_PASSWORD=xxx
SMTP_HOST=smtp.qq.com
SMTP_PORT=465
SMTP_PASS=xxx
SMTP_FROM=xxx
SMTP_TO=xxx

# 指定仓库
REPO_HOST=ghcr.1ms.run

# 执行脚本
docker pull "$REPO_HOST/jiehui555/cj-auto-report:latest"
docker run --rm \
    -e BASE_URL="$BASE_URL" \
    -e BOT_USERNAME="$BOT_USERNAME" \
    -e BOT_PASSWORD="$BOT_PASSWORD" \
    -e SMTP_HOST="$SMTP_HOST" \
    -e SMTP_PORT="$SMTP_PORT" \
    -e SMTP_PASS="$SMTP_PASS" \
    -e SMTP_FROM="$SMTP_FROM" \
    -e SMTP_TO="$SMTP_TO" \
    "$REPO_HOST/jiehui555/cj-auto-report:latest"
```
