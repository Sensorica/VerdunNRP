export WORKON_HOME=~/Envs
source ~/bin/virtualenvwrapper.sh
workon verdun
export PYTHONPATH=~/webapps/verdunnrp/VerdunNRP:~/lib/python2.7:~/webapps/verdunnrp/lib/python2.7:$PYTHONPATH
export DJANGO_SETTINGS_MODULE='valuenetwork.settings'
