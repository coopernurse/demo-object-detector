
import boto3

class Queue(object):
    def __init__(self, queue_name):
        self.queue_name = queue_name
        self.sqs = boto3.resource("sqs")
        self.q = self.sqs.create_queue(QueueName=queue_name)

    def send(self, msg):
        self.q.send_message(MessageBody=msg)

    def depth(self):
        q = self.sqs.get_queue_by_name(QueueName=self.queue_name)
        return q.attributes.get("ApproximateNumberOfMessages")
    
