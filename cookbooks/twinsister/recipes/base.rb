include_recipe "apt"
include_recipe "nginx"
include_recipe "python"
include_recipe "postgresql::server"
include_recipe "nodejs::install_from_package"
include_recipe "supervisor"

venv_root = node['twinsister']['app_root'] + '/env'
venv_pip = venv_root + '/bin/pip'

# virtualenv
python_virtualenv venv_root do
  action :create
  owner node['twinsister']['user']
end

# pillow requirements
%w(libjpeg-dev libfreetype6 libfreetype6-dev zlib1g-dev).each do |pkg|
  package pkg do
    action :install
  end
end

# python requirements
execute venv_pip + " install Pillow"
execute venv_pip + " install -r " + node['twinsister']['app_root'] + '/requirements.txt'

# less
execute "npm install -g less"
