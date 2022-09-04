{{
    config(
        materialized='incremental',
        unique_key='id'
    )
}}

with raw_contact as (
    select ext_contact.value ->> 'Id' as id,
        ext_contact.value ->> 'Name' as name,
        ext_contact.value ->> 'SystemModStamp' as system_mod_stamp,
        ext_contact.value ->> 'Phone' as phone,
        ext_contact.date_partition as date_partition
    from
        {{ source('ext', 'ext_contact') }} as ext_contact
    {% if is_incremental() %}
    where
        ext_contact.date_partition > (select max (date_partition) from {{ this }})
    {% endif %}
)

select
    *
from
    raw_contact