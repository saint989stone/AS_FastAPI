from src.repositories.hotels import HotelsRepo
from src.repositories.rooms import RoomsRepo
from src.repositories.users import UsersRepo
from src.repositories.bookings import BookingsRepo


class DBManager:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()

        self.hotels = HotelsRepo(self.session)
        self.rooms = RoomsRepo(self.session)
        self.users = UsersRepo(self.session)
        self.bookings = BookingsRepo(self.session)

        return self

    async def __aexit__(self, *args):
        await self.session.rollback()
        await self.session.close()


    async def commit(self):
        await self.session.commit()