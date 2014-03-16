execute "git pull" do
  command "git pull origin #{node['twinsister']['git_branch']}"
  cwd node['twinsister']['app_root']
end

# python requirements
execute "python_requirements" do
  command "env/bin/pip install -r requirements.txt"
  cwd node['twinsister']['app_root']
end

# syncdb and migrations
execute "syncdb" do
  command "env/bin/python src/manage.py syncdb --noinput"
  cwd node['twinsister']['app_root']
end

execute "migrate" do
  command "env/bin/python src/manage.py migrate"
  cwd node['twinsister']['app_root']
end

# collectstatic
execute "collectstatic" do
  command "env/bin/python src/manage.py collectstatic --noinput"
  cwd node['twinsister']['app_root']
  user node['twinsister']['user']
end

# restart gunicorn
execute "supervisorctl restart gunicorn"

# flush memcached
execute "echo 'flush_all' | nc localhost 11211"
