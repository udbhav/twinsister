apt_package "git"

# create directory and clone repo if it doesn't exist
unless File.directory?(node['twinsister']['app_root'])
  execute "git clone" do
    command "git clone -b #{node['twinsister']['git_branch']} #{node['twinsister']['git_repo']}"
    cwd "/home/#{node['twinsister']['user']}"
    user node['twinsister']['user']
  end
end

# disable password ssh
node.default['openssh']['server']['password_authentication'] = 'no'
include_recipe "openssh"

# copy root key to user if no ssh directory
unless File.directory?("/home/#{node['twinsister']['user']}/.ssh")
    execute "mkdir /home/#{node['twinsister']['user']}/.ssh"
    execute "cp /root/.ssh/authorized_keys /home/#{node['twinsister']['user']}/.ssh/"
    execute "chown #{node['twinsister']['user']} /home/#{node['twinsister']['user']}/.ssh/authorized_keys"
end

# firewall
include_recipe "firewall"

rules = [['ssh',22],['http',80],['ssl',443]]
rules.each do |r|
  firewall_rule r[0] do
    port r[1]
    action :allow
  end
end

firewall 'ufw'

include_recipe "twinsister::base"
