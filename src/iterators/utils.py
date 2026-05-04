from dataclasses import dataclass, field
from itertools import batched
from typing import Iterable, TypeAlias

SomeRemoteData: TypeAlias = int


@dataclass
class Query:
    per_page: int = 3
    page: int = 1


@dataclass
class Page:
    per_page: int = 3
    results: Iterable[SomeRemoteData] = field(default_factory=list)
    next: int | None = None


def request(query: Query) -> Page:
    data = [i for i in range(0, 10)]
    chunks = list(batched(data, query.per_page))
    return Page(
        per_page=query.per_page,
        results=chunks[query.page - 1],
        next=query.page + 1 if query.page < len(chunks) else None,
    )


class RetrieveRemoteData:
    def __init__(self, per_page: int):
        self.__per_page = per_page

    def __iter__(self):
        page_num = 1
        while True:
            respond = request(Query(per_page=self.__per_page, page=page_num))
            for element in respond.results:
                yield element
            page_num = respond.next
            if page_num is None:
                break

    
    def __next__(self):
        pass


class Fibo:
    def __init__(self, n: int):
        self.__prev = 0
        self.__next = 1
        self.__n = n    
    
    def __iter__(self):
        return self

    def __next__(self) -> int:
        last = self.__prev
        self.__prev, self.__next = self.__next, self.__prev + self.__next
        
        self.__n -= 1
        if self.__n + 1 <= 0: raise StopIteration 
        return last
