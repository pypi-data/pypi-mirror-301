"""
Status enums for persona_integration.
"""


class VerificationAttemptStatus:
    """This class describes valid statuses for a verification attempt to be in."""

    # This is the initial state of a verification attempt, after a learner has requested to complete IDV.
    initialized = "initialized"

    # A webhook was received that confirms that an inquiry has been created in Persona.
    created = "created"

    # A verification attempt is pending when it has been started but has not yet been completed.
    pending = "pending"

    # A verification attempt is expired when it is has not been completed in a pre-configured amount of time.
    expired = "expired"

    # A verification attempt is approved when it has been manually approved or approved via a Persona workflow.
    approved = "approved"

    # A verification attempt is declined when it has been manually declined or declined via a Persona workflow.
    declined = "declined"

    all_statuses = [initialized, created, pending, expired, approved, declined]

    @classmethod
    def is_valid_status(cls, status):
        """
        Return whether a verification attempt status is valid.

        Arguments:
            * status (str): the attempt status

        Returns:
            * True if the status is valid; else, False
        """
        return status in cls.all_statuses

    @classmethod
    def is_valid_status_transition(cls, from_status, to_status):
        """
        Return whether a verification attempt status transition is valid.

        Arguments:
            * from_status (str): the current verification attempt status
            * to_status (str): the new verification attempt status

        Returns:
            * True if the status transition is valid; else, False
        """
        if from_status == cls.initialized:
            return to_status in set([cls.created, cls.pending, cls.expired, cls.approved, cls.declined])
        if from_status == cls.created:
            return to_status in set([cls.pending, cls.expired, cls.approved, cls.declined])
        elif from_status == cls.pending:
            return to_status in set([cls.expired, cls.approved, cls.declined])
        else:
            # No status transitions are allowed from the terminal states expired, approved, and declined.
            return False
