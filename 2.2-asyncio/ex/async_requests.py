import asyncio
import datetime

import aiohttp
from more_itertools import chunked

from models import Session, SwapiPeople, close_orm, init_orm

MAX_REQUESTS = 5


async def get_people(person_id: int, session: aiohttp.ClientSession):
    response = await session.get(f"https://swapi.py4e.com/api/people/{person_id}/")
    json_data = await response.json()
    return json_data


async def insert_people(people_list: list[dict]):
    async with Session() as session:
        orm_objs = [SwapiPeople(json=item) for item in people_list]
        session.add_all(orm_objs)
        await session.commit()


async def main():
    await init_orm()
    async with aiohttp.ClientSession() as session:

        for id_chunk in chunked(range(1, 101), MAX_REQUESTS):
            coros = [get_people(i, session) for i in id_chunk]
            result = await asyncio.gather(*coros)
            insert_coro = insert_people(result)
            task = asyncio.create_task(insert_coro)

        tasks = asyncio.all_tasks()
        current_task = asyncio.current_task()
        tasks.remove(current_task)
        await asyncio.gather(*tasks)

    await close_orm()


start = datetime.datetime.now()
asyncio.run(main())
print(datetime.datetime.now() - start)
