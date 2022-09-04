{{
    config(
        materialized='incremental',
        unique_key='id'
    )
}}

with raw_account as (
    select ext_account.value ->> 'Id' as id,
        ext_account.value ->> 'SystemModStamp' as system_mod_stamp,
        ext_account.value ->> 'AmountDue' as amount_due,
        ext_account.value ->> 'DueDate' as due_date,
        ext_account.value ->> 'ContactId' as contact_id,
        ext_account.date_partition as date_partition
    from
        {{ source('ext', 'ext_account') }} as ext_account
    {% if is_incremental() %}
    where
        ext_account.date_partition > (select max (date_partition) from {{ this }})
    {% endif %}
)

select
    *
from
    raw_account