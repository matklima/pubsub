# pubsub
Requiremenst:

python3

usage:

run server.py: `python3 server.py`

run client.py: `python3 client.py`

after running client.py you will get prompt to input next action. Possible actions are: connect, subscribe, publish, disconnect, unsubscribe

after inpuntting `connect` you will automatically be connected to server on port 5050 (this can be improved to use other server/port)

option `publish` will ask you to input topic name to publish to and after that message you want to publish.

option `subscribe` will ask you topic you want to subscribe to.

option `unsubscribe` will ask you name of the topic you want to unsubscribe from

option `disconnect` will disconnect client from server.

TODO:

* improve server-client connections (add option to choose server and port - hardcoded now(works for localhost only))
* improve error handling
* after client disconnect find all his topics, remove client from dictionary, remove all his topics from subscribed clients subscription dictionary
