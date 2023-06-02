import random
from fabric.contrib.files import append, exists
from fabric.api import cd, env, local, run

REPO_URL = 'git@github.com:martinm43/get_goated.git'  
env.user = "m2"

#Author's Note
#paramiko and fabric have broken ssh key handling
#this issue is not fixed as of 1.14 fabric3.
#safe fix is to enable password login BUT restrict it to safe IPs
#the "theoretical" fix of using a specialized key without passphrase for 
#fabric is included here for posterity. 
#env.key_filename = "/Users/martin/.ssh/id_rsa_fabric"


def deploy():
    site_folder = f'/home/{env.user}/sites/{env.host}'  
    run(f'mkdir -p {site_folder}')  
    with cd(site_folder):  
        _get_latest_source()
        #_update_virtualenv()
        _create_or_update_dotenv()
        _update_static_files()
        _update_database()


def _get_latest_source():
    if exists('.git'):  
        run('git fetch')  
    else:
        run(f'git clone {REPO_URL} .')  
    current_commit = local("git log -n 1 --format=%H", capture=True)  
    run(f'git reset --hard {current_commit}') 

"""
def _update_virtualenv():
    if not exists('virtualenv/bin/pip'):  
        run(f'python3.7 -m venv virtualenv')
    run('./virtualenv/bin/pip install -r requirements.txt') 
"""

def _create_or_update_dotenv():
    append('.env', 'DJANGO_DEBUG_FALSE=y')  
    append('.env', f'SITENAME={env.host}')
    current_contents = run('cat .env')  
    if 'DJANGO_SECRET_KEY' not in current_contents:  
        new_secret = ''.join(random.SystemRandom().choices(  
            'abcdefghijklmnopqrstuvwxyz0123456789', k=50
        ))
        append('.env', f'DJANGO_SECRET_KEY={new_secret}')


def _update_static_files():
    run(f'/home/{env.user}/miniconda3/envs/goated_env/bin/python manage.py collectstatic --noinput')

def _update_database():
    run(f'/home/{env.user}/miniconda3/envs/goated_env/bin/python manage.py migrate --noinput') 

