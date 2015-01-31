# Monitoring Apache using Zabbix

The script and template are taken from https://www.zabbix.org/wiki/Docs/howto/apache_monitoring_script#Method_2
* Verified working with Zabbix v2.2 appliance. Original template did not work with Zabbix v2.2 :( . *Item Key* configuration had to be updated.
* The **BIG** advantage of this script is that it's "non-intrusive" - the Zabbix agent doesn't need to be running on the Apache hosts you want to monitor.
* Other Methods (https://www.zabbix.org/wiki/Docs/howto/apache_monitoring_script) may suit your needs better since they cache the status page result for a short duration to process all statistics.

## Installation

### Zabbix 2.2 appliance

#### Install the script
 sudo install -o root -g root -m 0755 query_apachestats.py /usr/share/zabbix/externalscripts/query_apachestats.py

#### On Zabbix web application
 Now import zabbix_apache_template.xml and bind "Template_Apache_Stats" to the Apache host.


### Customization
Q: My apache server uses https or is hosted at another url context ?  
A: Please update the python script according to your environment.
