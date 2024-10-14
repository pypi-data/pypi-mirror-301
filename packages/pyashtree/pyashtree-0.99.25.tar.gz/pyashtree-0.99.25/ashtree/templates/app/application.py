from ashtree.baseapp import BaseApp
from app.middleware import SessionMiddleware
from app.context import ctx


class Application(BaseApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        _ = ctx.db

    def setup_routes(self) -> None:
        from .controllers.api.v1.account import account_ctrl
        self.include_router(account_ctrl)

    def setup_middleware(self) -> None:
        super()
        self.add_middleware(SessionMiddleware)
