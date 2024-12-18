# Service Control

This package provides a simple means for controling Systemd services remotely.  
It uses NiceGUI to run a simple web page with Enable/Disable, Start/Stop, and system reboot options.

## Environment Setup on Raspberry Pi Zero 2

These instructions assume starting with a fresh install of Raspberry Pi OS Lite (Bookworm).  

1. Install OS packages:

   ```bash
   sudo apt update
   sudo apt upgrade
   sudo apt install python3-pip python3-venv python3-setuptools git libsystemd-dev python3-pystemd
   sudo reboot now
   ```

2. Create a Python virtual environment

   ```bash
   python -m venv service_control_env
   ```

3. Install Python packages into the virtual environment

   ```bash
   source service_control_env/bin/activate
   pip install nicegui pystemd

   ```

4. Clone the project

   Create a new SSH key for the system and add it to GitHub.

   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   ```

   Setup Git.

   ```bash
   git config --global user.name "Mona Lisa"
   git config --global user.email "YOUR_EMAIL"
   ```

   Clone to project.

   ```bash
   git clone git@github.com:mptsolutions/service_control.git
   ```

## Config setup

1. Rename ```config_template.py``` to ```config.py``` and update with correct values.

## Manual run

```bash
source /home/pi/service_control_env/bin/activate
sudo /home/pi/service_control_env/bin/python /home/pi/service_control/main.py
```

## Auto run on boot

1. Copy ```service_control.service``` to ```/lib/systemd/system/```.
2. Run ```sudo systemctl daemon-reload```
3. Run ```sudo systemctl enable service_control.service```

## Samba access setup

This will allow remote access to the ```pi``` user directory for easier file editing.

1. Install Samba

   ```bash
   sudo apt install samba samba-common-bin
   ```

2. Edit the ```smb.conf```

   ```bash
   sudo nano /etc/samba/smb.conf
   ```

   Update the workgroup line:

   ```bash
   workgroup = [HOME WORKGROUP NAME]
   ```

   Make home directories accessible:

   ```bash
   [homes]
      comment = Home Directories
      browseable = yes

   # By default, the home directories are exported read-only. Change the
   # next parameter to 'no' if you want to be able to write to them.
      read only = no
   ```

   Add a share for the ```pi``` user home directory:

   ```bash
   [f1_buzzer]
   path = /home/pi
   writeable=yes
   browseable=yes
   public=yes
   ```
