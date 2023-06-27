app_name=dowoco/zabbix-send-api

build:
        docker build -t $(app_name) .

run:
        docker run --detach -p 5000:5000 --name="$(app_name)" $(app_name)

kill:
        @echo 'Killing container...'
        docker stop $(app_name)
        docker rm $(app_name)
