---
id: brso.join.fact_exposure_party
title: FACT_EXPOSURE to DIM_PARTY
layer: metadata
kind: physical_join
version: meta-v0.1
status: ACTIVE
source_asset_id: brso.asset.fact_exposure
target_asset_id: brso.asset.dim_party
source_column_id: brso.column.fact_exposure.party_id
target_column_id: brso.column.dim_party.party_id
cardinality: MANY_TO_ONE
preferred: true
certified: true
join_type: INNER
---
# FACT_EXPOSURE -> DIM_PARTY

---
id: brso.join.party_industry
title: DIM_PARTY to DIM_INDUSTRY
layer: metadata
kind: physical_join
version: meta-v0.1
status: ACTIVE
source_asset_id: brso.asset.dim_party
target_asset_id: brso.asset.dim_industry
source_column_id: brso.column.dim_party.industry_id
target_column_id: brso.column.dim_industry.industry_id
cardinality: MANY_TO_ONE
preferred: true
certified: true
join_type: INNER
---
# DIM_PARTY -> DIM_INDUSTRY

---
id: brso.join.party_country
title: DIM_PARTY to DIM_COUNTRY
layer: metadata
kind: physical_join
version: meta-v0.1
status: ACTIVE
source_asset_id: brso.asset.dim_party
target_asset_id: brso.asset.dim_country
source_column_id: brso.column.dim_party.country_id
target_column_id: brso.column.dim_country.country_id
cardinality: MANY_TO_ONE
preferred: true
certified: true
join_type: INNER
---
# DIM_PARTY -> DIM_COUNTRY

---
id: brso.join.country_region
title: DIM_COUNTRY to DIM_REGION
layer: metadata
kind: physical_join
version: meta-v0.1
status: ACTIVE
source_asset_id: brso.asset.dim_country
target_asset_id: brso.asset.dim_region
source_column_id: brso.column.dim_country.region_id
target_column_id: brso.column.dim_region.region_id
cardinality: MANY_TO_ONE
preferred: true
certified: true
join_type: INNER
---
# DIM_COUNTRY -> DIM_REGION
