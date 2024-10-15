from regscale.core.app.utils.app_utils import get_current_datetime
from regscale.core.utils.date import datetime_obj, datetime_str, date_str
from regscale.models import ScanHistory
from dateutil.relativedelta import relativedelta
import datetime


def get_last_pull_epoch(regscale_ssp_id: int) -> int:
    """
    Gather last pull epoch from RegScale Security Plan

    :param int regscale_ssp_id: RegScale System Security Plan ID
    :return: Last pull epoch
    :rtype: int
    """
    two_months_ago = datetime.datetime.now() - relativedelta(months=2)
    two_weeks_ago = datetime.datetime.now() - relativedelta(weeks=2)
    last_pull = round(two_weeks_ago.timestamp())  # default the last pull date to two weeks

    # Limit the query with a filter_date to avoid taxing the database in the case of a large number of scans
    filter_date = date_str(two_months_ago)

    if res := ScanHistory.get_by_parent_recursive(
        parent_id=regscale_ssp_id, parent_module="securityplans", filter_date=filter_date
    ):
        # Sort by ScanDate desc
        res = sorted(res, key=lambda x: (datetime_obj(x.scanDate) or get_current_datetime()), reverse=True)
        # Convert to timestamp
        last_pull = round(datetime_obj(res[0].scanDate).timestamp()) if res else 0

    return last_pull
