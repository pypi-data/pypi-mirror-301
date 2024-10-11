
import json

from google.cloud import pubsub_v1

from airless.core.hook import QueueHook
from airless.core.utils import get_config


class GooglePubsubHook(QueueHook):

    def __init__(self):
        super().__init__()
        self.publisher = pubsub_v1.PublisherClient()

    def publish(self, project, topic, data):

        if get_config('ENV') == 'prod':
            topic_path = self.publisher.topic_path(project, topic)

            message_bytes = json \
                .dumps(data) \
                .encode('utf-8')

            publish_future = self.publisher.publish(topic_path, data=message_bytes)
            publish_future.result(timeout=10)
            self.logger.info(f'published to {project}.{topic}')
            return 'Message published.'
        else:
            self.logger.debug(f'[DEV] Message published to Project {project}, Topic {topic}: {data}')
