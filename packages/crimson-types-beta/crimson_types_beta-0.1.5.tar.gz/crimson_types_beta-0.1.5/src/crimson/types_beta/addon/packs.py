from crimson.types_beta.addon.intelli_type import IntelliHolder, T
from crimson.types_beta.addon.pydantic import PydanticCompatible
from crimson.types_beta.addon.annotated import annotated_type


@annotated_type
class TypesPack(PydanticCompatible, IntelliHolder[T]):
    """
    If you want to use the __metadata__, this must be the first base of your custom type.

    Go to docs(examples): [Link](https://github.com/crimson206/types/blob/main/example/addon/packs.ipynb)
    """

    # validate_base_index = 1
