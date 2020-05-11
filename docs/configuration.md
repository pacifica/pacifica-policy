# Configuration

The Pacifica Core services require two configuration files. The REST
API utilizes [CherryPy](https://github.com/cherrypy) and review of
their
[configuration documentation](http://docs.cherrypy.org/en/latest/config.html)
is recommended. The service configuration file is a INI formatted
file containing configuration for database connections.

## CherryPy Configuration File

An example of Policy server CherryPy configuration:

```ini
[global]
log.screen: True
log.access_file: 'access.log'
log.error_file: 'error.log'
server.socket_host: '0.0.0.0'
server.socket_port: 8181

[/]
request.dispatch: cherrypy.dispatch.MethodDispatcher()
tools.response_headers.on: True
tools.response_headers.headers: [('Content-Type', 'application/json')]
```

## Service Configuration File

The service configuration is an INI file and an example is as follows:

```ini
[policy]
; This section has policy service specific config options

; The following strings reference formatting directives {}. The
; object passed to the format method is the transaction object
; from the metadata API. The DOI is special and added into the
; transaction object for that format as well.

; Internal URL format for transactions not released or have DOIs
internal_url_format = https://internal.example.com/{_id}

; Release URL format for transactions released but no DOI
release_url_format = https://release.example.com/{_id}

; DOI URL format for transactions with a DOI
doi_url_format = https://dx.doi.org/{doi}

; In memory object cache size (used in data release)
cache_size = 10000

; This sets the admin group name
admin_group = admin

; This sets the admin group id (should match group name in metadata)
admin_group_id = 0

; This sets the admin user id (should match user name in metadata)
admin_user_id = 0

[metadata]
; This section contains configuration for metadata service

; The global metadata url
endpoint_url = http://localhost:8121

; The endpoint to check for status of metadata service
status_url = http://localhost:8121/groups

```

## Starting the Service

Starting the Policy service can be done by two methods. However,
understanding the requirements and how they apply to REST services
is important to address as well. Using the
internal CherryPy server to start the service is recommended for
Windows platforms. For Linux/Mac platforms it is recommended to
deploy the service with
[uWSGI](https://uwsgi-docs.readthedocs.io/en/latest/).

### Deployment Considerations

The Policy server can have the same memory consumption issues as the
Metadata service. Please consider those recommendations
[here](https://pacifica-metadata.readthedocs.io/en/latest/configuration.html#deployment-considerations)
similarly for the Policy service.

### CherryPy Server

To make running the Policy service using the CherryPy's builtin
server easier we have a command line entry point.

```
$ pacifica-policy --help
usage: pacifica-policy [-h] [-c CONFIG] [-p PORT] [-a ADDRESS]

Run the policy server.

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        cherrypy config file
  -p PORT, --port PORT  port to listen on
  -a ADDRESS, --address ADDRESS
                        address to listen on
$ pacifica-policy
[09/Jan/2019:09:17:26] ENGINE Listening for SIGTERM.
[09/Jan/2019:09:17:26] ENGINE Bus STARTING
[09/Jan/2019:09:17:26] ENGINE Set handler for console events.
[09/Jan/2019:09:17:26] ENGINE Started monitor thread 'Autoreloader'.
[09/Jan/2019:09:17:26] ENGINE Serving on http://0.0.0.0:8181
[09/Jan/2019:09:17:26] ENGINE Bus STARTED
```

### uWSGI Server

To make running the Policy service using uWSGI easier we have a
module to be included as part of the uWSGI configuration. uWSGI is
very configurable and can use this module many different ways. Please
consult the
[uWSGI Configuration](https://uwsgi-docs.readthedocs.io/en/latest/Configuration.html)
documentation for more complicated deployments.

```
$ pip install uwsgi
$ uwsgi --http-socket :8181 --master --module pacifica.policy.wsgi
```
