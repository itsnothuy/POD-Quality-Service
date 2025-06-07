# # import asyncio, pytest
# # from fastapi.testclient import TestClient
# # from sqlmodel import SQLModel
# # from sqlalchemy.ext.asyncio import create_async_engine
# # from sqlalchemy.orm import sessionmaker
# # from sqlmodel.ext.asyncio.session import AsyncSession

# # from app.main import create_app
# # from app.db.models import Delivery
# # from app.db.session import get_session as real_get_session, init_db as real_init_db
# # from app.storage.minio import init_bucket_blocking as real_init_bucket

# # TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
# # test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)
# # TestAsyncSession = sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)

# # @pytest.fixture(autouse=True)
# # def override_db(monkeypatch):
# #     async def noop_init_db(): pass
# #     def noop_init_bucket(): pass

# #     monkeypatch.setattr("app.db.session.init_db", noop_init_db)
# #     monkeypatch.setattr("app.storage.minio.init_bucket_blocking", noop_init_bucket)

# #     async def get_test_session():
# #         async with TestAsyncSession() as s:
# #             yield s

# #     from app import app as _dummy
# #     _dummy.dependency_overrides[real_get_session] = get_test_session

# #     async def seed():
# #         async with test_engine.begin() as conn:
# #             await conn.run_sync(SQLModel.metadata.create_all)
# #         async with TestAsyncSession() as s:
# #             rec = Delivery(
# #                 id="test123",
# #                 img_url="http://localhost:9000/pod-images/test.jpg",
# #                 blurry=False, underlit=False,
# #                 blur_var=123.4, mean=200.0,
# #             )
# #             s.add(rec)
# #             await s.commit()
# #     asyncio.run(seed())
# #     yield
# #     async def drop_all():
# #         async with test_engine.begin() as conn:
# #             await conn.run_sync(SQLModel.metadata.drop_all)
# #     asyncio.run(drop_all())
# #     _dummy.dependency_overrides.pop(real_get_session, None)

# # @pytest.fixture
# # def client():
# #     app = create_app()
# #     return TestClient(app)

# # def test_get_delivery_found(client):
# #     r = client.get("/deliveries/v1/test123")
# #     assert r.status_code == 200
# #     body = r.json()
# #     assert body["id"] == "test123"
# #     assert not body["blurry"] and not body["underlit"]

# # def test_get_delivery_not_found(client):
# #     r = client.get("/deliveries/v1/notthere")
# #     assert r.status_code == 404

# # tests/test_get_delivery.py
# import asyncio
# import pytest

# from fastapi.testclient import TestClient
# from sqlmodel import SQLModel
# from sqlalchemy.ext.asyncio import create_async_engine
# from sqlalchemy.orm import sessionmaker
# from sqlmodel.ext.asyncio.session import AsyncSession

# from app.main import create_app
# from app.db.models import Delivery
# from app.db.session import get_session as real_get_session, init_db as real_init_db
# from app.storage.minio import init_bucket_blocking as real_init_bucket

# # 1) In-memory Async SQLite URL + engine + session factory
# TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
# test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)
# TestAsyncSession = sessionmaker(
#     bind=test_engine,
#     class_=AsyncSession,
#     expire_on_commit=False,
# )


# @pytest.fixture(autouse=True)
# def override_dependencies_and_prepare_db(monkeypatch):
#     """
#     - No-op out real init_db() and MinIO bucket-init at startup
#     - Patch get_session() → our in-memory SQLite sessions
#     - Create all tables & seed one Delivery(id="test123")
#     - Tear down (drop tables) after each test
#     """
#     # a) No-ops for startup hooks
#     async def noop_init_db():
#         return

#     def noop_init_bucket():
#         return

#     monkeypatch.setattr("app.db.session.init_db", noop_init_db)
#     monkeypatch.setattr("app.storage.minio.init_bucket_blocking", noop_init_bucket)

#     # b) Patch the dependency FastAPI uses: get_session → TestAsyncSession
#     async def get_test_session():
#         async with TestAsyncSession() as session:
#             yield session

#     monkeypatch.setattr("app.db.session.get_session", get_test_session)

