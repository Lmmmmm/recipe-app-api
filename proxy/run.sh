#!/bin/sh

set -e

envsubst < /etc/nginx/default.conf.tpl > /etc/nginx/conf.d/default.conf
nginx -g 'daemon off;'


# # the script will exit immediately if it encounters any errors.
# set -e

# # Read the /etc/nginx/default.conf.tpl file
# # and replace the environment variables there with their actual values,
# # then save the replacements to /etc/nginx/conf.d/default.conf.
# envsubst < /etc/nginx/default.conf.tpl > /etc/nginx/conf.d/default.conf

# # Make Nginx run in foreground mode instead of the default daemon (background) mode.
# nginx -g 'daemon off;'