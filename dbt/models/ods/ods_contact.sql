{{
    config(
        materialized='incremental',
        unique_key='id'
    )
}}

with ods_contact as (
    select
        raw_contact.id as id,
        case
            when raw_contact.name is null then ''
            when trim(raw_contact.name) = '' then ''
            else split_part(raw_contact.name,' ', 1)
        end
        as first_name,
        case
            when raw_contact.name is null then ''
            when trim(raw_contact.name) = '' then ''
            else regexp_replace(trim(raw_contact.name), '^.* ', '')
        end
        as last_name,
        raw_contact.system_mod_stamp as system_mod_stamp,
        raw_contact.date_partition as date_partition
    from
        {{ ref('raw_contact') }} as raw_contact
    {% if is_incremental() %}
    where
        raw_contact.date_partition > (select max (date_partition) from {{ this }})
    {% endif %}
)


select *
from ods_contact

