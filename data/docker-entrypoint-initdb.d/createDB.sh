#!/bin/sh
su postgres -c "createdb combo"
su postgres -c "createdb passerelle"
su postgres -c "createdb authentic2"
su postgres -c "createdb fargo"
su postgres -c "createdb wcs"

