from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.entity_link_form_field_entity_type import EntityLinkFormFieldEntityType
from ..models.entity_link_form_field_type import EntityLinkFormFieldType
from ..types import UNSET, Unset

T = TypeVar("T", bound="EntityLinkFormField")


@attr.s(auto_attribs=True, repr=False)
class EntityLinkFormField:
    """  """

    _entity_type: Union[Unset, EntityLinkFormFieldEntityType] = UNSET
    _schema_id: Union[Unset, str] = UNSET
    _type: Union[Unset, EntityLinkFormFieldType] = UNSET
    _description: Union[Unset, str] = UNSET
    _is_required: Union[Unset, bool] = UNSET
    _key: Union[Unset, str] = UNSET
    _label: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("entity_type={}".format(repr(self._entity_type)))
        fields.append("schema_id={}".format(repr(self._schema_id)))
        fields.append("type={}".format(repr(self._type)))
        fields.append("description={}".format(repr(self._description)))
        fields.append("is_required={}".format(repr(self._is_required)))
        fields.append("key={}".format(repr(self._key)))
        fields.append("label={}".format(repr(self._label)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "EntityLinkFormField({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        entity_type: Union[Unset, int] = UNSET
        if not isinstance(self._entity_type, Unset):
            entity_type = self._entity_type.value

        schema_id = self._schema_id
        type: Union[Unset, int] = UNSET
        if not isinstance(self._type, Unset):
            type = self._type.value

        description = self._description
        is_required = self._is_required
        key = self._key
        label = self._label

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if entity_type is not UNSET:
            field_dict["entityType"] = entity_type
        if schema_id is not UNSET:
            field_dict["schemaId"] = schema_id
        if type is not UNSET:
            field_dict["type"] = type
        if description is not UNSET:
            field_dict["description"] = description
        if is_required is not UNSET:
            field_dict["isRequired"] = is_required
        if key is not UNSET:
            field_dict["key"] = key
        if label is not UNSET:
            field_dict["label"] = label

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_entity_type() -> Union[Unset, EntityLinkFormFieldEntityType]:
            entity_type = UNSET
            _entity_type = d.pop("entityType")
            if _entity_type is not None and _entity_type is not UNSET:
                try:
                    entity_type = EntityLinkFormFieldEntityType(_entity_type)
                except ValueError:
                    entity_type = EntityLinkFormFieldEntityType.of_unknown(_entity_type)

            return entity_type

        try:
            entity_type = get_entity_type()
        except KeyError:
            if strict:
                raise
            entity_type = cast(Union[Unset, EntityLinkFormFieldEntityType], UNSET)

        def get_schema_id() -> Union[Unset, str]:
            schema_id = d.pop("schemaId")
            return schema_id

        try:
            schema_id = get_schema_id()
        except KeyError:
            if strict:
                raise
            schema_id = cast(Union[Unset, str], UNSET)

        def get_type() -> Union[Unset, EntityLinkFormFieldType]:
            type = UNSET
            _type = d.pop("type")
            if _type is not None and _type is not UNSET:
                try:
                    type = EntityLinkFormFieldType(_type)
                except ValueError:
                    type = EntityLinkFormFieldType.of_unknown(_type)

            return type

        try:
            type = get_type()
        except KeyError:
            if strict:
                raise
            type = cast(Union[Unset, EntityLinkFormFieldType], UNSET)

        def get_description() -> Union[Unset, str]:
            description = d.pop("description")
            return description

        try:
            description = get_description()
        except KeyError:
            if strict:
                raise
            description = cast(Union[Unset, str], UNSET)

        def get_is_required() -> Union[Unset, bool]:
            is_required = d.pop("isRequired")
            return is_required

        try:
            is_required = get_is_required()
        except KeyError:
            if strict:
                raise
            is_required = cast(Union[Unset, bool], UNSET)

        def get_key() -> Union[Unset, str]:
            key = d.pop("key")
            return key

        try:
            key = get_key()
        except KeyError:
            if strict:
                raise
            key = cast(Union[Unset, str], UNSET)

        def get_label() -> Union[Unset, str]:
            label = d.pop("label")
            return label

        try:
            label = get_label()
        except KeyError:
            if strict:
                raise
            label = cast(Union[Unset, str], UNSET)

        entity_link_form_field = cls(
            entity_type=entity_type,
            schema_id=schema_id,
            type=type,
            description=description,
            is_required=is_required,
            key=key,
            label=label,
        )

        entity_link_form_field.additional_properties = d
        return entity_link_form_field

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties

    def get(self, key, default=None) -> Optional[Any]:
        return self.additional_properties.get(key, default)

    @property
    def entity_type(self) -> EntityLinkFormFieldEntityType:
        """ Benchling entity type of this link. Currently only custom_entity is supported """
        if isinstance(self._entity_type, Unset):
            raise NotPresentError(self, "entity_type")
        return self._entity_type

    @entity_type.setter
    def entity_type(self, value: EntityLinkFormFieldEntityType) -> None:
        self._entity_type = value

    @entity_type.deleter
    def entity_type(self) -> None:
        self._entity_type = UNSET

    @property
    def schema_id(self) -> str:
        """ Schema ID of the entity in question """
        if isinstance(self._schema_id, Unset):
            raise NotPresentError(self, "schema_id")
        return self._schema_id

    @schema_id.setter
    def schema_id(self, value: str) -> None:
        self._schema_id = value

    @schema_id.deleter
    def schema_id(self) -> None:
        self._schema_id = UNSET

    @property
    def type(self) -> EntityLinkFormFieldType:
        """The type of this form field. Type declares how this field behaves and dictates the additional properties passed along with the required properties like label and key"""
        if isinstance(self._type, Unset):
            raise NotPresentError(self, "type")
        return self._type

    @type.setter
    def type(self, value: EntityLinkFormFieldType) -> None:
        self._type = value

    @type.deleter
    def type(self) -> None:
        self._type = UNSET

    @property
    def description(self) -> str:
        """ Description of the purpose of this field """
        if isinstance(self._description, Unset):
            raise NotPresentError(self, "description")
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        self._description = value

    @description.deleter
    def description(self) -> None:
        self._description = UNSET

    @property
    def is_required(self) -> bool:
        """ Whether this field is required to be filled out in order to be a valid submission """
        if isinstance(self._is_required, Unset):
            raise NotPresentError(self, "is_required")
        return self._is_required

    @is_required.setter
    def is_required(self, value: bool) -> None:
        self._is_required = value

    @is_required.deleter
    def is_required(self) -> None:
        self._is_required = UNSET

    @property
    def key(self) -> str:
        """ Reference key of this form field. Used to fix identity of fields beyond the label """
        if isinstance(self._key, Unset):
            raise NotPresentError(self, "key")
        return self._key

    @key.setter
    def key(self, value: str) -> None:
        self._key = value

    @key.deleter
    def key(self) -> None:
        self._key = UNSET

    @property
    def label(self) -> str:
        """ End user facing name of this form field. What you see when you fill out the form each time """
        if isinstance(self._label, Unset):
            raise NotPresentError(self, "label")
        return self._label

    @label.setter
    def label(self, value: str) -> None:
        self._label = value

    @label.deleter
    def label(self) -> None:
        self._label = UNSET
