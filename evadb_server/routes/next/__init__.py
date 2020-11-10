import json
from functools import wraps
from flask import Blueprint, jsonify, request
from requests.utils import dict_from_cookiejar
from loguru import logger

import redis

from evadb_server.models.sessionmanager import SessionManager
from evadb_server.models.patient import legacy_sample_to_patient, legacy_hpo_to_symptom

from ..base import jsonrpc
from ..session import has_session, get_session_id
from ... import worker
from ...helper import generate_unique_id


# TODO: check if logged out! on calls, makes long-running session less painful
app = Blueprint("next", __name__)
R = redis.Redis("localhost")


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


@jsonrpc(app, "/query/submit")
@has_session
def submitQuery(session, query):
    """Run a query with the given parameters and store the returned results.
    """
    query_id = generate_unique_id()
    user_id = get_session_id()
    eva_session_id = session.get_session()
    worker.runQuery.send(user_id, query_id, query, eva_session_id)
    return {"error": None, "data": {"id": query_id}}


@jsonrpc(app, "/query/fetch")
@has_session
def fetchQuery(session, query):
    """Fetch the query with the given ID.
    """
    query_id = query["id"]

    session_id = get_session_id()
    query_ids_key = f"{session_id}-queries"
    rquery_ids = R.lrange(query_ids_key, 0, -1)
    query_ids = [q.decode() for q in rquery_ids]
    if query_id not in query_ids:
        return {"error": "Unauthorized", "data": None}

    rquery_result = R.get(f"{query_id}-result")
    if not rquery_result:
        return {"error": f"No data found for {query_id}", "data": None}
    query_result = json.loads(rquery_result)

    rquery_info = R.get(query_id)
    query_info = json.loads(rquery_info)

    resp_data = {"info": query_info, "data": query_result}
    return {"error": None, "data": resp_data}


@jsonrpc(app, "/query/all")
@has_session
def allQuery(session, query):
    """Get a summarized lists of all queries."""
    session_id = get_session_id()
    query_ids_key = f"{session_id}-queries"
    query_ids = R.lrange(query_ids_key, 0, -1)
    logger.info("Redis ({}) -> ({})", query_ids_key, query_ids)

    if query_ids is None:
        query_ids = []

    results = []
    for rquery_id in query_ids:
        query_id = rquery_id.decode()
        rquery_result = R.get(query_id)
        logger.info("Redis ({}) -> ({})", query_id, rquery_result)
        if rquery_result:
            query_result = json.loads(rquery_result)
            results_exist = R.exists(f"{query_id}-result")
            results.append({"id": query_id, "data": query_result, "resultsExist": results_exist})
    return {"error": None, "data": results}
