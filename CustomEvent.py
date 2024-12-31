class CustomEvent:
    """Event class for subscriptions    
    """
    def __init__(self):
        self._subscribers = []

    def subscribe(self, callback):
        """Subscribe to the event

        Args:
            callback (function): function that will be called when 
            event notify is called.
        """
        self._subscribers.append(callback)

    def unsubscribe(self, callback):
        """Unsubscribe from the event calls

        Args:
            callback (function): the callback that needs to be removed from 
            the event notification
        """
        self._subscribers.remove(callback)

    def notify(self, *args, **kwargs):
        """Execute the callbacks from the subscribers
        """
        for subscriber in self._subscribers:
            subscriber(*args, **kwargs)