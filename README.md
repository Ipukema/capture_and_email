This is a simple script taht alllows capturing and emailing a photograph from the laptop's built-in camera on a failed login attempt.
<br>
<h3>.Usage (on Linux):</h3>
<ol>
<li>Copy the script into an apppropriate directory (i.e. /usr/local/bin)
<li>Create a  config file from template, copy it next to the script. Encode the password with base64.
<li>Create a directory to keep the capture files, i.e. mkdir /var/log/camera
<li>Run the script by hand. Make sure it works.
<li>Make sure your /etc/pam.d/common_auth contains something like this:
<pre>
	auth	[success=2 default=ignore]	pam_unix.so nullok_secure
	auth    [default=ignore]                pam_exec.so /usr/local/bin/capture_and_email.py
</pre>
</ol>
<s>
<h3>.Usage (on OS X):</h3>
<li>install pythin3 using homeberew (brew install homebrew) - I cannot beelieve OSX does not have python3 by default
<li>install imagesnap utility using homeberew (brew install imagesnap)
<li>Copy and configure the script (same as in linux version); use osx config template
<li>Copy the log monitoring scipt into your /System/Library/StartupItems/: cp monitor_login.sh.osx /System/Library/StartupItems/monitor_login.sh
</ol
</s> - sorry, it is a bit trickier for MacOS X. MacOS has securitty restrictions taht pprevent an app to connect to window server before login. 
