{{
    config(
        materialized='incremental',
        unique_key='id'
    )
}}

with ods_account as (
    select
        raw_account.id as id,
        case
            when raw_account.name is null then ''
            when trim(raw_account.name) = '' then ''
            else split_part(raw_account.name,' ', 1)
        end
        as first_name,
        case
            when raw_account.name is null then ''
            when trim(raw_account.name) = '' then ''
            else regexp_replace(trim(raw_account.name), '^.* ', '')
        end
        as last_name,
        raw_account.system_mod_stamp as system_mod_stamp,
        raw_account.amount_due as amount_due,
        raw_account.date_partition as date_partition
    from
        {{ ref('raw_account') }} as raw_account
    {% if is_incremental() %}
    where
        raw_account.date_partition > (select max (date_partition) from {{ this }})
    {% endif %}
)


select *
from ods_account

