import os
import IPython
from ashtree.command import Command
from app.context import ctx


class Shell(Command):

    NAME = "shell"
    HELP = "run project-aware python shell"
    ASYNC_RUN = False

    def run_sync(self):
        _ = ctx.db  # initialise the database
        
        rcfile = ".shellrc.py"
        if not os.path.isfile(rcfile):
            rcfile = os.path.join(ctx.project_dir, ".shellrc.py")

        if os.path.isfile(rcfile):
            with open(rcfile) as rcf:
                try:
                    exec(rcf.read())
                except Exception:
                    from traceback import print_exc

                    print("Error running .shellrc.py script!")
                    print_exc()

        IPython.embed(using='asyncio', colors="neutral")
