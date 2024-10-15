import logging
import uuid
from abc import ABC
from abc import abstractmethod
from typing import TYPE_CHECKING
from typing import Any
from typing import Generic
from typing import TypeVar
from typing import Union

import amsdal_glue as glue
from amsdal_data.connections.constants import PRIMARY_PARTITION_KEY
from amsdal_data.connections.constants import SECONDARY_PARTITION_KEY
from amsdal_data.connections.historical.data_query_transform import METADATA_TABLE_ALIAS
from amsdal_data.connections.historical.data_query_transform import NEXT_VERSION_FIELD
from amsdal_data.connections.historical.schema_version_manager import HistoricalSchemaVersionManager
from amsdal_data.services.operation_manager import OperationManager
from amsdal_data.services.table_schema_manager import TableSchemasManager
from amsdal_utils.models.data_models.address import Address
from amsdal_utils.models.enums import Versions
from amsdal_utils.query.data_models.paginator import CursorPaginator
from amsdal_utils.query.data_models.paginator import NumberPaginator
from amsdal_utils.query.enums import Lookup
from amsdal_utils.query.enums import OrderDirection
from amsdal_utils.query.mixin import QueryableMixin
from amsdal_utils.query.utils import ConnectorEnum
from amsdal_utils.query.utils import Q

from amsdal_models.querysets.errors import AmsdalQuerySetError

if TYPE_CHECKING:
    from amsdal_models.classes.model import Model
    from amsdal_models.querysets.base_queryset import QuerySetBase

logger = logging.getLogger(__name__)

DEFAULT_DB_ALIAS = 'default'
LAKEHOUSE_DB_ALIAS = 'lakehouse'
OBJECT_ID_FIELD = 'object_id'
OBJECT_VERSION_FIELD = 'object_version'
CLASS_VERSION_FIELD = 'class_version'
ADDRESS_FIELD = '_address'

ModelType = TypeVar('ModelType', bound='Model')


class ExecutorBase(Generic[ModelType], ABC):
    """
    Abstract base class for query executors.

    This class provides the base functionality for executing queries and counting
    results. It defines the interface that all concrete executor classes must implement.

    Attributes:
        queryset (QuerySetBase): The query set to be executed.
    """

    queryset: 'QuerySetBase[ModelType]'

    def __init__(self, queryset: 'QuerySetBase[ModelType]') -> None:
        self.queryset = queryset

    @property
    def operation_manager(self) -> OperationManager:
        from amsdal_data.application import DataApplication

        return DataApplication().operation_manager

    @property
    def is_using_lakehouse(self) -> bool:
        from amsdal_data.application import DataApplication

        return self.queryset._using == LAKEHOUSE_DB_ALIAS or DataApplication().is_lakehouse_only

    @abstractmethod
    def query(self) -> list[dict[str, Any]]: ...

    @abstractmethod
    def count(self) -> int: ...


