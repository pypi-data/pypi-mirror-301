import flask
from flask import request, current_app, url_for
from flask_babel import gettext as _
from geovisio.utils import auth, db
from geovisio import errors
from psycopg.rows import dict_row
from psycopg.sql import SQL

from geovisio.web import stac
from geovisio.web.utils import get_root_link

bp = flask.Blueprint("user", __name__, url_prefix="/api/users")


def _get_user_info(id, name):
    userMapUrl = (
        flask.url_for("map.getUserTile", userId=id, x="11111111", y="22222222", z="33333333", format="mvt", _external=True)
        .replace("11111111", "{x}")
        .replace("22222222", "{y}")
        .replace("33333333", "{z}")
    )
    response = {
        "id": id,
        "name": name,
        "links": [
            {"rel": "catalog", "type": "application/json", "href": flask.url_for("stac.getUserCatalog", userId=id, _external=True)},
            {
                "rel": "collection",
                "type": "application/json",
                "href": flask.url_for("stac_collections.getUserCollection", userId=id, _external=True),
            },
            {
                "rel": "user-xyz",
                "type": "application/vnd.mapbox-vector-tile",
                "href": userMapUrl,
                "title": "Pictures and sequences vector tiles for a given user",
            },
        ],
    }
    return flask.jsonify(response)


@bp.route("/me")
@auth.login_required_with_redirect()
def getMyUserInfo(account):
    """Get current logged user informations
    ---
    tags:
        - Users
    responses:
        200:
            description: Information about the logged account
            content:
                application/json:
                    schema:
                        $ref: '#/components/schemas/GeoVisioUser'
    """
    return _get_user_info(account.id, account.name)


@bp.route("/<uuid:userId>")
def getUserInfo(userId):
    """Get user informations
    ---
    tags:
        - Users
    parameters:
        - name: userId
          in: path
          description: User ID
          required: true
          schema:
            type: string
    responses:
        200:
            description: Information about a user
            content:
                application/json:
                    schema:
                        $ref: '#/components/schemas/GeoVisioUser'
    """
    account = db.fetchone(current_app, SQL("SELECT name, id FROM accounts WHERE id = %s"), [userId], row_factory=dict_row)
    if not account:
        raise errors.InvalidAPIUsage(_("Impossible to find user"), status_code=404)

    return _get_user_info(account["id"], account["name"])


@bp.route("/me/catalog")
@auth.login_required_with_redirect()
def getMyCatalog(account):
    """Get current logged user catalog
    ---
    tags:
        - Users
        - Sequences
    responses:
        200:
            description: the Catalog listing all sequences associated to given user. Note that it's similar to the user's colletion, but with less metadata since a STAC collection is an enhanced STAC catalog.
            content:
                application/json:
                    schema:
                        $ref: '#/components/schemas/GeoVisioCatalog'
    """
    return flask.redirect(flask.url_for("stac.getUserCatalog", userId=account.id, _external=True))


@bp.route("/me/collection")
@auth.login_required_with_redirect()
def getMyCollection(account):
    """Get current logged user collection
    ---
    tags:
        - Users
        - Sequences
    parameters:
        - $ref: '#/components/parameters/STAC_collections_limit'
        - $ref: '#/components/parameters/STAC_collections_filter'
        - $ref: '#/components/parameters/STAC_bbox'
        - $ref: '#/components/parameters/OGC_sortby'
    responses:
        200:
            description: the Collection listing all sequences associated to given user. Note that it's similar to the user's catalog, but with more metadata since a STAC collection is an enhanced STAC catalog.
            content:
                application/json:
                    schema:
                        $ref: '#/components/schemas/GeoVisioCollectionOfCollection'
    """

    return flask.redirect(
        flask.url_for(
            "stac_collections.getUserCollection",
            userId=account.id,
            filter=request.args.get("filter"),
            limit=request.args.get("limit"),
            sortby=request.args.get("sortby"),
            bbox=request.args.get("bbox"),
            _external=True,
        )
    )


@bp.route("/search")
def searchUser():
    """Search for a user
    ---
    tags:
        - Users
    responses:
        200:
            description: List of matching users
            content:
                application/json:
                    schema:
                        $ref: '#/components/schemas/GeoVisioUserSearch'
    """
    q = request.args.get("q")
    # for the moment, we can only search by string
    if not q:
        raise errors.InvalidAPIUsage(_("No search parameter given, you should provide `q=<pattern>` as query parameter"), status_code=400)

    limit = request.args.get("limit", default=20, type=int)
    query = SQL(
        """
WITH ranked AS (
    SELECT name, id, similarity({q}, name) AS similarity from accounts
)
SELECT * from ranked 
WHERE similarity > 0.1
ORDER BY similarity DESC
LIMIT {limit};
"""
    ).format(limit=limit, q=q)
    res = db.fetchall(current_app, query, row_factory=dict_row)

    return {
        "features": [
            {
                "label": r["name"],
                "id": r["id"],
                "links": [
                    {
                        "rel": "user-info",
                        "type": "application/json",
                        "href": flask.url_for("user.getUserInfo", userId=r["id"], _external=True),
                    },
                    {
                        "rel": "collection",
                        "type": "application/json",
                        "href": flask.url_for("stac_collections.getUserCollection", userId=r["id"], _external=True),
                    },
                ],
            }
            for r in res
        ]
    }


@bp.route("/")
def listUsers():
    """List all users
    ---
    tags:
        - Users
    responses:
        200:
            description: List of users
            content:
                application/json:
                    schema:
                        $ref: '#/components/schemas/GeoVisioUserList'
    """

    # no pagination yet, can be done when needed
    limit = min(request.args.get("limit", default=1000, type=int), 1000)
    query = SQL(
        """SELECT 
a.id, a.name, l.has_seq
FROM accounts a
LEFT OUTER JOIN LATERAL (
   SELECT 1 as has_seq
   FROM sequences s
   WHERE s.account_id = a.id
   LIMIT 1
) l ON true
ORDER BY created_at
LIMIT {limit};"""
    ).format(limit=limit)
    res = db.fetchall(current_app, query, row_factory=dict_row)
    return {
        "stac_version": stac.STAC_VERSION,
        "id": "geovisio:users",
        "title": "users catalog",
        "description": "List of users catalog",
        "type": "Catalog",
        "conformsTo": stac.CONFORMANCE_LIST,
        "users": [
            {
                "name": r["name"],
                "id": r["id"],
                "links": [
                    {
                        "rel": "user-info",
                        "type": "application/json",
                        "href": flask.url_for("user.getUserInfo", userId=r["id"], _external=True),
                    },
                    {
                        "rel": "collection",
                        "type": "application/json",
                        "href": flask.url_for("stac_collections.getUserCollection", userId=r["id"], _external=True),
                    },
                ],
            }
            for r in res
        ],
        "links": [
            {
                "rel": "user-search",
                "type": "application/json",
                "href": flask.url_for("user.searchUser", _external=True),
                "title": "Search users",
            },
            get_root_link(),
        ]
        + [
            {
                "rel": "child",
                "title": f'User "{r["name"]}" sequences',
                "href": url_for("stac_collections.getUserCollection", userId=r["id"], _external=True),
            }
            for r in res
            if r["has_seq"]
        ],
    }
