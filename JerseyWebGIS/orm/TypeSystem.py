from sqlalchemy.orm import registry, mapped_column, Mapped, Session, DeclarativeBase

from sqlalchemy import Integer, create_engine, Text, select, Boolean, update,BINARY
from .utils import getMockedCategoryData, sortedCategoryList, \
    createCategoryIndex, getCategoryWeight, getMockedIsGeometry, unfold_sorted_category, unzip_except_dict, unzip_all
from .LiteralEnum import CATEGORY, str2ormtype
import ast


class ORM_Mapper(object):
    mapper_registry = registry()

    @mapper_registry.mapped
    class CategoryStore(object):
        __tablename__ = "CategoryStore"

        name = mapped_column(Text, primary_key=True)

        category = mapped_column(Text)

        isGeometry = mapped_column(Boolean, default=False)

        def to_dict(self):
            return {ele.name: getattr(self, ele.name) for ele in
                    self.__table__.columns}

    def __init__(self):
        self.engine = create_engine("sqlite:///./test.db")
        self.mapper_registry.metadata.create_all(bind=self.engine)
        self.mapper_type = {}

    def build_ORM(self):
        """
        clear tables except CategoryStore,then try to create all tables in orm.
        :return:
        """
        self.mapper_type.clear()
        for table in self.mapper_registry.metadata.sorted_tables:
            if table.name != 'CategoryStore':
                self.mapper_registry.metadata.remove(table)

        categoryList = unfold_sorted_category(
            sortedCategoryList(self.__getCategories())
        )
        categoryList = list(
            map(self.__category2classtype, categoryList)
        )
        for category in categoryList:
            self.mapper_registry.mapped(
                category
            )
            self.mapper_type[category.__name__] = category

        self.mapper_registry.metadata.create_all(bind=self.engine)

    def addCategory(self, category: dict, isGeometry: bool):
        with Session(self.engine) as session:
            session.add(
                self.CategoryStore(
                    name=category["name"],
                    category=str(category),
                    isGeometry=isGeometry
                )
            )
            session.commit()
        return self

    def addCategories(self, categories: list[dict], isGeometry: list[bool]):
        with Session(self.engine) as session:
            for index, category in enumerate(categories):
                session.add(
                    self.CategoryStore(
                        name=category["name"],
                        category=str(category),
                        isGeometry=isGeometry[index]
                    )
                )
            session.commit()
        return self

    def deleteCategory(self, category_name: str):
        with Session(self.engine) as session:
            target = session.get(
                self.CategoryStore,
                {
                    "name": category_name
                }
            )
            session.delete(target)
            session.commit()

    def deleteCategoriesWithCondition(self, conditions: list[dict]):
        with Session(self.engine) as session:
            for condition in conditions:
                target = session.get(
                    self.CategoryStore,
                    condition
                )
                session.delete(target)
            session.commit()

    def addDataForOneCategory(self, data_category_name: str, datas: list[dict]):
        with Session(self.engine) as session:
            for data in datas:
                session.add(
                    self.mapper_type[data_category_name](
                        **data
                    )
                )
            session.commit()
        return self

    def selectDataFromOneCategory(self, category_name: str, num: int = 20):
        with Session(self.engine) as session:
            if num == -1:
                sql = select(
                    self.mapper_type[category_name]
                )
            else:
                sql = select(
                    self.mapper_type[category_name]
                ).limit(num)
            return [
                data.to_dict() for data in session.scalars(sql)
            ]
        return self

    def selectDatasWithUserDefinedCondition(self, category_name: str, condition: dict):

        target_category_class = self.mapper_type[category_name]

        with Session(self.engine) as session:
            sql = select(
                self.mapper_type[category_name]
            ).where(
                *[
                    statement for statement in map(
                        lambda ele: target_category_class.__getattribute__(target_category_class, ele[0]) == ele[1],
                        condition.items()
                    )
                ]
            )
            return [
                data.to_dict() for data in session.scalars(sql)
            ]

    def updateDataInOneCategory(self, category_name: str, update_ids: list[int],
                                newer_data: list[dict]):
        with Session(self.engine) as session:
            for index, _id in enumerate(update_ids):
                sql = update(self.mapper_type[category_name]).where(
                    self.mapper_type[category_name]._id == _id
                ).values(
                    **self.mapper_type[category_name](
                        **newer_data[index]).to_dict()
                )
                session.execute(sql)
            session.commit()

    def deleteDataInOneCategory(self, category_name: str, del_ids: list[int]):
        with Session(self.engine) as session:
            for _id in del_ids:
                target = session.get(
                    self.mapper_type[category_name],
                    {
                        "_id": _id
                    }
                )
                session.delete(target)
            session.commit()

    def testAddOneData(self, data: dict, data_category_name: str):
        with Session(self.engine) as session:
            t = self.mapper_type[data_category_name]
            session.add(
                t(**data)
            )
            session.commit()
        return self

    def getCategories(self):
        """
        Expose to the invoker,it will ensure the categories its return are the unfolded categories,which means every category will be mapping
        to the bottom-level of data type.
        :return:
        """
        self.__unfoldStoredCategory()
        with Session(self.engine) as session:
            sql = select(self.CategoryStore)
            return [
                category.to_dict() for category in session.scalars(sql)
            ]

    def __getCategories(self):
        with Session(self.engine) as session:
            sql = select(self.CategoryStore.category)
            return [
                ast.literal_eval(category) for category in session.scalars(sql)
            ]

    def __category2classtype(self, category: dict):
        """Category -> ClassType
        """

        class Base(DeclarativeBase):
            pass

        specifications = {
            key: val for key, val in
            map(lambda dic: (dic['keyName'], str2ormtype(dic['keyCategory'])),
                category[CATEGORY.specification])
        }
        if category[CATEGORY.name] == "坐标":
            print(1)
        specifications["__tablename__"] = category[CATEGORY.name]
        specifications["_id"] = mapped_column(Integer, primary_key=True,
                                              nullable=True)

        def to_dict(self):
            return {ele.name: getattr(self, ele.name) for ele in
                    self.__table__.columns}

        def for_update(self):
            return {str(getattr(self, ele.name)): ele.name for ele in
                    self.__table__.columns}

        def __getattribute__(self, name):
            print("self:", self)
            return self.__getattribute__(name)

        specifications["to_dict"] = to_dict
        specifications["for_update"] = for_update
        # specifications["__getattribute__"] =  __getattribute__
        return type(
            category[CATEGORY.name],
            (),
            dict(specifications)
        )

    def __unfoldStoredCategory(self):
        categories = []
        with Session(self.engine) as session:
            sql = select(self.CategoryStore.category)
            categories = unfold_sorted_category(
                sortedCategoryList(
                    [
                        ast.literal_eval(category) for category in session.scalars(sql)
                    ]
                )
            )
            for category in categories:

                sql = update(self.CategoryStore).where(self.CategoryStore.name == category["name"]).values(

                        category=str(category)

                )
                session.execute(sql)
            session.commit()

        print(categories)


