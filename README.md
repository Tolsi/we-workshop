# Workshop - запуск кастомной сети Waves Enterprise [![Contact](https://img.shields.io/badge/contact-telegram-9cf)](https://t.me/tolsi1)

# Что необходимо для активного участия

Вы можете послушать и посмотреть как я разворачиваю сеть и запускаю смарт-контракты, но гораздо позновательнее попробовать пройти через все шаги вместе с ведущим самому. Для этого необходимо принести с собой ноутбук с предустановленным ПО:

* JRE 8. [На текущий момент эта.](https://www.oracle.com/technetwork/java/javase/downloads/jre8-downloads-2133155.html)

WE Node - это JVM приложение, написанное на Scala, поэтому её надо запускать с помощью Java Runtime Engine.

* Последняя версия Docker Engine. [На текущий момент эта.](https://docs.docker.com/v17.09/engine/installation/).

DE нужен чтобы запускать мощные и гибкие смарт-контракты, написанные на любом языке.

* Доступ между машинами внутри сети.

Без этого не получится взаимодействовать в рамках одной, похожей на настоящую, блокчейн сети. Каждому придется делать свою изолированную и проходить шаги в ней.

# Что надо будет делать

1. Создать аккаунт

Если вы в одной сети, то сделайте общий чат и скопируйте адрес и публичный ключ в него. Ведущий добавит вам токены и даст необходимые права в genesis блоке.

`java -jar generators-WE0.95.jar AccountsGeneratorApp account-generator.conf`

2. Подписать genesis

Если вы в общей сети, то этот шаг выполняет один раз ведущий. Если нет общей сети, то каждый запускает свою изолированную сеть (повторяет это действие). Надо зайти в `node.conf` и изменить в разделе `vostok.blockchain.custom.genesis` массивы `transactions` и `network-participants` по желанию. В `genesis-public-key-base-58` лидер должен вписать свой публичный ключ (он будет подписывать genesis блок).

`java -jar generators-WE0.95.jar GenesisBlockGenerator node.conf`

Затем лидер должен поделиться с этим конфигом со всеми участниками через общий чат (все настройки genesis блока в рамках одной сети должны быть одинаковыми). Если вы в одной сети, то можете добавить IP адреса в виде `"ip:port"` в массив `vostok.network.known-peers`, чтобы приложения знало, с кем ему соединиться.

3. Запустить ноду

Очень просто.

`java -jar node-WE0.95.jar node.conf`

Посмотрите в логи на наличие ошибок, процесс должен продолжить работать и весело сыпать события в лог.

4. Установить docker registry

Этот шаг выполняет один раз ведущий. Если нет общей сети, то каждый запускает свой локальный docker registry.

`docker run -p 5000:5000 --name registry registry:2`

Если появилась ошибка `Conflict. The container name "/registry" is already in use by container "7e53ae0461d09178bacc04083b5e3639374e53c45751c42aebd718852be283c0"...`, то возможно у вас уже есть созданный контейнер с registry, просто запустите его с помощью `docker start 7e53...`.

4.5. Docker insecure

Для тестового окружения мы выключаем требование HTTPS в Docker Engine от Docker репозитория. Сделать это вам помогут это инструкции:

Для Ubuntu:

https://docs.docker.com/registry/insecure/

https://askubuntu.com/questions/477551/how-can-i-use-docker-without-sudo

Для Mac OS X

https://stackoverflow.com/a/39492340/699934

Для Windows:

https://docs.docker.com/registry/insecure/

5. Собрать контракт и задеплоить

Если вы в одной сети, то замените IP адрес 127.0.0.1 на IP адрес лидера. Также вам потребуется утилиты curl и jq, если их нет, то можете сами сделать запрос и найти значение `config.digest` в возвращаемом json. Этот хеш (без `sha256:`) пригодится нам для создания контракта. Он нужен для защиты от возможной подмены контакта в репозитории.

```
docker build -t $(basename "$PWD") .
docker image tag $(basename "$PWD") 127.0.0.1:5000/$(basename "$PWD")
docker push 127.0.0.1:5000/$(basename "$PWD")
curl --silent --header "Accept: application/vnd.docker.distribution.manifest.v2+json" "http://127.0.0.1:5000/v2/$(basename "$PWD")/manifests/latest" | jq -r '.config.digest'
```

6. Создать и вызвать контракт в блокчейне

Если вы в одной сети, то замените IP адрес 127.0.0.1 на IP адрес лидера.

Вы можете попасть на панель нужного метода запустив ноду и перейдя по ссылке: http://localhost:6862/api-docs/index.html#!/transactions/signAndBroadcast_1 .

Под `POST /transactions/signAndBroadcast` вы можете копировать и изменять под себя шаблон транзакций создания и вызова контрактов ниже.

## Создание 

Замените `sender` на ваш адрес, `image` на путь вашего контракта, а `imageHash` на хеш из предыдущего шага.

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

Замените `sender` на ваш адрес, а `contractId` на ID транзакции, созданной выше - это и есть ID созданного смарт-контракта.  

```
{
"sender": "3MwLtQz26bEpxTxMq6Rh1htAYFE6VeqL9oV",
"contractId": "4fQaiaqn73FrN43Dyn7pJX5kvfuBzNEQwEnAK3BsP9YW",
"params": [],
"fee": 0,
"type": 104
}
```

# Документация

https://docs.wavesenterprise.com/
