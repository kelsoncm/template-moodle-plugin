Instalação
==========

Pelo pacote ZIP
---------------

1. Baixe o ``local_newplugin-<versão>.zip`` na
   `página de releases <https://github.com/{{OWNER}}/moodle-local_newplugin/releases>`_.
2. Acesse *Administração do site > Plugins > Instalar plugins* e envie o ZIP.
3. Conclua o upgrade do Moodle e limpe os caches.

Pelo Git
--------

.. code-block:: bash

   git clone https://github.com/{{OWNER}}/moodle-local_newplugin.git {{INSTALL_PATH}}
   php admin/cli/upgrade.php

No Moodle 5.1 ou posterior, clone em ``public/{{INSTALL_PATH}}``.
