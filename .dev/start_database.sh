#!/bin/sh


podman run  --network=host -e POSTGRES_PASSWORD=changeme -e POSTGRES_DB=dev -v ./volumes/db:/var/lib/postgresql/data postgres
