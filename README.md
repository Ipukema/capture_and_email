This is a simple script atht alllows capturing and emailing a photograph from the laptop's built-in camera.

Usage:
1. Copy the script into an apppropriate directory (i.e. /usr/local/bin)
2. Create teh config file from template, copy it next to the script. Encode the password with base64.
3. Create a directory to keep the capture files, i.e. mkdir /var/log/camera
4. Run the script by hand. Make sure it works.
5. Make sure your /etc/pam.d/common_auth contains something like this:
	auth	[success=2 default=ignore]	pam_unix.so nullok_secure
	auth    [default=ignore]                pam_exec.so /usr/local/bin/capture_and_email.py
 