class Executor(ExecutorBase['ModelType']):
    """
    Concrete executor class for executing queries and counting results.

    This class extends the `ExecutorBase` and provides the implementation for
    executing queries and counting results using the specified query set.
    """

    def _address(self) -> Address:
        return Address(
            resource='',
            class_name=self.queryset.entity_name,
            class_version=HistoricalSchemaVersionManager().get_latest_schema_version(self.queryset.entity_name),
            object_id='',
            object_version='',
        )

    def query(self) -> list[dict[str, Any]]:
        """
        Execute the query and return the results.

        This method uses the connection object to execute the query based on the
        query set's specifier, conditions, pagination, and order by attributes.

        Returns:
            list[dict[str, Any]]: The query results as a list of dictionaries.
        """
        _select_related = None
        if isinstance(self.queryset._select_related, dict):
            _select_related = self._process_select_related(self.queryset._select_related, self.queryset._entity)
        # print(self.queryset._conditions)
        query = self._build_query_statement(select_related=_select_related)
        # print(query)

        if self.is_using_lakehouse:
            result = self.operation_manager.query_lakehouse(query)
        else:
            result = self.operation_manager.query(query)

        if not result.success:
            msg = f'Error while executing query: {result.message}'
            raise AmsdalQuerySetError(msg) from result.exception

        return [self._process_data(item.data, _select_related) for item in (result.data or [])]

    def count(self) -> int:
        """
        Execute the query and return the count of results.

        This method uses the connection object to execute the query and return
        the count of model instances that match the query conditions.

        Returns:
            int: The count of matching results.
        """
        query = self._build_query_statement(is_count=True)

        if self.is_using_lakehouse:
            result = self.operation_manager.query_lakehouse(query)
        else:
            result = self.operation_manager.query(query)

        if not result.success:
            msg = 'Error while executing query'
            raise Exception(msg) from result.exception

        return (result.data or [])[0].data['total_count']

    def _process_select_related(
        self,
        select_related: dict[str, Any],
        model: type['ModelType'],
    ) -> dict[tuple[str, Address, str], Any]:
        from amsdal_models.classes.model import LegacyModel
        from amsdal_models.classes.model import Model

        _select_related = {}

        for key, value in select_related.items():
            _field_type = model.model_fields[key].annotation

            if not _field_type or not hasattr(_field_type, '__origin__') or _field_type.__origin__ != Union:
                msg = 'Select related field must be a Union type'
                raise ValueError(msg)

            base_class: type[ModelType] | None = next(
                (arg for arg in _field_type.__args__ if issubclass(arg, Model) and not issubclass(arg, LegacyModel)),
                None,
            )
            if not base_class:
                msg = 'Select related field must be a Model type'
                raise ValueError(msg)

            _related = self._process_select_related(value, base_class)
            for version in HistoricalSchemaVersionManager().get_all_schema_versions(base_class.__name__):
                _select_related[
                    (
                        key,
                        Address(
                            resource='',
                            class_name=base_class.__name__,
                            class_version=version,
                            object_id='',
                            object_version='',
                        ),
                        't' + uuid.uuid4().hex[:8],
                    )
                ] = _related

        return _select_related

    @staticmethod
    def _process_data(
        data: dict[str, Any],
        select_related: dict[tuple[str, Address, str], Any] | None = None,
    ) -> dict[str, Any]:
        if select_related:
            for (field, _, alias), nested_select_related in select_related.items():
                nested_data = {}
                prefix = f'{alias}__'
                for data_field, value in data.items():
                    if data_field.startswith(prefix):
                        nested_data[data_field[len(prefix) :]] = value

                nested_data = Executor._process_data(nested_data, nested_select_related)

                if nested_data and any(v is not None for v in nested_data.values()):
                    data[field] = nested_data

        if PRIMARY_PARTITION_KEY in data:
            data['_object_id'] = data.pop(PRIMARY_PARTITION_KEY)
        if SECONDARY_PARTITION_KEY in data:
            data['_object_version'] = data.pop(SECONDARY_PARTITION_KEY)
        return data

    def _build_query_statement(
        self,
        select_related: dict[tuple[str, Address, str], Any] | None = None,
        *,
        is_count: bool = False,
    ) -> glue.QueryStatement:
        # TODO: add supporting of distinct into glue
        aggregation = None

        _only = self._build_only(select_related)
        if is_count:
            aggregation = glue.AggregationQuery(
                expression=glue.Count(
                    field=glue.FieldReference(
                        field=glue.Field(name='*'),
                        table_name=self.queryset.entity_name,
                    )
                ),
                alias='total_count',
            )
            _only = None

        return glue.QueryStatement(
            only=_only,
            aggregations=[aggregation] if aggregation else None,
            table=glue.SchemaReference(
                name=self.queryset.entity_name,
                version=HistoricalSchemaVersionManager().get_latest_schema_version(self.queryset.entity_name),
            ),
            joins=self._build_joins(self.queryset.entity_name, select_related),
            where=self._build_conditions(self.queryset._conditions),
            order_by=self._build_order_by(),
            limit=self._build_limit(),
        )

    def _build_joins(
        self, parent_alias: str, select_related: dict[tuple[str, Address, str], Any] | None
    ) -> list[glue.JoinQuery] | None:
        if not select_related:
            return None

        _joins = []

        for (field, address, alias), nested_select_related in select_related.items():
            reference_field = glue.Field(name=field)
            ref_field = glue.Field(name='ref', parent=reference_field)
            object_id = glue.Field(name='object_id', parent=ref_field)
            reference_field.child = ref_field
            ref_field.child = object_id
            q = glue.QueryStatement(
                table=glue.SchemaReference(name=address.class_name, version=address.class_version),
                only=self._build_joined_only(address, nested_select_related),
                joins=self._build_joins(address.class_name, nested_select_related),
            )

            _joins.append(
                glue.JoinQuery(
                    table=glue.SubQueryStatement(
                        query=q,
                        alias=alias,
                    ),
                    on=glue.Conditions(
                        glue.Condition(
                            field=glue.FieldReference(
                                field=reference_field,
                                table_name=parent_alias,
                            ),
                            lookup=glue.FieldLookup.EQ,
                            value=glue.FieldReference(
                                field=glue.Field(name=PRIMARY_PARTITION_KEY),
                                table_name=alias,
                            ),
                        )
                    ),
                    join_type=glue.JoinType.LEFT,
                )
            )

        return _joins

    def _build_only(
        self,
        select_related: dict[tuple[str, Address, str], Any] | None,
    ) -> list[glue.FieldReference] | None:
        if self.queryset._query_specifier and self.queryset._query_specifier.only:
            return [
                glue.FieldReference(
                    field=self._build_field(item),
                    table_name=self.queryset.entity_name,
                )
                for item in self.queryset._query_specifier.only
            ]

        if select_related:
            _only = []
            main_schema = TableSchemasManager()._schemas_cache[self.queryset.entity_name.lower()]['LATEST']
            for prop in main_schema.properties:
                _only.append(
                    glue.FieldReference(
                        field=glue.Field(name=prop.name),
                        table_name=self.queryset.entity_name,
                    )
                )

            _only.extend(self._build_nested_only(select_related))

            return _only
        return None

    def _build_joined_only(
        self,
        current_address: Address,
        select_related: dict[tuple[str, Address, str], Any],
    ) -> list[glue.FieldReference]:
        model_schemas = TableSchemasManager()._schemas_cache[current_address.class_name.lower()]
        schema = model_schemas.get(current_address.class_version, model_schemas['LATEST'])

        _only = []

        for prop in schema.properties:
            _only.append(
                glue.FieldReference(
                    field=glue.Field(name=prop.name),
                    table_name=current_address.class_name,
                )
            )

        if select_related:
            _only.extend(self._build_nested_only(select_related))

        return _only

    def _build_nested_only(
        self,
        select_related: dict[tuple[str, Address, str], Any],
    ) -> list[glue.FieldReferenceAliased]:
        _only: list[glue.FieldReferenceAliased] = []

        for (_, address, alias), nested_select_related in select_related.items():
            model_schemas = TableSchemasManager()._schemas_cache[address.class_name.lower()]
            schema = model_schemas.get(address.class_version, model_schemas['LATEST'])
            for prop in schema.properties:
                _only.append(
                    glue.FieldReferenceAliased(
                        field=glue.Field(name=prop.name),
                        table_name=alias,
                        alias=f'{alias}__{prop.name}',
                    )
                )

            if nested_select_related:
                for sub_field in self._build_nested_only(nested_select_related):
                    _only.append(
                        glue.FieldReferenceAliased(
                            field=glue.Field(name=sub_field.alias),
                            table_name=alias,
                            alias=f'{alias}__{sub_field.alias}',
                        )
                    )

        return _only

    def _build_conditions(
        self,
        conditions: Q | None,
        *,
        is_lakehouse: bool = False,  # noqa: ARG002
    ) -> glue.Conditions | None:
        if conditions:
            _conditions: list[glue.Conditions | glue.Condition] = []

            for child in conditions.children:
                if isinstance(child, Q):
                    if _cond := self._build_conditions(child):
                        _conditions.append(_cond)
                else:
                    _value = child.value

                    if isinstance(_value, QueryableMixin):
                        new_q = _value.to_query(prefix=f'{child.field_name}__')

                        if child.lookup == Lookup.NEQ:
                            new_q = ~new_q

                        if _cond := self._build_conditions(new_q):
                            _conditions.append(_cond)
                        continue

                    if '__' in child.field_name:
                        [_field_name, _rest] = child.field_name.split('__', 1)
                    else:
                        [_field_name, _rest] = child.field_name, ''

                    if _field_name == ADDRESS_FIELD and not self.is_using_lakehouse and _rest != OBJECT_ID_FIELD:
                        # Ignore address field in non-lakehouse queries
                        continue

                    if _field_name == ADDRESS_FIELD and _rest in (OBJECT_ID_FIELD, OBJECT_VERSION_FIELD):
                        if _rest == OBJECT_ID_FIELD:
                            _field = glue.Field(name=PRIMARY_PARTITION_KEY)
                        else:
                            _field = glue.Field(name=SECONDARY_PARTITION_KEY)

                            if _value in (glue.Version.LATEST, Versions.LATEST, '', 'LATEST'):
                                _conditions.append(
                                    glue.Conditions(
                                        glue.Condition(
                                            field=glue.FieldReference(
                                                field=glue.Field(name=NEXT_VERSION_FIELD),
                                                table_name=METADATA_TABLE_ALIAS,
                                            ),
                                            lookup=glue.FieldLookup.ISNULL,
                                            value=glue.Value(value=True),
                                        ),
                                        glue.Condition(
                                            field=glue.FieldReference(
                                                field=glue.Field(name=NEXT_VERSION_FIELD),
                                                table_name=METADATA_TABLE_ALIAS,
                                            ),
                                            lookup=glue.FieldLookup.EQ,
                                            value=glue.Value(value=''),
                                        ),
                                        connector=glue.FilterConnector.OR,
                                    ),
                                )
                                continue
                            elif _value in (glue.Version.ALL, Versions.ALL, 'ALL'):
                                _conditions.append(
                                    glue.Condition(
                                        field=glue.FieldReference(
                                            field=_field,
                                            table_name=self.queryset.entity_name,
                                        ),
                                        lookup=glue.FieldLookup.NEQ,
                                        value=glue.Value('_empty-'),
                                    )
                                )
                                continue
                    else:
                        _field = self._build_field(child.field_name)

                    _conditions.append(
                        glue.Condition(
                            field=glue.FieldReference(
                                field=_field,
                                table_name=self.queryset.entity_name,
                            ),
                            lookup=self._to_glue_lookup(child.lookup),
                            value=glue.Value(value=_value),
                        ),
                    )

            return glue.Conditions(
                *_conditions,
                connector=(
                    {
                        ConnectorEnum.AND: glue.FilterConnector.AND,
                        ConnectorEnum.OR: glue.FilterConnector.OR,
                    }
                )[conditions.connector],
                negated=conditions.negated,
            )

        return None

    @staticmethod
    def _build_field(field_name: str) -> glue.Field:
        if '__' in field_name:
            _parent_name, *_rest_names = field_name.split('__')
            field = glue.Field(name=_parent_name)
            _root = field

            for _name in _rest_names:
                _child = glue.Field(name=_name, parent=_root)
                _root.child = _child
                _root = _child
        else:
            field = glue.Field(name=field_name)
        return field

    def _build_order_by(self) -> list[glue.OrderByQuery] | None:
        if self.queryset._order_by:
            return [
                glue.OrderByQuery(
                    field=glue.FieldReference(
                        field=self._build_field(item.field_name),
                        table_name=self.queryset.entity_name,
                    ),
                    direction=(
                        {
                            OrderDirection.ASC: glue.OrderDirection.ASC,
                            OrderDirection.DESC: glue.OrderDirection.DESC,
                        }
                    )[item.direction],
                )
                for item in self.queryset._order_by
            ]

        return None

    def _build_limit(self) -> glue.LimitQuery | None:
        if self.queryset._paginator:
            if isinstance(self.queryset._paginator, NumberPaginator):
                return glue.LimitQuery(
                    limit=self.queryset._paginator.limit or 0,
                    offset=self.queryset._paginator.offset or 0,
                )

            if isinstance(self.queryset._paginator, CursorPaginator):
                msg = 'CursorPaginator is not supported in glue'
                raise NotImplementedError(msg)

        return None

    @staticmethod
    def _to_glue_lookup(lookup: Lookup) -> glue.FieldLookup:
        return (
            {
                Lookup.EQ: glue.FieldLookup.EQ,
                Lookup.NEQ: glue.FieldLookup.NEQ,
                Lookup.GT: glue.FieldLookup.GT,
                Lookup.GTE: glue.FieldLookup.GTE,
                Lookup.LT: glue.FieldLookup.LT,
                Lookup.LTE: glue.FieldLookup.LTE,
                Lookup.IN: glue.FieldLookup.IN,
                Lookup.CONTAINS: glue.FieldLookup.CONTAINS,
                Lookup.ICONTAINS: glue.FieldLookup.ICONTAINS,
                Lookup.STARTSWITH: glue.FieldLookup.STARTSWITH,
                Lookup.ISTARTSWITH: glue.FieldLookup.ISTARTSWITH,
                Lookup.ENDSWITH: glue.FieldLookup.ENDSWITH,
                Lookup.IENDSWITH: glue.FieldLookup.IENDSWITH,
                Lookup.ISNULL: glue.FieldLookup.ISNULL,
                Lookup.REGEX: glue.FieldLookup.REGEX,
                Lookup.IREGEX: glue.FieldLookup.IREGEX,
            }
        )[lookup]
