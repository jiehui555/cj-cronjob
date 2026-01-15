# Scheduler Setup Guide

This project supports multiple methods for automated daily execution at 8:00 AM:

## Project Structure
```
cj-auto-report/
├── src/
│   ├── cron/
│   │   ├── __init__.py
│   │   └── scheduler.py      # Python scheduler
│   ├── utils/
│   │   ├── email.py
│   │   └── image.py
│   ├── app.py
│   └── config.py
├── run.bat                    # Direct job execution
├── scheduler.bat              # Python scheduler (Windows)
└── main.py
```

## Method 1: Python Schedule (Cross-platform)

### Run the scheduler:
```bash
# Windows
scheduler.bat

# Linux/Mac
python -m src.cron.scheduler
```

The scheduler will:
- Run immediately once at startup (for testing)
- Then run every day at 8:00 AM (Asia/Shanghai timezone)
- Keep running in the foreground

### To run in background:
```bash
# Windows (use Task Manager or run as service)
start /b python -m src.cron.scheduler

# Linux/Mac (use nohup)
nohup python -m src.cron.scheduler &
```

## Method 2: Windows Task Scheduler (Recommended for Windows)

### Step 1: Test the batch file
Double-click `run.bat` to make sure it works correctly.

### Step 2: Create scheduled task via GUI
1. Open **Task Scheduler** (search in Start menu)
2. Click **Create Basic Task**
3. Name: `DailyScreenshotJob`
4. Description: `Automated daily screenshot and email report`
5. Trigger: **Daily** at **8:00 AM**
6. Action: **Start a program**
7. Program/script: `C:\path\to\run.bat`
8. Start in: `D:\Projects\VscodeProjects\cj-auto-report`
9. Finish and test

### Step 3: Create scheduled task via Command Line
Run as Administrator:
```cmd
schtasks /create /tn "DailyScreenshotJob" /tr "C:\path\to\run.bat" /sc daily /st 08:00 /ri 1 /du 24:00 /f
```

To check existing tasks:
```cmd
schtasks /query /tn "DailyScreenshotJob"
```

To delete task:
```cmd
schtasks /delete /tn "DailyScreenshotJob" /f
```

## Method 3: Linux/Mac Cron

Edit crontab:
```bash
crontab -e
```

Add:
```cron
0 8 * * * cd /path/to/cj-auto-report && /usr/bin/python3 main.py >> /path/to/logs/screenshot.log 2>&1
```

## Configuration

The scheduler uses the same `.env` configuration as the main application. Make sure your `.env` file is properly configured:

```env
BASE_URL=your_url
BOT_USERNAME=your_username
BOT_PASSWORD=your_password
SMTP_HOST=smtp.qq.com
SMTP_PORT=465
SMTP_PASS=your_smtp_password
SMTP_FROM=your_email@qq.com
SMTP_TO=recipient@example.com
```

## Monitoring

### Logs
Check the console output or log files for execution status.

### Email Notifications
The email utility will send reports daily. If you don't receive emails, check:
1. SMTP configuration in `.env`
2. Email service provider settings
3. Spam folder

## Troubleshooting

### Scheduler not running
- Check if Python environment is activated
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check file permissions

### Job fails
- Run manually first: `python main.py`
- Check browser automation: ensure Playwright is installed: `playwright install chromium`
- Verify network connectivity and authentication

### Email not sending
- Test SMTP settings manually
- Check if attachments exist before sending
- Verify recipient email address