# Thermal Data Collector - Cron Setup Guide

## 1. Create Configuration File

Create `thermal_config.json`:

```json
{
  "cameras": [
    {
      "camera_id": "archer",
      "url": "https://app.cell-guardian.com/monitor/06789238-2655-417a-8765-23577a07743a/dashboard",
      "video_selector": ".video-control",
      "wait_time": 5,
      "field_selectors": {
        "temperature": "#temp-reading",
        "humidity": "#humidity-reading",
        "motion_detected": "#motion-status",
        "alert_level": "#alert-level"
      }
    },
    {
      "camera_id": "thermal_cam_2",
      "url": "https://app.cell-guardian.com/camera/2",
      "video_selector": ".video-control",
      "wait_time": 5,
      "field_selectors": {
        "temperature": "#temp-reading",
        "humidity": "#humidity-reading",
        "motion_detected": "#motion-status",
        "alert_level": "#alert-level"
      }
    }
  ],
  "login": {
    "username_field": "#username",
    "password_field": "#password",
    "submit_button": "#login-button",
    "username": "your_username",
    "password": "your_password"
  }
}
```

**Note:** If no login needed, remove the `"login"` section entirely.

## 2. Install Dependencies

Create [requirements.txt][rq] file...  dependencies:

requirements.txt:

```txt
pandas>=2.0.0
selenium>=4.38.0
webdriver-manager>=4.0.2
```

...and install

```bash
pip install -r requirements.txt
```

[rq]: ../requirements.txt

## 3. Test the Script Manually

```bash
# Test collection
python thermal_collector.py --config thermal_config.json --output-dir ~/thermal_data

# Check stats
python thermal_collector.py --config thermal_config.json --output-dir ~/thermal_data --stats

# Test labeling
python thermal_collector.py --config thermal_config.json --output-dir ~/thermal_data --label
```

## 4. Create Wrapper Script

Create `run_thermal_collector.sh`:

```bash
#!/bin/bash

# Set paths
SCRIPT_DIR="$HOME/thermal_collector"
CONFIG_FILE="$SCRIPT_DIR/thermal_config.json"
OUTPUT_DIR="$HOME/thermal_data"
PYTHON_BIN="$HOME/.local/bin/python3"  # Adjust to your Python path

# Activate virtual environment if using one
# source $SCRIPT_DIR/venv/bin/activate

# Set display for headless Chrome (important for cron)
export DISPLAY=:0

# Run the collector
cd "$SCRIPT_DIR"
$PYTHON_BIN thermal_collector.py \
    --config "$CONFIG_FILE" \
    --output-dir "$OUTPUT_DIR"

# Exit with script's exit code
exit $?
```

Make it executable:
```bash
chmod +x run_thermal_collector.sh
```

## 5. Setup Cron Job

Edit crontab:
```bash
crontab -e
```

Add this line for every 30 minutes:
```cron
*/30 * * * * /home/yourusername/thermal_collector/run_thermal_collector.sh >> /home/yourusername/thermal_data/logs/cron.log 2>&1
```

### Cron Schedule Examples

```cron
# Every 30 minutes
*/30 * * * * /path/to/run_thermal_collector.sh

# Every hour at minute 0
0 * * * * /path/to/run_thermal_collector.sh

# Every 15 minutes
*/15 * * * * /path/to/run_thermal_collector.sh

# Every 2 hours
0 */2 * * * /path/to/run_thermal_collector.sh

# Specific times (8 AM and 8 PM daily)
0 8,20 * * * /path/to/run_thermal_collector.sh
```

## 6. Verify Cron is Running

```bash
# Check if cron service is running
sudo systemctl status cron

# View your cron jobs
crontab -l

# Check cron execution log
grep CRON /var/log/syslog

# Check your application logs
tail -f ~/thermal_data/logs/cron.log
tail -f ~/thermal_data/logs/collector_*.log
```

## 7. Monitor Collection

Create a monitoring script `check_collection.sh`:

```bash
#!/bin/bash

OUTPUT_DIR="$HOME/thermal_data"
PYTHON_BIN="python3"

cd ~/thermal_collector

echo "========================================"
echo "Thermal Data Collection Status"
echo "========================================"
echo "Last run: $(date)"
echo ""

# Get stats
$PYTHON_BIN thermal_collector.py \
    --config thermal_config.json \
    --output-dir "$OUTPUT_DIR" \
    --stats

# Show recent logs
echo ""
echo "========================================"
echo "Recent Log Entries (last 10 lines)"
echo "========================================"
tail -10 "$OUTPUT_DIR/logs/collector_$(date +%Y%m).log"
```

