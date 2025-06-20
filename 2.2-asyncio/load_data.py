import asyncio
import datetime
from aiohttp import ClientSession
from more_itertools import chunked

from models import Session, SwapiPeople, init_orm, close_orm

MAX_REQUESTS = 5
MAX_IDS = 100

API_URL = "https://swapi.py4e.com/api/people/{}"

async def fetch_person(person_id: int, session: ClientSession):
    async with session.get(API_URL.format(person_id)) as resp:
        if resp.status == 200:
            data = await resp.json()
            name = data.get("name")
            if name:
                print(f"Fetched  person {person_id}: {name}")
            else:
                print(f"Fetched person {person_id}: No name")
            return data
        else:
            print(f"Failed to fetch person {person_id}: HTTP {resp.status}")
            return None

async def fetch_and_save(ids: list[int], session: ClientSession):
    results = await asyncio.gather(*(fetch_person(i, session) for i in ids))
    people = [
        SwapiPeople(
            name=r.get("name"),
            height=r.get("height"),
            mass=r.get("mass"),
            hair_color=r.get("hair_color"),
            skin_color=r.get("skin_color"),
            eye_color=r.get("eye_color"),
            birth_year=r.get("birth_year"),
            gender=r.get("gender"),
        )
        for r in results if r
    ]

    async with Session() as db:
        db.add_all(people)
        await db.commit()

async def main():
    await init_orm()

    async with ClientSession() as session:
        for chunk in chunked(range(1, MAX_IDS + 1), MAX_REQUESTS):
            await fetch_and_save(chunk, session)

    await close_orm()

if __name__ == "__main__":
    start = datetime.datetime.now()
    asyncio.run(main())
    print(datetime.datetime.now() - start)