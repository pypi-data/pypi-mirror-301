from fastapi import APIRouter, Depends, HTTPException, Request

import koco_product_sqlmodel.fastapi.routes.security as sec
import koco_product_sqlmodel.dbmodels.definition as sqlm
import koco_product_sqlmodel.mdb_connect.catalogs as mdb_cat
import koco_product_sqlmodel.mdb_connect.mdb_connector as mdb_con

router = APIRouter(
    dependencies=[Depends(sec.get_current_active_user)],
    tags=["Endpoints to CATALOG-data"],
)


@router.get("/")
def get_catalogs() -> list[mdb_cat.CCatalogGet]:
    catalogs = mdb_cat.collect_catalogs_db_items()
    cats_get = []
    for cat in catalogs:
        cats_get.append(
            sqlm.CCatalogGet(
                id=cat.id,
                supplier=cat.supplier,
                year=cat.year,
                user_id=cat.user_id,
                insdate=cat.insdate,
                upddate=cat.upddate,
            )
        )
    return cats_get


@router.get("/{id}/")
def get_catalog_by_id(id) -> mdb_cat.CCatalogGet:
    catalog = mdb_cat.collect_catalog_by_id(id)
    return catalog


@router.post("/", dependencies=[Depends(sec.has_post_rights)])
async def create_catalog(catalog: sqlm.CCatalogPost, request: Request) -> mdb_cat.CCatalogGet:
    user_id = await sec.get_user_id_from_request(request=request)
    new_catalog = mdb_cat.create_catalog(
        mdb_cat.CCatalog(
            supplier=catalog.supplier,
            year=catalog.year,
            status=catalog.status,
            user_id=user_id,
        )
    )
    return mdb_cat.CCatalogGet(**new_catalog.model_dump())


@router.patch(
    "/{id}/",
    dependencies=[
        Depends(sec.has_post_rights),
    ],
)
async def update_catalog(id: int, catalog: sqlm.CCatalogPost, request: Request) -> mdb_cat.CCatalogGet:
    catalog.user_id = await sec.get_user_id_from_request(request=request)
    updated_catalog = mdb_cat.update_catalog(id=id, catalog=catalog)
    if updated_catalog == None:
        raise HTTPException(status_code=404, detail="Catalog not found")
    return mdb_cat.CCatalogGet(**updated_catalog.model_dump())


@router.delete("/{id}/", dependencies=[Depends(sec.has_post_rights)])
def delete_catalog_by_id(id: int, delete_recursive: bool = True) -> dict[str, bool]:
    """
    Delete a catalog item by ccatalog.id.

    * Request parameter: *delete_recursive* = true

    If set to *true* all subitems contained in given catalog will be removed from database to avoid orphaned data
    """
    if delete_recursive == True:
        delete_recursive = True
    mdb_con.delete_catalog_by_id(catalog_id=id, delete_connected_items=delete_recursive)
    return {"ok": True}


def main():
    pass


if __name__ == "__main__":
    main()
