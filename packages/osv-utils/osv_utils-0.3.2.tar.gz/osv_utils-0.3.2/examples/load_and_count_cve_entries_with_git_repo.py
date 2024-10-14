from osvutils.core.loader import OSVDataLoader
from osvutils.core.filters.loader import LoaderFilters
from osvutils.core.filters.database import DatabaseFilter
from osvutils.core.filters.affected_packages import AffectedPackagesFilter


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
                        fix_events = git_range.get_fixed_events()

                        if len(fix_events) > 1:
                            print(f"Multiple fix events found for {record.id}")


print(f"{len(loader)} records loaded")
