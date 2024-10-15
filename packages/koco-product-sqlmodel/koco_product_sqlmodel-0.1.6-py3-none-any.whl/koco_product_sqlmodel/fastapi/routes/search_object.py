from fastapi import APIRouter, HTTPException, Depends
import koco_product_sqlmodel.dbmodels.definition as sql_def
import koco_product_sqlmodel.mdb_connect.select as mdb_select
import koco_product_sqlmodel.fastapi.routes.security as sec

router = APIRouter(tags=["Endpoints to generic object search methods"], dependencies=[Depends(sec.get_current_active_user),])

def get_product_group_by_field_like(search_field: str, search_string: str) -> list[sql_def.CProductGroup]:
    if search_field not in sql_def.CProductGroupGet().__dict__.keys():
        raise HTTPException(status_code=404, detail="search_field not in cproductgroup")
    res = mdb_select.select_objects_generic(
        object_type=sql_def.CProductGroup,
        where_str=f"cproductgroup.{search_field} like '%{search_string}%'",
        return_search_str=False
    )
    return res

@router.get("/product_group/{search_field}")
def get_product_group_where_search_field_like(search_field: str, search_string:str, limit: int|None=None, skip: int|None=None) -> list[sql_def.CProductGroupGet]:
    res=get_product_group_by_field_like(search_field=search_field, search_string=search_string)
    if res==None:
        return
    pgs = []
    limit, skip = check_limit_skip_vals(limit=limit, skip=skip, number_of_results=len(res))
    for item in res[skip:skip+limit]:
        pgs.append(
            sql_def.CProductGroupGet(**item.model_dump())
        )
    return pgs

@router.get("/product_group/count/{search_field}", response_description='{"count": 0}')
def get_product_group_count_where_search_field_like(search_field: str, search_string:str) -> dict[str, int]:
    res=get_product_group_by_field_like(search_field=search_field, search_string=search_string)
    if res==None:
        return {'count': 0}
    return {'count': len(res)}



def get_family_by_field_like(search_field: str, search_string: str) -> list[sql_def.CFamily]:
    if search_field not in sql_def.CFamilyGet().__dict__.keys():
        raise HTTPException(status_code=404, detail="search_field not in cfamily")
    res = mdb_select.select_objects_generic(
        object_type=sql_def.CFamily,
        where_str=f"cfamily.{search_field} like '%{search_string}%'",
        return_search_str=False
    )
    return res

@router.get("/family/{search_field}")
def get_family_where_search_field_like(search_field: str, search_string:str, limit: int|None=None, skip: int|None=None) -> list[sql_def.CFamilyGet]:
    res=get_family_by_field_like(search_field=search_field, search_string=search_string)
    if res==None:
        return
    pgs = []
    limit, skip = check_limit_skip_vals(limit=limit, skip=skip, number_of_results=len(res))
    for item in res[skip:skip+limit]:
        pgs.append(
            sql_def.CFamilyGet(**item.model_dump())
        )
    return pgs

@router.get("/family/count/{search_field}", response_description='{"count": 0}')
def get_family_count_where_search_field_like(search_field: str, search_string:str) -> dict[str, int]:
    res=get_family_by_field_like(search_field=search_field, search_string=search_string)
    if res==None:
        return {'count': 0}
    return {'count': len(res)}

def get_article_by_field_like(search_field: str, search_string: str) -> list[sql_def.CArticle]:
    if search_field not in sql_def.CArticleGet().__dict__.keys():
        raise HTTPException(status_code=404, detail="search_field not in carticle")
    res = mdb_select.select_objects_generic(
        object_type=sql_def.CArticle,
        where_str=f"carticle.{search_field} like '%{search_string}%'",
        return_search_str=False
    )
    return res

@router.get("/article/{search_field}")
def get_article_where_search_field_like(search_field: str, search_string:str, limit: int|None=None, skip: int|None=None) -> list[sql_def.CArticleGet]:
    res=get_article_by_field_like(search_field=search_field, search_string=search_string)
    if res==None:
        return
    pgs = []
    limit, skip = check_limit_skip_vals(limit=limit, skip=skip, number_of_results=len(res))
    for item in res[skip:skip+limit]:
        pgs.append(
            sql_def.CArticleGet(**item.model_dump())
        )
    return pgs

@router.get("/article/count/{search_field}", response_description='{"count": 0}')
def get_article_count_where_search_field_like(search_field: str, search_string:str) -> dict[str, int]:
    res=get_article_by_field_like(search_field=search_field, search_string=search_string)
    if res==None:
        return {'count': 0}
    return {'count': len(res)}




def check_limit_skip_vals(limit: int|None, skip: int|None, number_of_results: int) -> tuple[int, int]:
    if limit==None or limit>number_of_results:
        return(number_of_results, 0)
    if skip==None:
        return(limit, 0)
    if skip>number_of_results:
        return(number_of_results, 0)
    if skip+limit>number_of_results:
        return (skip+limit-number_of_results, skip)

def main():
    pass

if __name__=="__main__":
    main()