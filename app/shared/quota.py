from app.domain.accounts.models.plan import PLAN_QUOTAS, AccountPlan


class QuotaService:
    def check(
        plan: AccountPlan, resource: str, current_count: int
    ) -> True | False:
        quota = PLAN_QUOTAS[plan]
        limit = getattr(quota, f'max_{resource}')

        if limit is not None and current_count >= limit:
            return False
        return True
