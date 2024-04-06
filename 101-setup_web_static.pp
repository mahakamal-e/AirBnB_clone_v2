# Define a Puppet class for setting up web_static
class setup_web_static {
    package { 'nginx':
        ensure => installed,
    }

    file { '/data':
        ensure => directory,
    }

    file { '/data/web_static':
        ensure => directory,
    }

    file { '/data/web_static/releases':
        ensure => directory,
    }

    file { '/data/web_static/shared':
        ensure => directory,
    }

    file { '/data/web_static/releases/test':
        ensure => directory,
    }

    file { '/data/web_static/releases/test/index.html':
        ensure  => file,
        content => '<html><head></head><body>Holberton School</body></html>',
    }

    file { '/data/web_static/current':
        ensure => link,
        target => '/data/web_static/releases/test',
        force  => true,
    }

    file { '/data':
        owner   => 'ubuntu',
        group   => 'ubuntu',
        recurse => true,
    }

    file { '/etc/nginx/sites-available/default':
        ensure  => file,
        content => "server {
            listen 80 default_server;
            listen [::]:80 default_server;

            root /data/web_static/current;

            location /hbnb_static {
                alias /data/web_static/current/;
            }
        }",
    }

    service { 'nginx':
        ensure => running,
        enable => true,
        require => File['/etc/nginx/sites-available/default'],
    }
}

include setup_web_static
