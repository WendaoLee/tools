from dataclasses import dataclass
g:str = "hello"
a = type(
    "hello",
    (),
    dict(g = g)
)
def b(a=0):
    print(a)


class testc:
    aa:str = 2
    bb = 1

    def __getitem__(self, item):
        print(self.__getattribute__(item))

# def test_m(i:str):
#     a = {
#         "h":233
#     }
#     return a[i]

a = testc()
a["aa"]
# args = {
#     "aa":1
# }
# gg = testc(aa = "2")
#
#
# b(1)
# print(a)

