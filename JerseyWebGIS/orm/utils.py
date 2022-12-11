"""
ATTENTION:Category shouldn't be referred with each other.
BasicCategory:
{
    name:"",
    type:Text||Integer||Double||Boolean||Binary||Date||Datetime||Time
}

Category:
{
    name:"",
    specification:[
        {
            keyName:"",
            keyCategory:BasicCategory||Category
        }
    ]
}

CategoryTupleList:
[
    (Category,weight)
]
"""
from .LiteralEnum import str2ormtype, CATEGORY
from copy import deepcopy

global BASICCATEGORY
BASICCATEGORY = ["Text", "Integer", "Double", "Boolean", "Binary", "Date", "Datetime", "Time","PrimaryId"]


def createCategoryIndex(category_list: list[dict]):
    """
    [Category]->CategoryIndex
    CategoryIndex:
    {
        "Category's name":index in [Category]
    }
    """
    return {name: index for index, name in map(lambda tup: (tup[0], tup[1]["name"]), enumerate(category_list))}


def createCategorySpecificationHash(category_list: list[dict]):
    return {name: specification for name, specification in
            map(lambda a: (a["name"], a["specification"]), category_list)}


def getCategoryWeight(category: dict) -> int:
    """
    Category->Integer(weight)

    If one of a Category's specification's keyCategory not BasicCategory,then its weight plus 1.
    """
    weight = 0
    for ele in category["specification"]:
        print(ele)
        if ele["keyCategory"] not in BASICCATEGORY:
            weight += 1
    return weight


def createCategoryTuples(category_list: list[dict]) -> list[tuple]:
    """
    [Category]->[tuple(Category,Weight)]
    """
    return [
        (category, weight) for category, weight in map(lambda ele: (ele, getCategoryWeight(ele)), category_list)
    ]


def sortedCategoryTuple(category_tuple: list[tuple]):
    return sorted(category_tuple, key=lambda tup: tup[1])


"""

"""


def categoryTuple2categoryList(category_tuple: list[tuple]) -> list[dict]:
    return [
        ele for ele in map(lambda tup: tup[0], category_tuple)
    ]


def sortedCategoryList(category_list: list[dict]) -> list[dict]:
    """
    [Category]->[Category]
    """
    return categoryTuple2categoryList(
        sortedCategoryTuple(
            createCategoryTuples(category_list)
        )
    )


# def specification2ormtype(specification:list[dict],sortedCategoryList:list[dict],categoryIndex:dict):
#     for one_specification in specification:
#         if one_specification["keyCategory"] in BASICCATEGORY:
#             one_specification["keyCategory"] = str2ormtype[
#                 one_specification["keyCategory"]
#             ]
#         else:


def getOneSpecInORM(one_specification: dict):
    """
    Dict(CategorySpecification,just str)->Dict(CategorySpecification,with mapping with orm)
    """
    if one_specification[CATEGORY.SPECIFICATION.keyCategory] in BASICCATEGORY:
        one_specification[CATEGORY.SPECIFICATION.keyCategory] = str2ormtype[
            one_specification[CATEGORY.SPECIFICATION.keyCategory]
        ]
        return one_specification


def unfoldOneSpec(one_spec: dict, mapping_hash: dict) -> list[dict]:
    """
    Example:
    one_spec:
        {
            "keyName":"纬度",
            "keyCategory":"Text"
        }
    mapping_hash:
        {
            "category_name":[{"category_name":"category_spec"}]
        }

    :param one_spec:
    :param mapping_hash:
    :return:
    """
    CATEGORYNAME = one_spec[CATEGORY.SPECIFICATION.keyCategory]
    if one_spec[CATEGORY.SPECIFICATION.keyCategory] not in BASICCATEGORY:
        mapping_result = mapping_hash[
            one_spec[CATEGORY.SPECIFICATION.keyCategory]
        ]

        def change_dictkeyName(dic: dict):
            dic["keyName"] = CATEGORYNAME + "_" + dic["keyName"]
            return dic

        result =  [
            ele for ele in map(lambda dic: change_dictkeyName(dic), unzip_except_dict(mapping_result))
        ]
        result.append(
            {
                "keyName":CATEGORYNAME + "_id",
                "keyCategory":"PrimaryId"
            }
        )

        return result
    else:
        return one_spec


def changeOneSpecificationKeyName(one_specification: dict, newname):
    one_specification["keyName"] = newname
    return one_specification


def unzipListInList(l: list):
    del_hash = []
    for index, ele in enumerate(l):
        if type(ele) == list:
            l.extend(ele)
            l.remove(ele)
    # for ele in del_hash:
    #     del l[ele]
    return l


def unzip_all(l: list):
    ele, *last_ele = l
    if last_ele != []:
        return list(ele) + unzip_all(last_ele)
    return list(ele)

# def unzip_bool(l:list[bool]):
#     for ele in l:


def unzip_except_dict(l: list):
    ele, *last_ele = l
    if last_ele != [] and type(ele) == dict:
        return [ele] + unzip_except_dict(last_ele)
    if last_ele != []:
        return list(ele) + unzip_except_dict(last_ele)
    if type(ele) == dict:
        return [ele]
    return list(ele)


def unfold_sorted_category(sorted_category: list[dict]):
    unfolded_hash = {}
    for category in sorted_category:
        category[CATEGORY.specification] = unzip_except_dict([ele for ele in map(lambda ele: unfoldOneSpec(ele, deepcopy(unfolded_hash)),
                                                               category[CATEGORY.specification])])
        unfolded_hash[category[CATEGORY.name]] = category[CATEGORY.specification]
    return sorted_category


def getMockedCategoryData():
    return [
        {
            "name": "坐标",
            "specification": [
                {"keyName": "纬度", "keyCategory": "Double"},
                {"keyName": "经度", "keyCategory": "Double"}
            ]
        },
        {
            "name": "回复",
            "specification": [
                {"keyName": "日期", "keyCategory": "Date"},
                {"keyName": "時間", "keyCategory": "Time"},
                {"keyName": "回复坐标", "keyCategory": "坐标"}
            ]
        },
        {
            "name": "谈论点",
            "specification": [
                {"keyName": "日期", "keyCategory": "Date"},
                {"keyName": "時間", "keyCategory": "Time"},
                {"keyName": "谈论内容", "keyCategory": "回复"}
            ]
        },
        {
            "name": "hello",
            "specification": [
                {"keyName": "引用名", "keyCategory": "Text"}
            ]
        }
    ]


def getMockedIsGeometry(num: int):
    return [True for ele in range(num)]


if __name__ == "__main__":
    inputV = sortedCategoryList(getMockedCategoryData())
    inputV = unfold_sorted_category(inputV)
    inputIndex = createCategoryIndex(inputV)
    test = createCategorySpecificationHash(inputV)
    d = [
        {"keyName": "引用名", "keyCategory": "Text"}
        ,
        [1, 2, 3, 4, 5],
        [
            {"keyName": "引用名", "keyCategory": "Text"},
            {"keyName": "引用名", "keyCategory": "Text"},
            {"keyName": "引用名", "keyCategory": "Text"}
        ],
        {"keyName": "引用名", "keyCategory": "Text"}]
    gg = unzip_except_dict(d)
    dd = getMockedIsGeometry(5)


    for ele in inputV:
        ele[CATEGORY.specification] = unzip_except_dict(ele[CATEGORY.specification])
    print(inputV)
