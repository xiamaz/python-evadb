from flask import Blueprint

from ..base import jsonrpc
from ..session import has_session


app = Blueprint("legacy", __name__)


@jsonrpc(app, "/")
def status(_):
    """Quickly check the health of the server. To be extended."""
    return {"status": "ok"}


@jsonrpc(app, "/samples")
@has_session
def samples(session, data):
    """Search samples."""
    result = session.search_sample(data)
    return {"error": result.error, "data": result.data}



@jsonrpc(app, "/search-ad")
@has_session
def search_ad(session, data):
    """Search autosomal dominant variants."""
    result = session.search_ad(data)
    return {"error": result.error, "data": result.data}


@jsonrpc(app, "/search-ar")
@has_session
def search_ar(session, data):
    """Search autosomal recessive variants."""
    result = session.search_ar(data)
    return {"error": result.error, "data": result.data}
