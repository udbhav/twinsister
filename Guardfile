# A sample Guardfile
# More info at https://github.com/guard/guard#readme

# Add files and commands to this file, like the example:
#   watch(%r{file/path}) { `command(s)` }
#
guard :shell do
  watch /.*\.py/ do |m|
    `sudo supervisorctl restart gunicorn`
  end

  watch /static\/.*/ do
    `/home/vagrant/env/bin/python /vagrant/src/manage.py collectstatic --noinput`
  end
end
