import json
from aiohttp import web
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from models import Ad, Session, init_orm, close_orm
from schema import AdCreateSchema

app = web.Application()


@web.middleware
async def session_middleware(request: web.Request, handler):
    async with Session() as session:
        request.session = session
        response = await handler(request)
        return response


async def orm_context(app):
    print("Starting ORM...")
    await init_orm()
    yield
    print("Closing ORM...")
    await close_orm()


app.cleanup_ctx.append(orm_context)
app.middlewares.append(session_middleware)


def get_error(err_cls, message):
    return err_cls(
        text=json.dumps({"error": message}),
        content_type="application/json"
    )


async def get_ad_by_id(ad_id: int, session: AsyncSession) -> Ad:
    ad = await session.get(Ad, ad_id)
    if ad is None:
        raise get_error(web.HTTPNotFound, "Ad not found")
    return ad


async def add_ad(ad: Ad, session: AsyncSession):
    session.add(ad)
    try:
        await session.commit()
    except IntegrityError:
        raise get_error(web.HTTPConflict, "Ad conflict")
    return ad


class AdView(web.View):

    @property
    def ad_id(self):
        return int(self.request.match_info["ad_id"])

    @property
    def session(self):
        return self.request.session

    async def get(self):
        ad = await get_ad_by_id(self.ad_id, self.session)
        return web.json_response(ad.dict)

    async def post(self):
        try:
            data = await self.request.json()
            ad_data = AdCreateSchema(**data)
        except (ValidationError, json.JSONDecodeError) as e:
            raise get_error(web.HTTPBadRequest, str(e))

        ad = Ad(**ad_data.dict())
        await add_ad(ad, self.session)
        return web.json_response(ad.id_dict)

    async def patch(self):
        ad = await get_ad_by_id(self.ad_id, self.session)
        data = await self.request.json()

        for field in ['title', 'description', 'owner']:
            if field in data:
                setattr(ad, field, data[field])

        await add_ad(ad, self.session)
        return web.json_response(ad.dict)

    async def delete(self):
        ad = await get_ad_by_id(self.ad_id, self.session)
        await self.session.delete(ad)
        await self.session.commit()
        return web.json_response({"status": "deleted"})


app.add_routes([
    web.post('/api/v1/ads', AdView),
    web.get('/api/v1/ads/{ad_id:\d+}', AdView),
    web.patch('/api/v1/ads/{ad_id:\d+}', AdView),
    web.delete('/api/v1/ads/{ad_id:\d+}', AdView),
])


if __name__ == "__main__":
    web.run_app(app, port=8080)