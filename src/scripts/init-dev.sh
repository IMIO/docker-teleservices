#! /bin/sh

# base things
test -L /usr/share/publik/themes/imio || mv /usr/share/publik/themes/imio /usr/share/publik/themes/imio-orig
rm -f /etc/nginx/sites-enabled/default
cp /etc/nginx/sites-available/default /etc/nginx/sites-enabled/default

# imio-publik-themes
if [ -d /opt/publik/imio-publik-themes ]
then
	ln -sf imio-orig /usr/share/publik/themes/imio
else
	ln -sf /opt/publik/imio-publik-themes /usr/share/publik/themes/imio
fi

# combo
if [ -d /opt/publik/combo ]
then
	sed -i 's/proxy_pass.*combo.*/proxy_pass http:\/\/127.0.0.1:8010;/' /etc/nginx/sites-enabled/default
fi

# passerelle
if [ -d /opt/publik/passerelle ]
then
	sed -i 's/proxy_pass.*passerelle.*/proxy_pass http:\/\/127.0.0.1:8011;/' /etc/nginx/sites-enabled/default
fi

# authentic
if [ -d /opt/publik/authentic ]
then
	sed -i 's/proxy_pass.*authentic.*/proxy_pass http:\/\/127.0.0.1:8012;/' /etc/nginx/sites-enabled/default
fi

# passerelle-imio-tax-compute
if [ -d /opt/publik/passerelle-imio-tax-compute ]
then
	(cd /opt/publik/passerelle-imio-tax-compute && python setup.py develop)
fi

# authentic2-auth-fedict
if [ -d /opt/publik/authentic2-auth-fedict ]
then
	(cd /opt/publik/authentic2-auth-fedict && python setup.py develop)
fi

service nginx reload
