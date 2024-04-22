from typing import List, TypeVar, Dict, Any, Generic
import operator
import strawberry

# Paginacion basada en offset
T = TypeVar("T")

@strawberry.type
class PaginationWindow(Generic[T]):
    items: List[T] = strawberry.field(description="Lista de items en ventana de paginacion.")
    total_items_count: int = strawberry.field(description="Total de items en el dataset.")

class Pagination:
    @staticmethod
    def get_pagination_window(
        dataset: List[T],
        ItemType: type,
        order_by: str,
        limit: int,
        offset: int = 0,
        filters: dict[str, str] = {}) -> PaginationWindow:
        """
        Get one pagination window on the given dataset for the given limit
        and offset, ordered by the given attribute and filtered using the
        given filters
        """

        datasetOut = []

        if limit <= 0 or limit > 100:
            raise Exception(f"limit ({limit}) debe estar entre 0 y 100")

        if filters:
            fieldName = list(filters.keys())[0]
            filterValues = list(filters.values())[0]
            filterList = filterValues.split(',')
            for item in dataset:
                if item[fieldName] in filterList:
                    datasetOut.append(item)
            # dataset = list(filter(lambda x: __class__.matches(x, filters), dataset))
        else:
            datasetOut = dataset.copy()
            
        # attrorder = operator.attrgetter(order_by)
        # dataset.sort(key=attrorder)
            
        datasetOut.sort(key=lambda x: x[order_by])

        if offset != 0 and not 0 <= offset < len(datasetOut):
            raise Exception(f"offset ({offset}) is out of range " f"(0-{len(datasetOut) - 1})")

        total_items_count = len(datasetOut)
        items = datasetOut[offset : offset + limit]
        items = [ItemType.from_row(x) for x in items]

        return PaginationWindow(items=items, total_items_count=total_items_count)

    @staticmethod
    def matches(item, filters):
        """
        Test whether the item matches the given filters.
        This demo only supports filtering by string fields.
        """
        for attr_name, val in filters.items():
            if val not in item[attr_name]:
                return False
        return True
