import pytest
from risk_query.sql.validator import SqlValidator, SqlValidationError

def test_rejects_mutation():
    with pytest.raises(SqlValidationError):
        SqlValidator().validate("DELETE FROM FACT_EXPOSURE")
