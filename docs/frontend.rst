Frontend
=====================================

.. index:: Angular
.. index:: Frontend

The Frontend is written as an Angular app. The source code is in a extra 
git repo https://github.com/linuxluigi/meetup-data-scraper-angular

For developing the frontend it's best to run the flask app in background. 
The develoing settings of the app try to make ``PUT`` request on 
``http://localhost:5000`` and the production site is designt to run 
on the same domain as the backend. 

To run the frontend & backend on the same domain `traefik <https://containo.us/traefik/>`_
is setup to handle every ``http`` & ``https`` request. The default setup is that every
traffik goes to the angular app (NGINX server) and only http ``PUT`` request go to
the flask backend app.
