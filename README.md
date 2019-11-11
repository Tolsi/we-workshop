# Workshop - запуск кастомной сети Waves Enterprise

1. Создать аккаунт

`java -jar generators-WE0.95.jar AccountsGeneratorApp account-generator.conf`

2. Подписать genesis

`java -jar generators-WE0.95.jar GenesisBlockGenerator node.conf`

3. Запустить ноду

`java -jar node-WE0.95.jar node.conf`

4. Установить docker registry

`docker run -p 5000:5000 --name registry registry:2`

5. Собрать контракт и задеплоить

```
docker build -t $(basename "$PWD") .
docker image tag $(basename "$PWD") 127.0.0.1:5000/$(basename "$PWD")
docker push 127.0.0.1:5000/$(basename "$PWD")
curl --silent --header "Accept: application/vnd.docker.distribution.manifest.v2+json" "http://127.0.0.1:5000/v2/$(basename "$PWD")/manifests/latest" | jq -r '.config.digest'
```

6. Создать и вызвать контракт в блокчейне

http://localhost:6862/

`POST /transactions/signAndBroadcast`

## Создание 

```
{
"sender": "3MwLtQz26bEpxTxMq6Rh1htAYFE6VeqL9oV",
"image": "127.0.0.1:5000/stateful-increment-contract",
"imageHash": "05cf9072db28f13fe8fb05e2b4d5358df92fc404f6bc6aec5899da6d815ddabe",
"params": [],
"fee": 0,
"type": 103,
"contractName": "test"
}
```

## Вызов

```
{
"sender": "3MwLtQz26bEpxTxMq6Rh1htAYFE6VeqL9oV",
"contractId": "4fQaiaqn73FrN43Dyn7pJX5kvfuBzNEQwEnAK3BsP9YW",
"params": [],
"fee": 0,
"type": 104
}
```

# Docker insecure

Для тестового окружения мы выключаем требование HTTPS от Docker репозитория:

## Ubuntu

https://docs.docker.com/registry/insecure/

https://askubuntu.com/questions/477551/how-can-i-use-docker-without-sudo

## Mac OS X

https://stackoverflow.com/a/39492340/699934

## Windows

https://docs.docker.com/registry/insecure/
