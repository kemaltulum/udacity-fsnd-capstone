#!/bin/sh
export AUTH0_DOMAIN="fsnd-kml.auth0.com"
export ALGORITHMS="RS256"
export API_AUDIENCE="capstone"

export DATABASE_URL="postgres:///capstone"
export FLASK_APP=flaskr
export FLASK_DEBUG=True
export FLASK_ENVIRONMENT=debug