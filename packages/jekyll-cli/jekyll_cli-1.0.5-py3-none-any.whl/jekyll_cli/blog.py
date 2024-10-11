# -*- coding: UTF-8 -*-
import re
from fnmatch import fnmatch
from typing import List, Dict

from .config import Config
from .item import Item, BlogType


class __Blog:

    def __init__(self):
        self.__post_items: Dict[str, Item] | None = None
        self.__draft_items: Dict[str, Item] | None = None

    @property
    def posts(self) -> List[Item]:
        return list(self.__posts_dict.values())

    @property
    def drafts(self) -> List[Item]:
        return list(self.__drafts_dict.values())

    @property
    def articles(self) -> List[Item]:
        return self.posts + self.drafts

    @property
    def __posts_dict(self) -> Dict[str, Item]:
        if not self.__post_items:
            self.__post_items = self.__initialize_items(BlogType.Post)
        return self.__post_items

    @property
    def __drafts_dict(self) -> Dict[str, Item]:
        if not self.__draft_items:
            self.__draft_items = self.__initialize_items(BlogType.Draft)
        return self.__draft_items

    def find(self, pattern: str, subset: BlogType | None = None) -> List[Item]:
        match subset:
            case BlogType.Post:
                items = self.__posts_dict
            case BlogType.Draft:
                items = self.__drafts_dict
            case _:
                items = dict(self.__posts_dict, **self.__drafts_dict)

        # precise match
        item = items.get(pattern)
        if item is not None:
            return [item]

        # fuzzy match
        return [item for name, item in items.items() if fnmatch(name, f'*{pattern}*')]

    def __initialize_items(self, type_: BlogType) -> Dict[str, Item]:
        parent_dir = Config.root / type_.value
        if not parent_dir.is_dir():
            raise ValueError(f'{parent_dir} is not a directory.')

        if Config.mode == 'item':
            item_paths = [f for f in parent_dir.iterdir() if f.is_dir()]
        else:
            item_paths = [f for f in parent_dir.iterdir() if f.is_file() and f.suffix == '.md']

        items = {}
        for item_path in item_paths:
            if Config.mode == 'item':
                name = item_path.name
            else:
                pattern = r'\d{4}-\d{2}-\d{2}-(.+)\.md' if type_ == BlogType.Post else r'(.+)\.md'
                name = re.search(pattern, item_path.name).group(1)
            items[name] = Item(name, type_, item_path)
        return items

    def __contains__(self, item: Item) -> bool:
        return item.name in (self.__posts_dict if item.type == BlogType.Post else self.__drafts_dict)


Blog: __Blog = __Blog()
