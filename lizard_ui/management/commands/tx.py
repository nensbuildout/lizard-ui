# -*- coding: utf-8 -*-
# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
from __future__ import print_function, unicode_literals
import sys
import logging

from django.core.management.base import BaseCommand

from txclib import utils  # txclib is from transifex-client


logger = logging.getLogger(__name__)


def main_tx_wrapper(*args, **options):
    # TODO: implement following commands
    # create_project if not exists
    # status: check if project and resource exists, if not create
    # push: push translations to server
    # pull: pull translations from server
    #
    # general workflow idea
    # pull from tx, commit (merge conflict?), make and compile messages (i18n),
    # commit and push to transifex

    # main(*args, **options)
    print("WARNING: do not use for now, work in progress")

def main(*args, **options):
    """
    Transifex wrapper, got code from tx console script from transifex-client.
    Consider also using code from python-transifex or django-transifex.

    """
    path_to_tx = utils.find_dot_tx()

    args = list(args)

    cmd = args[0]
    try:
        utils.exec_command(cmd, args[1:], path_to_tx)
    except utils.UnknownCommandError:
        logger.error("tx: Command %s not found" % cmd)
    except SystemExit:
        sys.exit()
    except:
        import traceback
        if options['traceback']:
            traceback.print_exc()
        else:
            formatted_lines = traceback.format_exc().splitlines()
            logger.error(formatted_lines[-1])
        sys.exit(1)


class Command(BaseCommand):
    args = ''
    help = 'Management command to wrap around tx (from transifex-client).'

    def handle(self, *args, **options):
        main_tx_wrapper(*args, **options)