Run periodically to check status:
```bash
./check_collection.sh
```

## 8. Disk Space Management

Create cleanup script `cleanup_old_data.sh`:

```bash
#!/bin/bash

OUTPUT_DIR="$HOME/thermal_data"
DAYS_TO_KEEP=30  # Keep 30 days of unlabeled data

# Remove unlabeled images older than X days
find "$OUTPUT_DIR/images" -name "*.png" -type f -mtime +$DAYS_TO_KEEP -delete
find "$OUTPUT_DIR/metadata" -name "*.json" -type f -mtime +$DAYS_TO_KEEP -delete

# Keep labeled data and logs forever (or adjust as needed)

echo "Cleanup complete: $(date)" >> "$OUTPUT_DIR/logs/cleanup.log"
```

Add to crontab to run daily:
```cron
0 2 * * * /home/yourusername/thermal_collector/cleanup_old_data.sh
```

## 9. Email Notifications (Optional)

Install mail utils:
```bash
sudo apt-get install mailutils
```

Modify `run_thermal_collector.sh` to send email on failure:

```bash
#!/bin/bash

SCRIPT_DIR="$HOME/thermal_collector"
CONFIG_FILE="$SCRIPT_DIR/thermal_config.json"
OUTPUT_DIR="$HOME/thermal_data"
PYTHON_BIN="python3"
EMAIL="your-email@example.com"

export DISPLAY=:0

cd "$SCRIPT_DIR"
$PYTHON_BIN thermal_collector.py \
    --config "$CONFIG_FILE" \
    --output-dir "$OUTPUT_DIR"

EXIT_CODE=$?

# Send email if failed
if [ $EXIT_CODE -ne 0 ]; then
    echo "Thermal collector failed at $(date)" | \
    mail -s "Thermal Collector Error" "$EMAIL"
fi

exit $EXIT_CODE
```

## 10. Systemd Service (Alternative to Cron)

If you prefer systemd over cron, create `/etc/systemd/system/thermal-collector.service`:

```ini
[Unit]
Description=Thermal Data Collector
After=network.target

[Service]
Type=oneshot
User=yourusername
WorkingDirectory=/home/yourusername/thermal_collector
Environment="DISPLAY=:0"
ExecStart=/home/yourusername/.local/bin/python3 thermal_collector.py --config thermal_config.json --output-dir /home/yourusername/thermal_data
StandardOutput=append:/home/yourusername/thermal_data/logs/cron.log
StandardError=append:/home/yourusername/thermal_data/logs/cron.log

[Install]
WantedBy=multi-user.target
```

Create timer `/etc/systemd/system/thermal-collector.timer`:

```ini
[Unit]
Description=Run Thermal Data Collector every 30 minutes

[Timer]
OnBootSec=5min
OnUnitActiveSec=30min
Persistent=true

[Install]
WantedBy=timers.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable thermal-collector.timer
sudo systemctl start thermal-collector.timer

# Check status
sudo systemctl status thermal-collector.timer
sudo systemctl list-timers
```

## 11. Labeling After Collection Period

After several days of collection:

```bash
# Check how much data you have
python thermal_collector.py --config thermal_config.json --output-dir ~/thermal_data --stats

# Start labeling
python thermal_collector.py --config thermal_config.json --output-dir ~/thermal_data --label
```

The labeling tool will show you images one at a time and you can press:
- `p` for person
- `n` for no person  
- `u` for uncertain
- `s` to skip
- `q` to quit

After labeling, `training_dataset.csv` will be automatically generated.

## Troubleshooting

**Cron job not running:**
```bash
# Check cron is running
sudo systemctl status cron

# Check for errors
grep CRON /var/log/syslog | tail -20
```

**Chrome/Selenium issues:**
```bash
# Install Chrome if not present
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
sudo apt-get install -f

# Install ChromeDriver
pip install webdriver-manager
```

**Display issues in cron:**
- Make sure `export DISPLAY=:0` is in your wrapper script
- Or run truly headless with `--headless=new` Chrome option

**Permission issues:**
- Ensure output directory is writable: `chmod 755 ~/thermal_data`
- Check script is executable: `chmod +x run_thermal_collector.sh`
