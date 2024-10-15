from fastapi import Request, HTTPException, APIRouter, Depends

import koco_product_sqlmodel.dbmodels.changelog as sqlc
import koco_product_sqlmodel.mdb_connect.changelog as mdb_change
import koco_product_sqlmodel.mdb_connect.generic_object_connect as mdb_gen
import koco_product_sqlmodel.fastapi.routes.security as rsec


class ChangelogRoute:
    def __init__(
        self,
        sqlmodel_db: sqlc.SQLModel,
        sqlmodel_post: sqlc.SQLModel,
        sqlmodel_get: sqlc.SQLModel,
        tags: list[str],
    ):
        self.router = APIRouter(
            dependencies=[Depends(rsec.get_current_active_user)],
            tags=tags,
        )
        self.sqlmodel_db = sqlmodel_db
        self.sqlmodel_post = sqlmodel_post
        self.sqlmodel_get = sqlmodel_get
        self.router.add_api_route(
            path="/",
            endpoint=self.get_objects,
            methods=["GET"],
            response_model=list[self.sqlmodel_get],
        )
        self.router.add_api_route(
            path="/{id}/",
            endpoint=self.get_object,
            methods=["GET"],
            response_model=self.sqlmodel_get,
        )
        self.router.add_api_route(
            path="/",
            endpoint=self.post_object,
            methods=["POST"],
            dependencies=[Depends(rsec.has_post_rights)],
            response_model=self.sqlmodel_get,
        )
        self.router.add_api_route(
            path="/{id}/",
            endpoint=self.delete_object,
            methods=["DELETE"],
            dependencies=[Depends(rsec.has_post_rights)],
        )


    def get_objects(self, entity_id: int|None=None) -> list[sqlc.CChangelogGet]:
        """
        GET list of changelog-objects from DB.
        Optional parameter:
        * *entity_id* - when specified a list of objects with provided entity_id will be provided
        """
        return mdb_change.get_changes_for_entity_with_id(entity_id=entity_id)

    def get_object(self, id) -> sqlc.CChangelogGet:
        return mdb_change.get_change_by_id(id=id)


    async def post_object(self, object: sqlc.CChangelogPost, request: Request) -> sqlc.SQLModel:
        object.user_id = await rsec.get_user_id_from_request(request=request)
        new_obj = mdb_gen.post_object(db_obj=self.sqlmodel_db(**object.model_dump()))
        return self.sqlmodel_get(**new_obj.model_dump())

    def delete_object(self, id: int) -> dict[str, bool]:
        """
        Delete an object item by cobject.id.
        """
        res = mdb_gen.delete_object(db_obj_type=self.sqlmodel_db, id=id)
        if res == None:
            raise HTTPException(status_code=404, detail="Object not found")
        return {"ok": True}

route_changelog = ChangelogRoute(
    sqlmodel_db=sqlc.CChangelog,
    sqlmodel_get=sqlc.CChangelogGet,
    sqlmodel_post=sqlc.CChangelogPost,
    tags=["Endpoints to CHANGELOG-data"],
)


def main():
    pass


if __name__ == "__main__":
    main()
