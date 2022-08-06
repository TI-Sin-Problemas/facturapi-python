"""Invoice relation codes"""

from typing import NamedTuple


class InvoiceRelation(NamedTuple):
    """Invoice relation codes"""

    NOTA_DE_CREDITO = "01"
    NOTA_DE_DEBITO = "02"
    DEVOLUCION = "03"
    SUSTITUCION = "04"
    TRASLADOS = "05"
    FACTURA_POR_TRASLADOS = "06"
    CDFI_POR_ANTICIPO = "07"
    FACTURA_POR_PARCIALIDADES = "08"
    FACTURA_POR_DIFERIDOS = "09"