#     # c) Create tables & insert dummy record
#     async def _init_and_seed():
#         async with test_engine.begin() as conn:
#             await conn.run_sync(SQLModel.metadata.create_all)
#         async with TestAsyncSession() as session:
#             session.add(
#                 Delivery(
#                     id="test123",
#                     img_url="http://localhost:9000/pod-images/test.jpg",
#                     blurry=False,
#                     underlit=False,
#                     blur_var=123.4,
#                     mean=200.0,
#                 )
#             )
#             await session.commit()

#     asyncio.run(_init_and_seed())
#     yield

#     # d) Tear down: drop all tables
#     async def _drop_all():
#         async with test_engine.begin() as conn:
#             await conn.run_sync(SQLModel.metadata.drop_all)

#     asyncio.run(_drop_all())

#     # e) Restore real hooks & dependency
#     monkeypatch.setattr("app.db.session.init_db", real_init_db)
#     monkeypatch.setattr("app.storage.minio.init_bucket_blocking", real_init_bucket)
#     monkeypatch.setattr("app.db.session.get_session", real_get_session)


# @pytest.fixture
# def client():
#     """
#     Build a fresh app **after** the above monkeypatch, so that
#     startup uses our patched init_db/get_session.
#     """
#     app = create_app()
#     with TestClient(app) as tc:
#         yield tc


# def test_get_delivery_found(client):
#     """
#     GET /deliveries/v1/test123 should return our seeded record.
#     """
#     r = client.get("/deliveries/v1/test123")
#     assert r.status_code == 200

#     payload = r.json()
#     assert payload["id"] == "test123"
#     assert payload["img_url"].endswith("test.jpg")
#     assert payload["blurry"] is False
#     assert payload["underlit"] is False


# def test_get_delivery_not_found(client):
#     """
#     GET /deliveries/v1/notthere should 404.
#     """
#     r = client.get("/deliveries/v1/notthere")
#     assert r.status_code == 404


# tests/test_get_delivery.py
import asyncio
import pytest

from fastapi.testclient import TestClient
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

from app import create_app
from app.db.models import Delivery
from app.db.session import get_session as real_get_session, init_db as real_init_db
from app.storage.minio import init_bucket_blocking as real_init_bucket

# Use an in-memory SQLite for these tests
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestAsyncSession = sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

@pytest.fixture(autouse=True)
def override_dependencies_and_prepare_db(monkeypatch):
    """
    - No-op real init_db() and MinIO bucket-init at startup
    - Patch get_session() → our in-memory SQLite sessions
    - Create all tables & seed one Delivery(id="test123")
    - Tear down after each test
    """
    # 1) No-ops for startup hooks
    async def noop_init_db():
        return

    def noop_init_bucket():
        return

    monkeypatch.setattr("app.db.session.init_db", noop_init_db)
    monkeypatch.setattr("app.storage.minio.init_bucket_blocking", noop_init_bucket)

    # 2) Override get_session dependency
    async def get_test_session():
        async with TestAsyncSession() as session:
            yield session

    monkeypatch.setattr("app.db.session.get_session", get_test_session)

    # 3) Create tables & seed
    async def _init_and_seed():
        async with test_engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
        async with TestAsyncSession() as session:
            session.add(
                Delivery(
                    id="test123",
                    img_url="http://localhost:9000/pod-images/test.jpg",
                    blurry=False,
                    underlit=False,
                    blur_var=123.4,
                    mean=200.0,
                )
            )
            await session.commit()

    asyncio.run(_init_and_seed())
    yield

    # 4) Tear down
    async def _drop_all():
        async with test_engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.drop_all)

    asyncio.run(_drop_all())

    # 5) Restore real hooks & dependency
    monkeypatch.setattr("app.db.session.init_db", real_init_db)
    monkeypatch.setattr("app.storage.minio.init_bucket_blocking", real_init_bucket)
    monkeypatch.setattr("app.db.session.get_session", real_get_session)

@pytest.fixture
def client():
    """
    Create a fresh TestClient after overriding dependencies.
    """
    application = create_app()
    with TestClient(application) as tc:
        yield tc


def test_get_delivery_not_found(client):
    """
    GET /deliveries/v1/notthere should 404.
    """
    r = client.get("/deliveries/v1/notthere")
    assert r.status_code == 404
