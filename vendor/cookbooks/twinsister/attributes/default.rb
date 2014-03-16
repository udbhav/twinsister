default['twinsister']['user'] = 'udbhav'
default['twinsister']['app_root'] = "/home/#{node['twinsister']['user']}/twinsister"
default['twinsister']['git_repo'] = "https://github.com/udbhav/twinsister.git"
default['twinsister']['git_branch'] = "kishore"
default['twinsister']['db'] = {
  user: 'twinsister',
  name: 'twinsister',
  password: 'changethisdummy'}
