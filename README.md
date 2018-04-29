You can run Flask's local server by executing the manager script:
`./manage.py runserver`

For safety's sake, this defaults to a production config with DEBUG turned off.
You can change the config by setting the LOCATIONS_API_CONFIG
environment variable to "development" in your shell:
`export LOCATIONS_API_CONFIG=development`

[Generator Homepage](https://github.com/ColeKettler/generator-flask-api)
