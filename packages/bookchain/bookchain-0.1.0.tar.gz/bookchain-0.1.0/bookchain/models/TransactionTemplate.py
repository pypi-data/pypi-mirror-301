from sqloquent import HashedModel
import packify

class TransactionTemplate(HashedModel):
    connection_info: str = ''
    table: str = 'transaction_templates'
    id_column: str = 'id'
    columns: tuple[str] = (
        'id', 'fields', 'template'
    )
    id: str
    fields: bytes
    template: str

    # override automatic property
    @property
    def fields(self) -> dict[str, str]:
        return {
            k: v
            for k, v in
            packify.unpack(
                self.data.get('fields', None) or b'd\x00\x00\x00\x00'
            ).items()
        }
    @fields.setter
    def fields(self, vals: dict[str, str]):
        if type(vals) is dict and all([type(k) is str for k, _ in vals.items()]) \
            and all([type(v) is str for _, v in vals.items()]):
            self.data['fields'] = packify.pack(vals)

    def compile(self, models: list = [], data: dict = {}) -> bytes:
        """Attempt to compile a message using the fields, template,
            models, and data. Raises TypeError if any data is missing or
            is the wrong type.
        """
        for fld, tp in self.fields.items():
            ...
