Troubleshooting
=====================================

This page contains some advice about errors and problems commonly encountered during the development of Meetup Data Scraper.


max virtual memory areas vm.max_map_count [65530] likely too low, increase to at least [262144]
-----------------------------------------------------------------------------------------------

When using docker on some machines, you will need to manually extend the max virtual memory. For CentOS & Ubuntu use::

    $ sudo sysctl -w vm.max_map_count=262144

Or add it permanently use::

    $ echo "vm.max_map_count=262144" | sudo tee -a /etc/sysctl.conf
    $ sudo reboot

For more detils go to -> https://www.elastic.co/guide/en/elasticsearch/reference/current/vm-max-map-count.html
