
from osvutils.core.collector import OSVDataCollector

collector = OSVDataCollector(verbose=True)
count = collector(['Debian', 'Ubuntu', 'npm'])

print(f"Total records collected: {count}")
