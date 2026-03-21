import pytest

from app.domain.accounts.enums import AccountPlan
from app.shared.exceptions import QuotaExceededError
from app.shared.quota import QuotaService


def test_free_plan_estate_limit():
    with pytest.raises(QuotaExceededError):
        QuotaService.check(AccountPlan.FREE, 'estates', 1)


def test_pro_plan_estate_limit():
    with pytest.raises(QuotaExceededError):
        QuotaService.check(AccountPlan.PRO, 'estates', 5)


def test_enterprise_plan_no_limit():
    # não deve levantar exceção
    QuotaService.check(AccountPlan.ENTERPRISE, 'estates', 1000)


def test_free_plan_within_limit():
    # não deve levantar exceção
    QuotaService.check(AccountPlan.FREE, 'estates', 0)
