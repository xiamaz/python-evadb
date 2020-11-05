import json
from functools import wraps
from flask import Blueprint, jsonify, request


from evadb_server.models.sessionmanager import SessionManager
from evadb_server.models.patient import legacy_sample_to_patient, legacy_hpo_to_symptom

from ..base import jsonrpc
from ..session import has_session


# TODO: check if logged out! on calls, makes long-running session less painful
app = Blueprint("next", __name__)


@jsonrpc(app, "/")
def status(_):
    """Check if online."""
    return {"status": "ok"}


@jsonrpc(app, "/getPatient")
@has_session
def getPatient(session, query):
    """Get a single sample by id

    query: { id }
    """
    patient_id = query["id"]

    samples = session.search_sample({})
    if samples.error:
        return {"error": samples.error, "data": None}

    patients = [legacy_sample_to_patient(s) for s in samples.data]

    patient = None
    for candidate in patients:
        if candidate.id == patient_id:
            patient = candidate
            break
    else:
        return {"error": f"Patient with ID {patient_id} not found", "data": None}

    hpo_result = session.show_hpo(patient_id)
    if hpo_result.error:
        return {"error": f"Failed to query HPO with {hpo_result.error}", "data": None}

    patient.symptoms = [legacy_hpo_to_symptom(h) for h in hpo_result.data]

    patient_json = patient.to_dict()
    return {"error": None, "data": patient_json}
