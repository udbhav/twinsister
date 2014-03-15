apt_package "git"

# create directory and clone repo if it doesn't exist
unless File.directory?(node['twinsister']['app_root'])
  execute "git clone" do
    command "git clone -b #{node['twinsister']['git_branch']} #{node['twinsister']['git_repo']}"
    cwd "/home/#{node['twinsister']['user']}"
    user node['twinsister']['user']
  end
end

include_recipe "twinsister::base"
