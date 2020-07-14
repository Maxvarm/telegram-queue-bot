import datetime
from mongoengine import Document, EmbeddedDocument
from mongoengine.base.datastructures import EmbeddedDocumentList
from mongoengine.connection import connect
from mongoengine.fields import IntField, BooleanField, StringField, DateTimeField, \
    EmbeddedDocumentField, EmbeddedDocumentListField
from mongoengine.queryset import queryset_manager

from strings import REALTIME_HELLO, DEFAULT_USERNAME
from private import db_name, db_host

connect(db_name, host=db_host, port=27017)

class Config(EmbeddedDocument):
    sortby = IntField(default=0)
    reverse = BooleanField(default=False)
    priority = BooleanField(default=False)

class User(EmbeddedDocument):
    user_id = IntField(required=True)
    username = StringField(default=DEFAULT_USERNAME, max_length=50)
    fullname = StringField(required=True, max_length=50)
    add_time = DateTimeField(default=datetime.datetime.now)
    priority = IntField(default=0)
    

class Queue(Document):
    queue_id = StringField(required=True, max_length=100)
    author_id = IntField(required=True, max_length=50)
    title = StringField(required=True, max_length=100)
    publish_time = DateTimeField(default=datetime.datetime.now)
    config = EmbeddedDocumentField(Config, default=Config())
    queue = EmbeddedDocumentListField(User, default=[])

    @classmethod
    def is_prioritized(cls, queue_id):
        return cls.objects(queue_id=queue_id).only('config')[0].config.priority
    
    @classmethod
    def print_hello(cls, queue_id=None, query_name=None):
        """
        Draw greeting message
        """
        if query_name:
            return f"🔸*{query_name}*🔸" + "\n➖➖➖➖➖➖➖➖➖➖➖➖\n" + REALTIME_HELLO
        elif queue_id:
            title = cls.objects(queue_id=queue_id).only('title')[0].title
            return f"🔸*{title}*🔸" + "\n➖➖➖➖➖➖➖➖➖➖➖➖\n" + REALTIME_HELLO

    @classmethod
    def print_config(cls, queue_id):
        """
        Draw current config info
        """
        document = cls.objects(queue_id=queue_id).only('config','title')[0]
        config = document.config

        sort_options = ["By time", "By fullname", "By username", "By registration date"]
        res = f"🔸*{document.title}:Config*🔸"
        res += "\n➖➖➖➖➖➖➖➖➖➖➖➖\n"
        res += "_Sort by:_\n"
        for i, option in enumerate(sort_options):
            if i == config.sortby:
                res += f"   *💚{option}💚*"
            else:
                res += f"   *{option}*"
            res += '\n'
        res += "\n➖➖➖➖➖➖➖➖➖➖➖➖\n"
        res += "_Reverse:_" + (" *Yes*" if config.reverse else " *No*")
        res += "\n➖➖➖➖➖➖➖➖➖➖➖➖\n"
        res += "_Priority:_" + (" *Yes*\n" if config.priority else " *No*\n")
        return res
    
    @classmethod
    def print_queue(cls, queue_id):
        """
        Draw current queue state
        """
        document = cls.objects(queue_id=queue_id)[0]
        key = ""
        if document.config.sortby == 0:
            pass
        elif document.config.sortby == 1:
            key += "fullname"
        elif document.config.sortby == 2:
            key += "username"
        elif document.config.sortby == 3:
            key += "user_id"
        
        queue = document.queue

        if document.config.priority and document.config.sortby:
            queue.sort(key=lambda user: (user.priority, str(user[key]).lower()), reverse=document.config.reverse)
        elif document.config.priority and not document.config.sortby:
            queue.sort(key=lambda user: user.priority, reverse=document.config.reverse)
        elif document.config.sortby:
            queue.sort(key=lambda user: str(user[key]).lower(), reverse=document.config.reverse)
        else:
            pass
        
        document.save()
        
        res = f"🔸*{document.title}*🔸"
        res += "\n➖➖➖➖➖➖➖➖➖➖➖➖\n"
        res += "_Formed queue:_\n"
        res += '\n'.join(f"  *{i}.* {user.fullname} (@{user.username})" for i, user in enumerate(queue, 1))
        return res

    @classmethod
    def toggle_sortby(cls, queue_id):
        queue = cls.objects(queue_id=queue_id)[0]
        #Next sorting option in cycle list with 4 options
        queue.config.sortby = (queue.config.sortby + 1) % 4
        queue.save()
    
    @classmethod
    def toggle_reverse(cls, queue_id):
        queue = cls.objects(queue_id=queue_id)[0]
        queue.config.reverse = not queue.config.reverse
        queue.save()
    
    @classmethod
    def toggle_priority(cls, queue_id):
        queue = cls.objects(queue_id=queue_id)[0]
        queue.config.priority = not queue.config.priority
        queue.save()

    @classmethod
    def check_author(cls, err_msg=None):
        """
        Decorator that checks if user has right to click inline button
        """
        def decorator(f):
            def wrapper(update, context):
                query = update.callback_query
                if not Queue.objects(
                    queue_id=query.inline_message_id,
                    author_id=update.effective_user.id
                    ):
                    query.answer(err_msg)
                else:
                    return f(update, context)
                return None
            return wrapper
        return decorator

    @classmethod
    def check_queue(cls, to_remove=False, err_msg=None):
        """
        Decorator that checks user state in queue (exists or not)
        """
        def decorator(f):
            def wrapper(update, context):
                query = update.callback_query
                #Hack to handle both adding and deletion to the queue
                if to_remove != bool(Queue.objects(
                    queue_id=query.inline_message_id,
                    queue__user_id=update.effective_user.id
                    )):
                    query.answer(err_msg)
                else:
                    return f(update, context)
                return None
            return wrapper
        return decorator









