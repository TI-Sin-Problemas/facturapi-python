"""Enum constants"""

from enum import Enum
from typing import NamedTuple


class PaymentForm(Enum):
    """SAT's payment form codes"""

    EFECTIVO = "01"
    CHEQUE_NOMINATIVO = "02"
    TRANSFERENCIA_ELECTRONICA_DE_FONDOS = "03"
    TARJETA_DE_CREDITO = "04"
    MONEDERO_ELECTRONICO = "05"
    DINERO_ELECTRONICO = "06"
    VALES_DE_DESPENSA = "08"
    DACION_EN_PAGO = "12"
    PAGO_POR_SUBROGACION = "13"
    PAGO_POR_CONSIGNACION = "14"
    CONDONACION = "15"
    COMPENSACION = "17"
    NOVACION = "23"
    CONFUSION = "24"
    REMISION_DE_DEUDA = "25"
    PRESCRIPCION_O_CADUCIDAD = "26"
    A_SATISFACCION_DEL_ACREEDOR = "27"
    TARJETA_DE_DEBITO = "28"
    TARJETA_DE_SERVICIOS = "29"
    APLICACION_DE_ANTICIPOS = "30"
    INTERMEDIARIO_PAGOS = "31"
    POR_DEFINIR = "99"


class PaymentMethod(Enum):
    """SAT's payment method"""

    UNA_SOLA_EXHIBICION = "PUE"
    PARCIALIDADES_DIFERIDO = "PPD"


class InvoiceUse(Enum):
    """SAT's CFDI usage"""

    ADQUISICION_MERCANCIAS = "G01"
    DEVOLUCIONES_DESCUENTOS_BONIFICACIONES = "G02"
    GASTOS_EN_GENERAL = "G03"
    CONSTRUCCIONES = "I01"
    MOBILIARIO_Y_EQUIPO_DE_OFICINA = "I02"
    EQUIPO_DE_TRANSPORTE = "I03"
    EQUIPO_DE_COMPUTO = "I04"
    DADOS_TROQUELES_HERRAMENTAL = "I05"
    COMUNICACIONES_TELEFONICAS = "I06"
    COMUNICACIONES_SATELITALES = "I07"
    OTRA_MAQUINARIA = "I08"
    HONORARIOS_MEDICOS = "D01"
    GASTOS_MEDICOS_POR_INCAPACIDAD = "D02"
    GASTOS_FUNERALES = "D03"
    DONATIVOS = "D04"
    INTERESES_POR_CREDITOS_HIPOTECARIOS = "D05"
    APORTACIONES_VOLUNTARIAS_SAR = "D06"
    PRIMA_SEGUROS_GASTOS_MEDICOS = "D07"
    GASTOS_TRANSPORTACION_ESCOLAR = "D08"
    CUENTAS_AHORRO_PENSIONES = "D09"
    SERVICIOS_EDUCATIVOS = "D10"
    SIN_EFECTOS_FISCALES = "S01"
    PAGOS = "CP01"
    NOMINA = "CN01"


class CancellationReason(Enum):
    ERRORS_WITH_RELATION = "01"
    ERRORS_WITHOUT_RELATION = "02"
    OPERATION_NOT_CARRIED_OUT = "03"
    NOMINATIVE_TRANSACTION = "04"


class ReceiptPeriodicity(Enum):
    DAY = "day"
    WEEK = "week"
    FORTNIGHT = "fortnight"
    MONTH = "month"
    TWO_MONTHS = "two_months"


class Catalogs(NamedTuple):
    payment_forms = PaymentForm
    payment_methods = PaymentMethod
    invoice_use = InvoiceUse
    cancellation_reasons = CancellationReason

    receipt_periodicity = ReceiptPeriodicity
