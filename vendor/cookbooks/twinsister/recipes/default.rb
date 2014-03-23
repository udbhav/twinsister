include_recipe "twinsister::base"

# on change
template "/home/#{node['twinsister']['user']}/on_change.sh" do
  source "on_change.erb"
  owner node['twinsister']['user']
  mode "774"
  variables({app_root: node['twinsister']['app_root']})
end

# temporary kishore dev stuff
# venv_root = node['twinsister']['app_root'] + '/env'
# execute "kishore_symlink" do
#   command "ln -sf /home/vagrant/kishore #{venv_root}/lib/python2.7/site-packages/kishore"
# end
