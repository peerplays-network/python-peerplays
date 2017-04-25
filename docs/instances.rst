Instances
~~~~~~~~~

Default instance to be used when no ``peerplays_instance`` is given to
the Objects!

.. code-block:: python

   from peerplays.instance import shared_peerplays_instance

   account = Account("xeroc")
   # is equivalent with 
   account = Account("xeroc", peerplays_instance=shared_peerplays_instance())

.. automethod:: peerplays.instance.shared_peerplays_instance
.. automethod:: peerplays.instance.set_shared_peerplays_instance
