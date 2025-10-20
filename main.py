# ### NOT IMPLEMENTED ###

import fastapi

import eden # local module
from eden.server.types import EntityPos2D, EntityState


api = fastapi.FastAPI(docs_url=None, redoc_url=None)

@api.post('/entity/player/position')
def updateplayerpos(entitypos: EntityPos2D) -> dict:
    pass
@api.post('/entity/player/state')
def updateplayerstate(entitystate: EntityState) -> dict:
    pass
@api.post('/entity/player/login')
def playerlogin(player: EntityState) -> dict:
    pass
@api.post('/entity/player/logout')
def playerlogoff(player: EntityState) -> dict:
    pass
@api.get('/entity/player/list')
def listplayers() -> list:
    pass
@api.get('/entity/player/{username}/state')
def getplayerstate(username: str) -> dict:
    # returns EntityState
    pass
@api.get('/entity/player/{username}/position')
def getplayerposition(username: str) -> dict:
    # returns EntityPos2D
    pass
