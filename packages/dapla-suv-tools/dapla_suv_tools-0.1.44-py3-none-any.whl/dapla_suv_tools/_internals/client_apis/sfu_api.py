import json
import os
from typing import Optional

from dapla_suv_tools._internals.integration.api_client import SuvApiClient
from dapla_suv_tools._internals.util.decorators import result_to_dict
from dapla_suv_tools._internals.util.operation_result import OperationResult
from dapla_suv_tools._internals.util import constants
from dapla_suv_tools._internals.util.suv_operation_context import SuvOperationContext
from dapla_suv_tools._internals.util.validators import (
    ra_nummer_validator,
    delreg_id_validator,
)


END_USER_API_BASE_URL = os.getenv("SUV_END_USER_API_URL", "")

client = SuvApiClient(base_url=END_USER_API_BASE_URL)


@result_to_dict
@SuvOperationContext(validator=ra_nummer_validator)
def get_utvalg_from_sfu(
    self,
    *,
    delreg_nr: int,
    ra_nummer: str,
    pulje: Optional[str] = "",
    context: SuvOperationContext,
) -> OperationResult:
    """
    Attempts to get all skjema with the supplied RA-number.

    Parameters:
    ------------
    delreg_nr: int, required
        The delreg number of the selection.
    ra_nummer: str, required
        Skjema's RA-number, e.g. 'RA-1234'.
    pulje: int, optional
        Limit the selection by pulje.
    context: SuvOperationContext
        Operation context.  This is injected by the underlying pipeline.  Adding a custom context will result in an error.

    Returns:
    --------
    dict:
        A list of skjema json objects matching the RA-number

    Example:
    --------
    get_skjema_by_ra_nummer(ra_nummer="123456789", versjon=1, max_results=0, latest_only=False, pagination_info=None)

    """

    model = {
        "delreg_nr": delreg_nr,
        "ra_number": ra_nummer,
        "pulje": pulje,
    }

    try:
        content: str = client.post(
            path=f"{constants.SFU_PATH}/utvalg",
            body_json=json.dumps(model),
            context=context,
        )
        content_json = json.loads(content)
        context.log(message=f"Fetched selection for delreg_nr'{delreg_nr}'")

        return OperationResult(value=content_json, log=context.logs())
    except Exception as e:
        context.set_error(f"Failed to fetch for delreg_nr {delreg_nr}", e)

        return OperationResult(
            success=False, value=context.errors(), log=context.logs()
        )


@result_to_dict
@SuvOperationContext(validator=delreg_id_validator)
def get_enhet_from_sfu(
    self,
    *,
    delreg_nr: int,
    orgnr: str,
    context: SuvOperationContext,
) -> OperationResult:
    """
    Get unit from SFU.

    Parameters:
    ------------
    delreg_nr: int, required
        The delreg number of the selection.
    orgnr: str, required
        The organization number of the unit.
    context: SuvOperationContext
        Operation context.  This is injected by the underlying pipeline.  Adding a custom context will result in an error.

    Returns:
    --------
    dict:
        An object matching the organization number

    Example:
    --------
    get_enhet_from_sfu(delreg_nr="123456789", orgnr="123456789")

    """

    data = {
        "delreg_nr": delreg_nr,
        "orgnr": orgnr,
    }

    print(data)

    try:
        content: str = client.post(
            path=f"{constants.SFU_PATH}/enhet",
            body_json=json.dumps(data),
            context=context,
        )
        content_json = json.loads(content)
        context.log(message=f"Fetched org for delreg_nr'{delreg_nr}'")

        return OperationResult(value=content_json, log=context.logs())
    except Exception as e:
        context.set_error(f"Failed to fetch org for delreg_nr {delreg_nr}", e)

        return OperationResult(
            success=False, value=context.errors(), log=context.logs()
        )
