from sqlalchemy import Text,Integer,Double,Boolean,Date,DateTime,Time
from sqlalchemy.orm import mapped_column
from copy import deepcopy

def getCategoryStore():
    class CategoryStore(object):
        __tablename__ = "CategoryStore"

        name = mapped_column(Text,primary_key=True)

        category = mapped_column(Text)

        isGeometry = mapped_column(Boolean,default=False)

        def to_dict(self):
            return {ele.name: getattr(self, ele.name) for ele in self.__table__.columns}

    return deepcopy(CategoryStore)

def str2ormtype(str:str):
    str2ormtype = deepcopy({
        "Text": mapped_column(Text),
        "Integer": mapped_column(Integer),
        "Double": mapped_column(Double),
        "Boolean": mapped_column(Boolean),
        "Binary": mapped_column(Text),
        "Date": mapped_column(Date),
        "Datetime": mapped_column(DateTime),
        "Time": mapped_column(Time),
        "PrimaryId":mapped_column(Integer,primary_key=True,nullable=True)
    })
    return str2ormtype[str]


class CATEGORY:
    name = "name"
    specification = "specification"

    class SPECIFICATION:
        keyName = "keyName"
        keyCategory = "keyCategory"