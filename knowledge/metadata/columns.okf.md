---
id: brso.column.dim_party.party_id
layer: metadata
kind: physical_column
title: PARTY_ID
version: meta-v0.1
status: ACTIVE
asset_id: brso.asset.dim_party
physical_name: PARTY_ID
data_type: VARCHAR
nullable: false
is_key: true
---
# PARTY_ID

---
id: brso.column.dim_party.party_name
layer: metadata
kind: physical_column
title: PARTY_NAME
version: meta-v0.1
status: ACTIVE
asset_id: brso.asset.dim_party
physical_name: PARTY_NAME
data_type: VARCHAR
nullable: false
is_key: false
---
# PARTY_NAME

---
id: brso.column.dim_party.country_id
layer: metadata
kind: physical_column
title: COUNTRY_ID
version: meta-v0.1
status: ACTIVE
asset_id: brso.asset.dim_party
physical_name: COUNTRY_ID
data_type: VARCHAR
nullable: true
is_key: false
---
# COUNTRY_ID

---
id: brso.column.dim_party.industry_id
layer: metadata
kind: physical_column
title: INDUSTRY_ID
version: meta-v0.1
status: ACTIVE
asset_id: brso.asset.dim_party
physical_name: INDUSTRY_ID
data_type: VARCHAR
nullable: true
is_key: false
---
# INDUSTRY_ID

---
id: brso.column.dim_industry.industry_id
layer: metadata
kind: physical_column
title: INDUSTRY_ID
version: meta-v0.1
status: ACTIVE
asset_id: brso.asset.dim_industry
physical_name: INDUSTRY_ID
data_type: VARCHAR
nullable: false
is_key: true
---
# INDUSTRY_ID

---
id: brso.column.dim_industry.industry_name
layer: metadata
kind: physical_column
title: INDUSTRY_NAME
version: meta-v0.1
status: ACTIVE
asset_id: brso.asset.dim_industry
physical_name: INDUSTRY_NAME
data_type: VARCHAR
nullable: false
is_key: false
---
# INDUSTRY_NAME

---
id: brso.column.dim_country.country_id
layer: metadata
kind: physical_column
title: COUNTRY_ID
version: meta-v0.1
status: ACTIVE
asset_id: brso.asset.dim_country
physical_name: COUNTRY_ID
data_type: VARCHAR
nullable: false
is_key: true
---
# COUNTRY_ID

---
id: brso.column.dim_country.country_name
layer: metadata
kind: physical_column
title: COUNTRY_NAME
version: meta-v0.1
status: ACTIVE
asset_id: brso.asset.dim_country
physical_name: COUNTRY_NAME
data_type: VARCHAR
nullable: false
is_key: false
---
# COUNTRY_NAME

---
id: brso.column.dim_country.region_id
layer: metadata
kind: physical_column
title: REGION_ID
version: meta-v0.1
status: ACTIVE
asset_id: brso.asset.dim_country
physical_name: REGION_ID
data_type: VARCHAR
nullable: false
is_key: false
---
# REGION_ID

---
id: brso.column.dim_region.region_id
layer: metadata
kind: physical_column
title: REGION_ID
version: meta-v0.1
status: ACTIVE
asset_id: brso.asset.dim_region
physical_name: REGION_ID
data_type: VARCHAR
nullable: false
is_key: true
---
# REGION_ID

---
id: brso.column.dim_region.region_name
layer: metadata
kind: physical_column
title: REGION_NAME
version: meta-v0.1
status: ACTIVE
asset_id: brso.asset.dim_region
physical_name: REGION_NAME
data_type: VARCHAR
nullable: false
is_key: false
---
# REGION_NAME

---
id: brso.column.fact_exposure.party_id
layer: metadata
kind: physical_column
title: PARTY_ID
version: meta-v0.1
status: ACTIVE
asset_id: brso.asset.fact_exposure
physical_name: PARTY_ID
data_type: VARCHAR
nullable: false
is_key: false
---
# PARTY_ID

---
id: brso.column.fact_exposure.facility_id
layer: metadata
kind: physical_column
title: FACILITY_ID
version: meta-v0.1
status: ACTIVE
asset_id: brso.asset.fact_exposure
physical_name: FACILITY_ID
data_type: VARCHAR
nullable: false
is_key: false
---
# FACILITY_ID

---
id: brso.column.fact_exposure.exposure_date
layer: metadata
kind: physical_column
title: EXPOSURE_DATE
version: meta-v0.1
status: ACTIVE
asset_id: brso.asset.fact_exposure
physical_name: EXPOSURE_DATE
data_type: DATE
nullable: false
is_key: false
---
# EXPOSURE_DATE

---
id: brso.column.fact_exposure.ead
layer: metadata
kind: physical_column
title: EAD
version: meta-v0.1
status: ACTIVE
asset_id: brso.asset.fact_exposure
physical_name: EAD
data_type: DECIMAL(20,4)
nullable: false
is_key: false
---
# EAD

---
id: brso.column.fact_exposure.currency
layer: metadata
kind: physical_column
title: CURRENCY
version: meta-v0.1
status: ACTIVE
asset_id: brso.asset.fact_exposure
physical_name: CURRENCY
data_type: CHAR(3)
nullable: false
is_key: false
---
# CURRENCY
