"""Herramientas para el perfilado de clientes con problemas de deuda."""

import json
from datetime import datetime
from typing import Optional

from langchain.tools import tool

# Almacenamiento temporal en memoria (para MVP)
# En produccion esto se conectaria a una base de datos
client_profiles: dict = {}


@tool
def save_client_data(
    client_name: str,
    debt_type: Optional[str] = None,
    total_debt_amount: Optional[str] = None,
    has_embargo: Optional[bool] = None,
    monthly_income: Optional[str] = None,
    marital_status: Optional[str] = None,
    num_children: Optional[int] = None,
    monthly_rent: Optional[str] = None,
    monthly_utilities: Optional[str] = None,
) -> str:
    """Guarda los datos del cliente recopilados durante la llamada.

    Usa esta herramienta para guardar informacion del cliente a medida que la recopilas.
    Puedes llamarla multiples veces para ir actualizando los datos.

    Args:
        client_name: Nombre del cliente (obligatorio en la primera llamada)
        debt_type: Tipo de deuda (hipoteca, tarjetas, prestamos, etc.)
        total_debt_amount: Cantidad total de deuda aproximada (ej: "quince mil euros")
        has_embargo: Si tiene embargos activos o notificaciones
        monthly_income: Ingresos mensuales aproximados (ej: "mil doscientos euros")
        marital_status: Estado civil (soltero, casado, divorciado, viudo)
        num_children: Numero de hijos
        monthly_rent: Gasto mensual en alquiler o hipoteca
        monthly_utilities: Gasto mensual en suministros (agua, luz, gas)

    Returns:
        Confirmacion de que los datos han sido guardados
    """
    profile_id = client_name.lower().replace(" ", "_")

    if profile_id not in client_profiles:
        client_profiles[profile_id] = {
            "client_name": client_name,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
        }

    profile = client_profiles[profile_id]

    # Actualizar solo los campos proporcionados
    if debt_type is not None:
        profile["debt_type"] = debt_type
    if total_debt_amount is not None:
        profile["total_debt_amount"] = total_debt_amount
    if has_embargo is not None:
        profile["has_embargo"] = has_embargo
    if monthly_income is not None:
        profile["monthly_income"] = monthly_income
    if marital_status is not None:
        profile["marital_status"] = marital_status
    if num_children is not None:
        profile["num_children"] = num_children
    if monthly_rent is not None:
        profile["monthly_rent"] = monthly_rent
    if monthly_utilities is not None:
        profile["monthly_utilities"] = monthly_utilities

    profile["updated_at"] = datetime.now().isoformat()

    return f"Datos de {client_name} guardados correctamente."


@tool
def get_client_summary(client_name: str) -> str:
    """Obtiene un resumen de los datos recopilados del cliente.

    Usa esta herramienta para revisar que datos ya tienes del cliente
    antes de continuar con las preguntas.

    Args:
        client_name: Nombre del cliente

    Returns:
        Resumen de los datos recopilados o mensaje si no hay datos
    """
    profile_id = client_name.lower().replace(" ", "_")

    if profile_id not in client_profiles:
        return f"No hay datos guardados para {client_name}."

    profile = client_profiles[profile_id]
    summary_parts = [f"Datos de {profile.get('client_name', client_name)}:"]

    if profile.get("debt_type"):
        summary_parts.append(f"Tipo de deuda: {profile['debt_type']}")
    if profile.get("total_debt_amount"):
        summary_parts.append(f"Deuda total: {profile['total_debt_amount']}")
    if profile.get("has_embargo") is not None:
        embargo_text = "Si" if profile["has_embargo"] else "No"
        summary_parts.append(f"Embargos: {embargo_text}")
    if profile.get("monthly_income"):
        summary_parts.append(f"Ingresos: {profile['monthly_income']}")
    if profile.get("marital_status"):
        summary_parts.append(f"Estado civil: {profile['marital_status']}")
    if profile.get("num_children") is not None:
        summary_parts.append(f"Hijos: {profile['num_children']}")
    if profile.get("monthly_rent"):
        summary_parts.append(f"Alquiler/hipoteca: {profile['monthly_rent']}")
    if profile.get("monthly_utilities"):
        summary_parts.append(f"Suministros: {profile['monthly_utilities']}")

    if len(summary_parts) == 1:
        return f"Solo tenemos el nombre: {client_name}. Faltan datos por recopilar."

    return " | ".join(summary_parts)


@tool
def finalize_profile(client_name: str, wants_callback: bool = True) -> str:
    """Finaliza el perfilado del cliente y marca como listo para seguimiento.

    Usa esta herramienta cuando hayas recopilado toda la informacion necesaria
    y el cliente haya confirmado que quiere ser contactado por un asesor.

    Args:
        client_name: Nombre del cliente
        wants_callback: Si el cliente quiere que le llame un asesor

    Returns:
        Confirmacion del estado del perfil
    """
    profile_id = client_name.lower().replace(" ", "_")

    if profile_id not in client_profiles:
        return f"No hay datos guardados para {client_name}."

    profile = client_profiles[profile_id]
    profile["status"] = "ready_for_callback" if wants_callback else "completed_no_callback"
    profile["finalized_at"] = datetime.now().isoformat()
    profile["wants_callback"] = wants_callback

    if wants_callback:
        return f"Perfecto. El perfil de {client_name} esta listo. Un asesor le contactara pronto."
    else:
        return f"Entendido. Hemos guardado la informacion de {client_name} por si necesita ayuda en el futuro."
