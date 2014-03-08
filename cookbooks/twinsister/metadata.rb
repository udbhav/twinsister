name             'twinsister'
maintainer       'YOUR_NAME'
maintainer_email 'YOUR_EMAIL'
license          'All rights reserved'
description      'Installs/Configures twinsister'
long_description IO.read(File.join(File.dirname(__FILE__), 'README.md'))
version          '0.2.1'

depends "apt"
depends "nginx"
depends "python"
depends "postgresql"
depends "nodejs"
depends "ruby_build"
depends "rbenv"
depends "supervisor"
