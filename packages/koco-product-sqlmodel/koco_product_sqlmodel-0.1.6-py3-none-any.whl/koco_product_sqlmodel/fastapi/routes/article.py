from fastapi import HTTPException, Request

import koco_product_sqlmodel.dbmodels.definition as sqlm
import koco_product_sqlmodel.mdb_connect.generic_object_connect as mdb_gen
import koco_product_sqlmodel.mdb_connect.mdb_connector as mdb_con
import koco_product_sqlmodel.fastapi.routes.generic_route as rgen
import koco_product_sqlmodel.fastapi.routes.security as rsec


class ArticleRoute(rgen.MyBaseRoute):
    def __init__(
        self,
        sqlmodel_db: sqlm.SQLModel,
        sqlmodel_post: sqlm.SQLModel,
        sqlmodel_get: sqlm.SQLModel,
        tags: list[str],
    ):
        super().__init__(
            sqlmodel_db=sqlmodel_db,
            sqlmodel_post=sqlmodel_post,
            sqlmodel_get=sqlmodel_get,
            tags=tags,
        )

    async def post_object(self, object: sqlm.CArticlePost, request: Request) -> sqlm.SQLModel:
        user_id = await rsec.get_user_id_from_request(request=request)
        object.user_id=user_id
        new_obj = mdb_gen.post_object(db_obj=self.sqlmodel_db(**object.model_dump()))
        return self.sqlmodel_get(**new_obj.model_dump())

    async def patch_object(self, id: int, obj: sqlm.CArticlePost, request: Request) -> sqlm.SQLModel:
        obj.user_id = await rsec.get_user_id_from_request(request=request)
        updated_object = mdb_gen.patch_object(
            id=id, db_obj=obj, db_obj_type=self.sqlmodel_db
        )
        if updated_object == None:
            raise HTTPException(status_code=404, detail="Object not found")
        return self.sqlmodel_get(**updated_object.model_dump())

    def delete_object(self, id: int) -> dict[str, bool]:
        """
        Delete an article item by carticle.id.

        * Request parameter: *delete_recursive* = true

        If set to *true* all subitems contained in given article will be removed from database to avoid orphaned data
        """
        if delete_recursive == True:
            delete_recursive = True
        mdb_con.delete_article_by_id(
            article_id=id, delete_connected_items=delete_recursive
        )
        return {"ok": True}


route_article = ArticleRoute(
    sqlmodel_db=sqlm.CArticle,
    sqlmodel_get=sqlm.CArticle,
    sqlmodel_post=sqlm.CArticle,
    tags=["Endpoints to ARTICLE-data"],
)


# from fastapi import APIRouter, Depends, HTTPException

# import koco_product_sqlmodel.fastapi.routes.security as sec
# import koco_product_sqlmodel.dbmodels.definition as sqlm
# import koco_product_sqlmodel.mdb_connect.articles as mdb_art
# import koco_product_sqlmodel.mdb_connect.mdb_connector as mdb_con

# router = APIRouter(
#     dependencies=[Depends(sec.get_current_active_user)],
#     tags=["Endpoints to ARTICLE-data"],
# )
# # router = APIRouter()


# @router.get("/")
# def get_articles(family_id: int = None) -> list[mdb_art.CArticleGet]:
#     """
#     GET articles from DB.
#     Optional parameter:
#     * *family_id* - when specified, only articles from the selected family are retrieved
#     """
#     arts = mdb_art.get_articles_db(family_id=family_id)
#     arts_get = []
#     for art in arts:
#         art_dump = art.model_dump()
#         art_get = sqlm.CArticleGet(**art_dump)
#         arts_get.append(art_get)
#     return arts_get


# @router.get("/{id}/")
# def get_article_db_by_id(id) -> mdb_art.CArticleGet:
#     pg_art = mdb_art.get_article_db_by_id(id=id)
#     if pg_art == None:
#         raise HTTPException(status_code=404, detail="Article not found")
#     return sqlm.CArticleGet(**pg_art.model_dump())


# @router.post("/", dependencies=[Depends(sec.has_post_rights)])
# def create_family(art: sqlm.CArticlePost) -> mdb_art.CArticleGet:
#     new_art = mdb_art.create_article(article=sqlm.CArticle(**art.model_dump()))
#     return mdb_art.CArticleGet(**new_art.model_dump())


# @router.patch(
#     "/{id}/",
#     dependencies=[
#         Depends(sec.has_post_rights),
#     ],
# )
# def update_article(id: int, art: sqlm.CArticlePost) -> mdb_art.CArticleGet:
#     updated_article = mdb_art.update_article_DB(id=id, art_post=art)
#     if updated_article == None:
#         raise HTTPException(status_code=404, detail="Article not found")
#     return mdb_art.CArticleGet(**updated_article.model_dump())


# @router.delete("/{id}/", dependencies=[Depends(sec.has_post_rights)])
# def delete_article_by_id(id: int, delete_recursive: bool = True) -> dict[str, bool]:
#     """
#     Delete an article item by carticle.id.

#     * Request parameter: *delete_recursive* = true

#     If set to *true* all subitems contained in given article will be removed from database to avoid orphaned data
#     """
#     if delete_recursive == True:
#         delete_recursive = True
#     mdb_con.delete_article_by_id(article_id=id, delete_connected_items=delete_recursive)
#     return {"ok": True}


def main():
    pass


if __name__ == "__main__":
    main()
