Installation
============

From the ZIP package
--------------------

1. Download ``local_newplugin-<version>.zip`` from the
   `releases page <https://github.com/{{OWNER}}/moodle-local_newplugin/releases>`_.
2. Go to *Site administration > Plugins > Install plugins* and upload the ZIP.
3. Complete the Moodle upgrade and purge the caches.

From Git
--------

.. code-block:: bash

   git clone https://github.com/{{OWNER}}/moodle-local_newplugin.git {{INSTALL_PATH}}
   php admin/cli/upgrade.php

In Moodle 5.1 or later, clone into ``public/{{INSTALL_PATH}}``.
