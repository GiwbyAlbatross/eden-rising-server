# ### MOSTLY IMPLEMENTED, NOW TESTING ###

from __future__ import annotations
import logging

import fastapi
from fastapi import FastAPI, Request

import eden  # local module
from eden.server.types import EntityPos2D, EntityState
from eden.logic import LogicalPlayer
from eden.server import errors, auth, DEFAULT_BANNER

VERSION = "v0.0.1-pre/incomplete"

if __debug__:
    api = FastAPI()
else:
    api = FastAPI(docs_url=None, redoc_url=None)
eden.IS_SERVER = True

logger = logging.getLogger(__name__)
authlogger = logging.getLogger(__name__ + ".auth")

players: dict[str, LogicalPlayer] = {}  # 'username':<Player object>
playerIPs: dict[str, str] = {}  # 'username':'IP.of.that.user'


def _verify_ip(ip: str, username: str) -> bool:
    "verify that the source of a POST affecting `user` comes from the same IP as the logon from that user"
    r = ip == playerIPs[username]
    if not r:
        authlogger.warning(
            f"IP address verification failed for user {username} from {ip}"
        )
        authlogger.info(f"Authentic IP for {username}: {playerIPs[username]}")
    return r


@api.post("/entity/player/position")
async def updateplayerpos(entitypos: EntityPos2D, request: Request) -> dict:
    clientIP = request.client.host
    username = entitypos.entityID
    if not _verify_ip(clientIP, username):
        return errors.sketchyip(clientIP, username)
    players[username].setpos(entitypos)
    return {"response": "SUCCESSS", "type": "update:state"}


@api.post("/entity/player/state")
async def updateplayerstate(entitystate: EntityState, request: Request) -> dict:
    clientIP = request.client.host
    username = entitystate.entityID
    if not _verify_ip(clientIP, username):
        return errors.sketchyip(clientIP, username)
    players[username].set_state(entitystate)
    return {"response": "SUCCESSS", "type": "update:pos"}


@api.get("/entity/player/inv")
async def getplayerinv() -> dict:
    # get inventory
    pass


@api.post("/entity/player/inv/holditem")
async def switch_held_item(invslot: int, request: Request) -> dict:
    pass


@api.post("/entity/player/login")
async def playerlogin(player: EntityState, request: Request) -> dict:
    clientIP = request.client.host
    username = player.entityID
    if username is None:
        return errors.missinginfo(clientIP, "missing")
    if username in players:
        return errors.sketchyip(clientIP, username)
    if player.hashedpass is None:
        return errors.missinginfo(clientIP, username)
    if not (await auth.verifypass(username, player.hashedpass)):
        return errors.wrongpass(clientIP, username)
    # TODO: add some authentication logic
    playerIPs[username] = clientIP
    players[username] = LogicalPlayer()
    players[username].init(username, (0, 704))
    return {
        "response": "SUCCESS",
        "type": "log:on",
        "msg": "You are now connected.",
        "banner": DEFAULT_BANNER % {"version": VERSION},
    }


@api.post("/entity/player/logout")
async def playerlogoff(player: EntityState, request: Request) -> dict:
    clientIP = request.client.host
    username = player.entityID
    if username is None:
        return errors.missinginfo(clientIP, "missing")
    if username not in players:
        return errors.notfound(clientIP, username)
    if clientIP != playerIPs[username]:
        return errors.sketchyip(clientIP, username)
    del players[username]
    del playerIPs[username]
    return {"response": "SUCCESS", "type": "log:off", "msg": "You are now disconnected"}


@api.get("/entity/player/list")
async def listplayers() -> list:
    return list(players.keys())


@api.get("/entity/player/{username}/state")
async def getplayerstate(username: str) -> EntityState | dict:
    if username in players:
        return players[username].get_state()
    else:
        return errors.notfound("?.?.?.?", username)


@api.get("/entity/player/{username}/position")
async def getplayerposition(username: str) -> EntityPos2D | dict:
    if username in players:
        return players[username].getpos()
    else:
        return errors.notfound("?.?.?.?", username)


@api.post("/_/admin/console")
async def runconsolecmd(cmd: str, request: Request) -> dict:
    # run an admin console command, request is taken for logging
    clientIP = request.client.host
    authlogger.info(
        f"User at {clientIP} tried to access admin console running command {cmd!r}"
    )
    return errors.unimplemented("admin-console")
