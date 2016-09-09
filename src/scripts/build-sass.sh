#! /bin/sh

test -d /opt/publik/imio-publik-themes || exit 0

cd /opt/publik/imio-publik-themes
# sass -w doesn't work on wheezy (it needs ruby-listen)
while /bin/true
do
	sass \
		static/test/style.scss:static/test/style.css \
		static/liege/style.scss:static/liege/style.css \
		static/namur/style.scss:static/namur/style.css \
		static/lalouviere/style.scss:static/lalouviere/style.css \
		static/huy/style.scss:static/huy/style.css
	sleep 5
done
