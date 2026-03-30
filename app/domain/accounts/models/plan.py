from dataclasses import dataclass

from app.domain.accounts.enums import AccountPlan


@dataclass(frozen=True)
class PlanQuota:
    max_users: int
    max_estates: int
    max_fields_per_estate: int
    max_activities_per_field: int | None  # None = no limit


PLAN_QUOTAS: dict[AccountPlan, PlanQuota] = {
    AccountPlan.FREE: PlanQuota(
        max_users=3,
        max_estates=1,
        max_fields_per_estate=4,
        max_activities_per_field=2,
    ),
    AccountPlan.PRO: PlanQuota(
        max_users=5,
        max_estates=5,
        max_fields_per_estate=20,
        max_activities_per_field=None,
    ),
    AccountPlan.ENTERPRISE: PlanQuota(
        max_users=None,
        max_estates=None,
        max_fields_per_estate=None,
        max_activities_per_field=None,
    ),
}
