import json

import redis
from loguru import logger

import dramatiq

import evadb
from .models.patient import legacy_sample_to_patient
from .config import CUSTOM_HOST

R = redis.Redis("localhost")


def getPatient(session, patient_id):
    samples = session.search_sample({})
    if samples.error:
        raise RuntimeError(samples.error)

    patients = [legacy_sample_to_patient(s) for s in samples.data]
    patient = None
    for candidate in patients:
        if candidate.id == patient_id:
            patient = candidate
            break
    else:
        raise RuntimeError(f"No patient with ID {patient_id} found.")

    return patient


def queryAD(session, params, patient):
    params["s.pedigree"] = patient.pedigree_id
    result = session.search_ad(params)
    return {"error": result.error, "data": result.data}


def queryAR(session, params, patient):
    params["s.name"] = patient.samples[0].id
    result = session.search_ar(params)
    return {"error": result.error, "data": result.data}


@dramatiq.actor(max_retries=0)
def runQuery(user_id, query_id, query_data, session_id):
    # store query into redis
    R.lpush(f"{user_id}-queries", query_id)
    R.set(query_id, json.dumps(query_data))

    eva = evadb.EvaDBUser(CUSTOM_HOST)
    eva.set_session(session_id)
    eva.check_session()

    patient_id = query_data["patientId"]

    # get additional patient information
    patient = getPatient(eva, patient_id)

    # iteratively call all queries
    results = []
    for query in query_data["data"]:
        qtype = query["type"]
        qparams = query["data"]

        if qtype == "AD Variants":
            result = queryAD(eva, qparams, patient)
        elif qtype == "AR Variants":
            result = queryAR(eva, qparams, patient)
        else:
            raise RuntimeError(f"Unknown query type {qtype}")

        results.append(result)

    R.set(f"{query_id}-result", json.dumps(results))
    print(results)
