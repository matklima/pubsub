# pubsub
Requirements:

python3

usage:

run server.py: `python3 server.py`

after running server you have to enter port where you want to cumunicate with clients

run client.py: `python3 client.py`

after running client.py you will get prompt to input next action. Possible actions are: connect, subscribe, publish, disconnect, unsubscribe

after inputting `connect` you ill be prompetd to enter server address and right after that port which you want to communicate on 

option `publish` will ask you to input topic name to publish to and after that message you want to publish.

option `subscribe` will ask you topic you want to subscribe to.

option `unsubscribe` will ask you name of the topic you want to unsubscribe from

option `disconnect` will disconnect client from server.

TODO:

* improve error handling
