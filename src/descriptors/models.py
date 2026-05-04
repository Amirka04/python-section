from typing import Any, TypeAlias

JSON: TypeAlias = dict[str, Any]


class Model:
    def __init__(self, payload: JSON):
        self.payload = payload


class Field:
    def __init__(self, path: str):
        self.__path = path
    

    def __get__(self, instance, owner):
        # присвою переменной значение первого пути
        pathlist = self.__path.split(".")
        val = instance.payload[pathlist[0]]
        
        # дальше в цикле будет переписывать переменную пока не дойдём до конца
        # начну с нуля т.к. переменная val уже имеет в себе значение на 0 индексе
        for i in range(1, len(pathlist)): 
            try:
                val = val[pathlist[i]]
            except KeyError:
                return None
        return val


    def __set__(self, instance, value):
        pathlist = self.__path.split(".")
        current = instance.payload
        for key in pathlist[:-1]:
            current = current[key]
        current[pathlist[-1]] = value
