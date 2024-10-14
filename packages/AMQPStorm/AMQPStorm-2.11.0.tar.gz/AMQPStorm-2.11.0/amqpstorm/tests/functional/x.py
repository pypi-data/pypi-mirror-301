from amqpstorm import AMQPChannelError
from amqpstorm import AMQPConnectionError
from amqpstorm import Connection
from amqpstorm.tests import HOST
from amqpstorm.tests import PASSWORD
from amqpstorm.tests import USERNAME

import logging

logging.basicConfig(level=logging.DEBUG)

connection = Connection(
    HOST, USERNAME, PASSWORD
)
channel = connection.channel()
channel.confirm_deliveries()
channel.queue.declare('self.queue_name')
try:
    channel.basic.publish(
        body='message',
        routing_key='self.queue_name',
    )
except (AMQPConnectionError, AMQPChannelError):
    pass

while True:
    x = channel.basic.get('self.queue_name')
    if not x:
        continue

channel.close()
connection.close()