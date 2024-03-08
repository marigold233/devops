docker run -d --name elastalert --restart=always -v ./elastalert.yaml:/opt/elastalert/config.yaml -v ./rules:/opt/elastalert/rules --network=host jertel/elastalert2 --verbose