class DataBaseHanlder(object):

    def __init__(self):
        self.ORMMapper = ORM_Mapper()
        self.ORMMapper.build_ORM()

    def Add_Categories(self, categories: list[dict], isGeometry: list[bool]):
        """
        Category-format:
        {
            "name":"category_name",
            "specification":[{
                {"keyName":"xxx","keyCategory":"xxx"}
            }]
        }
        :param categories:
        :param isGeometry:
        :return:
        """
        self.ORMMapper.addCategories(
            categories, isGeometry
        )
        self.ORMMapper.build_ORM()

    def Get_Categories(self):
        return self.ORMMapper.getCategories()

    def Add_Data(self, category_name, datas: list[dict]):
        """
        :param category_name:category's name.For instance:"Position"
        :param datas:[{"spec_name":"spec_value}].For instance:[{"Latitude":22,"Longitude":11}]
        :return:
        """
        self.ORMMapper.addDataForOneCategory(
            category_name, datas
        )

    def Get_Data_ByNums(self, category_name: str, num: int):
        """
        :param category_name:
        :param num:If num == -1,then get all datas
        :return:
        """
        return self.ORMMapper.selectDataFromOneCategory(
            category_name, num
        )

    def Get_Data_ByCondition(self, category_name: str, condition: dict):
        return self.ORMMapper.selectDatasWithUserDefinedCondition(
            category_name, condition
        )


if __name__ == "__main__":
    # d = DataBaseHanlder()
    # d.Add_Categories(
    #     [{
    #         "name":"你好",
    #         "specification":[
    #             {"keyName": "好感度", "keyCategory": "Double"},
    #         ]
    #     }],[False]
    # )
    a = ORM_Mapper()
    a.build_ORM()
    # categories = unfold_sorted_category(
    #     sortedCategoryList(getMockedCategoryData())
    # )
    # a.addCategories(categories,getMockedIsGeometry(4))
    # a.deleteCategoriesWithCondition(
    #     [
    #         {
    #             "name":"hello"
    #         },
    #         {
    #             "name":"坐标"
    #         }
    #     ]
    # )
    # print(a.build_ORM())
    # a.build_ORM()
    # print(a.selectDatasWithUserDefinedCondition("谈论点", {
    #     "回复_坐标_id": 1,
    #     "回复_id": 1
    # }))
    # a.addDataForOneCategory("坐标",[
    #     {
    #         "纬度":3,
    #         "经度":44
    #     }
    # ])
    # a.updateDataInOneCategory("坐标",[6],[
    #     {
    #         "纬度": 23,
    #         "经度": 121,
    #         "_id":6
    #     }
    # ])
