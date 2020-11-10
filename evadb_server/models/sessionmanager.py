from ..helper import generate_unique_id

from loguru import logger


class SessionManager:
    """Create and manage evaDB sessions against the request interface of evaDB."""

    def __init__(self):
        self._sessions = {}

    def add(self, session_cookie: str, session):
        """Add a session with cookie as key."""
        # TODO: maybe store session ids instead of a whole requests session
        logger.debug("Adding session for {}", session_cookie)
        self._sessions[session_cookie] = session

    def get(self, session_cookie: str) -> "Union[EvaDBUser, Any]":
        """Get a evaDB user Instance using a session cookie."""
        session = self._sessions.get(session_cookie)
        if session is None:
            logger.debug("Failed to find session for {}", session_cookie)
        return session

    def delete(self, session_cookie: str) -> "Union[EvaDBUser, Any]":
        """Test"""
        if session_cookie in self._sessions:
            del self._sessions[session_cookie]
        else:
            logger.debug("Could not find session for {}", session_cookie)

    @staticmethod
    def generate_session_id() -> str:
        """Generate a session id."""
        return generate_unique_id()
