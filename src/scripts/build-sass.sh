#! /bin/sh

test -d /opt/publik/imio-publik-themes || exit 0

cd /opt/publik/imio-publik-themes
# sass -w doesn't work on wheezy (it needs ruby-listen)
while /bin/true
do
	sass \
		static/liege/style.scss:static/liege/style.css \
		static/namur/style.scss:static/namur/style.css \
		static/lalouviere/style.scss:static/lalouviere/style.css
	sleep 5
done
