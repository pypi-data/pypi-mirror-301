from sqlmodel import select, Session
import koco_product_sqlmodel.dbmodels.changelog as sql_change
import koco_product_sqlmodel.dbmodels.definition as sql_def
import koco_product_sqlmodel.mdb_connect.mdb_connector as mdb_con

def get_changes_for_entity_with_id(entity_id: int|None) -> list[sql_change.CChangelogGet]|None:
    if entity_id==None:
        statement=select(sql_change.CChangelog)
    else:
        statement = select(sql_change.CChangelog).where(sql_change.CChangelog.entity_id==entity_id)
    res = []
    with Session(mdb_con.mdb_engine) as session:
        results = session.exec(statement=statement).all()
        for r in results:
            return_res = sql_change.CChangelogGet(**r.model_dump())
            return_res.user_name = get_user_name_from_id(session=session, user_id=r.user_id)
            res.append(return_res)
    return res

def get_user_name_from_id(session: Session=None, user_id: int=None)->str|None:
    if not user_id:
        return
    if session!=None:
        statemnt_user = select(sql_def.CUser.name).where(sql_def.CUser.id == user_id)
        user_name = session.exec(statement=statemnt_user).one_or_none()
        return user_name
    with Session(mdb_con.mdb_engine) as session:
        return get_user_name_from_id(session=session, user_id=user_id)

def get_change_by_id(id: int=None)->sql_change.CChangelogGet|None:
    statement = select(sql_change.CChangelog).where(sql_change.CChangelog.id==id)
    with Session(mdb_con.mdb_engine) as session:
        res = session.exec(statement=statement).one_or_none()
        if res!=None:
            return_res = sql_change.CChangelogGet(**res.model_dump())
            return_res.user_name = get_user_name_from_id(user_id=res.user_id)
            return return_res
        

def main():
    pass

if __name__=="__main__":
    main()