from collections import defaultdict
from nvdutils.core.loaders.json_loader import JSONFeedsLoader
from nvdutils.types.options import CVEOptions
from nvdutils.types.configuration import CPEPart

loader = JSONFeedsLoader(data_path='~/.nvdutils/nvd-json-data-feeds', options=CVEOptions(), verbose=True)

# Populate the loader with CVE records
loader.load()

tgt_hw = defaultdict(int)
vendor_product_pairs = set()
app_specific_cves = 0
platform_specific_cves = 0

for cve_id, cve in loader.records.items():

    try:
        vendor_product_tgt_hw = cve.get_target(target_type='hw', skip_sw=['*', '-'], is_vulnerable=True,
                                               is_part=CPEPart.Application, is_platform_specific=True, strict=True)
    except ValueError as e:
        continue

    app_specific_cves += 1

    if len(vendor_product_tgt_hw) == 0:
        continue

    platform_specific_cves += 1

    for vendor_product, target_hw in vendor_product_tgt_hw.items():
        vendor_product_pairs.add(vendor_product)
        for hw in target_hw:
            # count only once per vendor-product
            tgt_hw[hw] += 1


print(len(vendor_product_pairs), dict(tgt_hw))
print(f"App specific CVEs: {app_specific_cves}")
print(f"Platform specific CVEs: {platform_specific_cves}")
