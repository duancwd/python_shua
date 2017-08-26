#
# snimpy -- Interactive SNMP tool
#
# Copyright (C) Vincent Bernat <bernat@luffy.cx>
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
#

# We are using readline module of Python. Depending on the Python
# distribution, this module may be linked to GNU Readline which is
# GPLv2 licensed.

"""Provide an interactive shell for snimpy.

The main method is C{interact()}. It will either use IPython if
available or just plain python Shell otherwise. It will also try to
use readline if available.

For IPython, there is some configuration stuff to use a special
profile. This is the recommended way to use it. It allows a separate
history.
"""

import sys
import os
import atexit
import code
from datetime import timedelta

import snimpy
from snimpy import manager
from snimpy.config import Conf


def interact(argv=sys.argv):  # pragma: no cover
    conf = Conf().load()

    banner = "\033[1mSnimpy\033[0m ({0}) -- {1}.\n".format(
        snimpy.__version__, snimpy.__doc__)
    banner += "  load        -> load an additional MIB\n"
    banner += "  M           -> manager object"

    local = {"conf": conf,
             "M": manager.Manager,
             "load": manager.load,
             "timedelta": timedelta,
             "snmp": manager.snmp
             }

    if len(argv) <= 1:
        manager.Manager._complete = True

    for ms in conf.mibs:
        manager.load(ms)

    globals().update(local)

    if len(argv) > 1:
        argv = argv[1:]
        exec(compile(open(argv[0]).read(), argv[0], 'exec')) in local
        return

    try:
        try:
            try:
                # ipython >= 1.0
                from IPython.terminal.embed import \
                    InteractiveShellEmbed
            except ImportError:
                # ipython >= 0.11
                from IPython.frontend.terminal.embed import \
                    InteractiveShellEmbed
            import IPython
            if IPython.version_info < (4,):
                from IPython.config.loader import Config
            else:
                from traitlets.config.loader import Config
            cfg = Config()
            try:
                # >= 5
                from IPython.terminal.prompts import Prompts, Token

                class SnimpyPrompt(Prompts):
                    def in_prompt_tokens(self, cli=None):
                        return [
                            (Token.Prompt, "Snimpy["),
                            (Token.PromptNum, str(self.shell.execution_count)),
                            (Token.Prompt, ']> '),
                        ]

                    def out_prompt_tokens(self):
                        return [
                            (Token.OutPrompt, "Snimpy["),
                            (Token.OutPromptNum,
                             str(self.shell.execution_count)),
                            (Token.OutPrompt, ']: '),
                        ]
            except ImportError:
                SnimpyPrompt = None
                try:
                    # >= 0.12
                    cfg.PromptManager.in_template = "Snimpy [\\#]> "
                    cfg.PromptManager.out_template = "Snimpy [\\#]: "
                except ImportError:
                    # 0.11
                    cfg.InteractiveShellEmbed.prompt_in1 = "Snimpy [\\#]> "
                    cfg.InteractiveShellEmbed.prompt_out = "Snimpy [\\#]: "
            if conf.ipythonprofile:
                cfg.InteractiveShellEmbed.profile = conf.ipythonprofile
            shell = InteractiveShellEmbed(
                config=cfg,
                banner1=banner,
                user_ns=local)
            # Not interested by traceback in this module
            shell.InteractiveTB.tb_offset += 1
            if SnimpyPrompt is not None:
                shell.prompts = SnimpyPrompt(shell)
        except ImportError:
            # ipython < 0.11
            from IPython.Shell import IPShellEmbed
            argv = ["-prompt_in1", "Snimpy [\\#]> ",
                    "-prompt_out", "Snimpy [\\#]: "]
            if conf.ipythonprofile:
                argv += ["-profile", conf.ipythonprofile]
            shell = IPShellEmbed(argv=argv,
                                 banner=banner, user_ns=local)
            # Not interested by traceback in this module
            shell.IP.InteractiveTB.tb_offset += 1
    except ImportError:
        shell = None

    if shell and conf.ipython:
        shell()
    else:
        try:
            import rlcompleter
            import readline
        except ImportError:
            readline = None
        if readline:
            if conf.histfile:
                try:
                    readline.read_history_file(
                        os.path.expanduser(conf.histfile))
                except IOError:
                    pass
                atexit.register(lambda: readline.write_history_file(
                    os.path.expanduser(conf.histfile)))

            readline.set_completer(rlcompleter.Completer(local).complete)
            readline.parse_and_bind("tab: menu-complete")
        sys.ps1 = conf.prompt
        code.interact(banner=banner, local=local)
