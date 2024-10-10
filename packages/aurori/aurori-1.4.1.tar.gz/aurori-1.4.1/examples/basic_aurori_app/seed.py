import logging
from sqlalchemy.orm import Session
from aurori.features.database import Permission, PermissionGroup
from app.User.database import User

logger = logging.getLogger("APP")

def seed_environment(db : Session, clean=False):
    logger.info("")
    logger.info("Create environment")
    if clean is True:
        db.query(User).delete()
        db.query(PermissionGroup).delete()

    pAll = db.query(Permission).all()
    permissions = {}
    logger.info(f'  Found {len(pAll)} permissions:')
    for p in pAll:
        permissions[p.name] = p
        logger.info(f'    {p}')


    if len(db.query(User).filter(User.email=="admin@fabba.space").all()) == 0:
        user = User("admin@fabba.space", "change",isAdmin=True)
        user.firstname = "Test"
        user.lastname = "User"
        db.add(user)

    db.commit()

    all_user = db.query(User).all()
    logger.info(f'  Found {len(all_user)} users:')
    for u in all_user:
        logger.info(f'    {u}')
    return
