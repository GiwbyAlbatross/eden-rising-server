# ### NOT IMPLEMENTED ###

import fastapi
from fastapi import FastAPI, Request

import eden # local module
from eden.server.types import EntityPos2D, EntityState
from eden.logic import LogicalPlayer
from eden.server import errors

api = FastAPI(docs_url=None, redoc_url=None)

players: dict[str, LogicalPlayer] = {} # 'username':<Player object>
playerIPs: dict[str, str] = {} # 'username':'IP.of.that.user'

@api.post('/entity/player/position')
def updateplayerpos(entitypos: EntityPos2D) -> dict:
    pass
@api.post('/entity/player/state')
def updateplayerstate(entitystate: EntityState) -> dict:
    pass
@api.post('/entity/player/login')
def playerlogin(player: EntityState, request: Request) -> dict:
    clientIP = request.client.host
    username = player.entityID
    if username is None:
        return errors.missinginfo(clientIP, 'missing')
    if player in players:
        return errors.sketchyip(clientIP, username)
    # TODO: add some authentication logic
    playerIPs[username] = clientIP
    players[username] = LogicalPlayer(username, (0,704))
    return {'response':"SUCCESS", 'msg':"You are now connected."}
@api.post('/entity/player/logout')
def playerlogoff(player: EntityState) -> dict:
    pass
@api.get('/entity/player/list')
def listplayers() -> list:
    return list(player.keys())
@api.get('/entity/player/{username}/state')
def getplayerstate(username: str) -> dict:
    # returns EntityState
    pass
@api.get('/entity/player/{username}/position')
def getplayerposition(username: str) -> dict:
    # returns EntityPos2D
    pass
