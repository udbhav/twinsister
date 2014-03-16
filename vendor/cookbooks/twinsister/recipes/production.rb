# normal provisioning
include_recipe "twinsister::base"

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

# db user password
execute "change db user pw" do
  command "psql -c \"ALTER USER #{node['twinsister']['db']['user']} WITH PASSWORD '#{node['twinsister']['db']['password']}'\""
  user 'postgres'
end

include_recipe "twinsister::deploy"
