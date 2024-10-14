from osvutils.core.loader import OSVDataLoader
from osvutils.core.filters.loader import LoaderFilters
from osvutils.core.filters.database import DatabaseFilter
from osvutils.core.filters.affected_packages import AffectedPackagesFilter

from giturlparse import parse, validate


loader = OSVDataLoader(
    ecosystems=['GIT'],
    filters=LoaderFilters(
        database_filter=DatabaseFilter(
            prefix_is_cve=True
        ),
        affected_packages_filter=AffectedPackagesFilter(
            has_git_ranges=True
        )
    )
)

loader()
git_has_pkg_cnt = 0

for ecosystem, osv_data in loader:
    for _id, record in osv_data.items():
        if record.has_affected():
            for affected in record.affected:
                git_ranges = affected.get_git_ranges()

                if git_ranges:
                    for git_range in git_ranges:
                        print(git_range.repo)

print(f"{len(loader)} records loaded")
