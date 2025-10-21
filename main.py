aync# ### PARTIALLY IMPLEMENTED ###

import logging

import fastapi
from fastapi import FastAPI, Request

import eden # local module
from eden.server.types import EntityPos2D, EntityState
from eden.logic import LogicalPlayer
from eden.server import errors

api = FastAPI(docs_url=None, redoc_url=None)

logger = logging.getLogger(__name__)
authlogger = logging.getLogger(__name__+'.auth')

players: dict[str, LogicalPlayer] = {} # 'username':<Player object>
playerIPs: dict[str, str] = {} # 'username':'IP.of.that.user'

def _verify_ip(ip: str, username: str) -> bool:
    r = ip == playerIPs[username]
    if not r:
        authlogger.warning(f"IP address verification failed for user {username} from {ip}")
        authlogger.info(f"Authentic IP for {username}: {playerIPs[username]}")
    return r

@api.post('/entity/player/position')
async def updateplayerpos(entitypos: EntityPos2D) -> dict:
    pass
@api.post('/entity/player/state')
async def updateplayerstate(entitystate: EntityState) -> dict:
    pass
@api.post('/entity/player/login')
async def playerlogin(player: EntityState, request: Request) -> dict:
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
async def playerlogoff(player: EntityState) -> dict:
    clientIP = request.client.host
    username = player.entityID
    if username is None:
        return errors.missinginfo(clientIP, 'missing')
    if clientIP != playerIPs[username]:
        return errors.sketchyip(clientIP, username)
    del players[username]
    del playerIPs[username]
    return {'response':"SUCCESS", 'msg':"You are now disconnected"}
@api.get('/entity/player/list')
async def listplayers() -> list:
    return list(player.keys())
@api.get('/entity/player/{username}/state')
async def getplayerstate(username: str) -> dict:
    # returns EntityState
    pass
@api.get('/entity/player/{username}/position')
async def getplayerposition(username: str) -> dict:
    # returns EntityPos2D
    pass
