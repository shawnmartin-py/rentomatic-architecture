import sqlalchemy as sql
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker

from rentomatic.domain.room import Room as DomainRoom
from rentomatic.repository.postgres_objects import Base, Room as RepositoryRoom


class PostgresRepo:
    def __init__(self, configuration: dict):
        connection_url = URL.create(
            drivername="postgresql+psycopg2",
            username=configuration["POSTGRES_USER"],
            password=configuration["POSTGRES_PASSWORD"],
            host=configuration["POSTGRES_HOSTNAME"],
            port=configuration["POSTGRES_PORT"],
            database=configuration["APPLICATION_DB"],
        )
        self.engine = sql.create_engine(connection_url)
        Base.metadata.create_all(self.engine)
        Base.metadata.bind = self.engine

    def _create_room_objects(
        self, results: list[RepositoryRoom]
    ) -> list[DomainRoom]:
        return [
            DomainRoom(
                code=q.code,
                size=q.size,
                price=q.price,
                latitude=q.latitude,
                longitude=q.longitude,
            )
            for q in results
        ]

    def list(self, filters: dict | None = None) -> list[DomainRoom]:
        DBSession = sessionmaker(bind=self.engine)
        session = DBSession()

        query = session.query(RepositoryRoom)

        if filters is None:
            return self._create_room_objects(query.all())

        if "code__eq" in filters:
            query = query.filter(RepositoryRoom.code == filters["code__eq"])

        if "price__eq" in filters:
            query = query.filter(RepositoryRoom.price == filters["price__eq"])

        if "price__lt" in filters:
            query = query.filter(RepositoryRoom.price < filters["price__lt"])

        if "price__gt" in filters:
            query = query.filter(RepositoryRoom.price > filters["price__gt"])

        return self._create_room_objects(query.all())
