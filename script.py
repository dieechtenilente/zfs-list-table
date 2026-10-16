import json
from subprocess import run

SORT_BY = "used_percent"
SORT_REVERSE= True
PRINT_TOP_N = True
TOP_N = 5

# zfs list parameters:
# -j         -- Print the output in JSON format
# --json-int -- print the numbers as integer instead of strings
# -p         -- Display numbers in parsable (exact) values
result = run(
    ["zfs", "list", "-o", "name,used,quota,available", "-j", "--json-int", "-p"],
    capture_output=True,
    text=True,
    check=True,
)

try:
    data = json.loads(result.stdout)
except:
    pass


zfs_datasets = []

for name, dataset in data["datasets"].items():
    props = dataset["properties"]
    used = int(props["used"]["value"]) / 1024 / 1024 / 1024 # convert into GiB
    quota = int(props["quota"]["value"]) / 1024 / 1024 / 1024 # convert into GiB
    available = int(props["available"]["value"]) / 1024 / 1024 / 1024 # convert into GiB

    if quota > 0:
        used_percent = used / quota * 100
    else:
        used_percent = 0

    zfs_datasets.append({
        "name": name,
        "used": used,
        "quota": quota,
        "available": available,
        "used_percent": used_percent
    })


# Table header
table_header = f"{'NAME':<30} {'USED GiB':>12} {'QUOTA GiB':>12} {'AVAIL GiB':>12} {'USED %':>12}"
print(table_header)
print("-" * len(table_header))

# order by used_percent, descending
zfs_datasets.sort(key=lambda d: d[SORT_BY], reverse=SORT_REVERSE)

# Print only first TOP_N results
if PRINT_TOP_N:
    print_until = TOP_N
else:
    print_until = int(len(zfs_datasets))

# Print table content
for d in zfs_datasets[:print_until]:
    # String formatting
    # <    -- left-aligned
    # >    -- right-aligned
    # 12   -- use a minimum width of 12 chars
    # :.2f -- two digits after decimal point
    #print(f"{d['name']:<30} {d['used']:12.2f} {d['quota']:12.2f} {d['available']:12.2f} {d['used_percent']:12.2f}")
    print(f"{d['name']:<30} {d['used']:12.2f} {d['quota']:12.2f} {d['available']:12.2f} {d['used_percent']:12.2f}")