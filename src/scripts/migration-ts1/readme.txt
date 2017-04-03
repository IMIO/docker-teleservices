scripts usage
-------------
- import-forms.py

  >> sudo -u  wcs-au-quotidien wcsctl -f /etc/wcs/wcs-au-quotidien.cfg runscript --vhost=test-formulaires.guichet-citoyen.be /opt/publik/scripts/migration-ts1/import-forms.py /opt/publik/scripts/migration-ts1/forms/

  Docker sample execution :

  for i in commune1 commune2 commune3 ...; do
      echo docker exec -ti ${i}teleservices_${i}teleservices_1 sudo -u  wcs-au-quotidien wcsctl -f /etc/wcs/wcs-au-quotidien.cfg runscript --vhost=${i}-formulaires.guichet-citoyen.be /opt/publik/scripts/migration-ts1/import-forms.py /opt/publik/scripts/migration-ts1/forms/
  done

- import-workflows.py

  >> sudo -u  wcs-au-quotidien wcsctl -f /etc/wcs/wcs-au-quotidien.cfg runscript --vhost=test-formulaires.guichet-citoyen.be /opt/publik/scripts/migration-ts1/import-workflows.py /opt/publik/scripts/migration-ts1/workflows/


- import-wcs-user.py
  Create a default wcs user
  >> wcsctl runscript --vhost=test-formulaires.guichet-citoyen.be import-wcs-user.py --app-dir=/var/lib/wcs-au-quotidien/

- import-authentic-user.py
  Create a default authentic user with role in generic TS instance. (automatic wcs provisioning)
  >> authentic2-multitenant-manage tenant_command runscript import-authentic-user.py -d test-auth.guichet-citoyen.be

