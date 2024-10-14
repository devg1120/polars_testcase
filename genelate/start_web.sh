# markdown-server
# https://pypi.org/project/markdown-server/
#
#markdownserver

# python-md-to-html-server
# https://github.com/treatmesubj/python-md-to-html-server
#/
#python -m httpmdhtml.server -b 127.0.0.1 -d . --css_file ./github.css -l 8000
#python -m httpmdhtml.server -b 127.0.0.1 -d . --css_file ./mymd.css -l 8000
#python -m httpmdhtml.server -b 127.0.0.1 -d .  -l 8000

#python ./server/python-md-to-html-server/httpmdhtml/server.py \
#	-b 127.0.0.1 -d . -l 8000

	#--css_file ./css/markdown-css-themes/markdown4.css    \
	#--css_file ./css/markdown-css-themes/markdown6.css    \
	#--css_file ./css/markdown-css-themes/markdown7.css    \
	#--css_file ./css/markdown-css-themes/markdown9.css    \
	#--css_file ./css/markdown-css-themes/markdown10.css    \
	#--css_file ./css/github-markdown-css/github-markdown-light.css   \
	#--css_file ./css/github-markdown-css/github-markdown-dark.css   \

python ./server/python-md-to-html-server/httpmdhtml/server.py \
	--css_file ./css/github-markdown-css/github-markdown-light.css   \
	-b 127.0.0.1 \
	-d . \
	-l 8000
