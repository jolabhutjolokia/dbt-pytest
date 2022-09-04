{{
    config(
        materialized='incremental',
        unique_key='id'
    )
}}

with ods_account as (
    select
        raw_account.id as id,
        raw_account.system_mod_stamp as system_mod_stamp,
        raw_account.amount_due as amount_due,
        raw_account.date_partition as date_partition,
        raw_account.contact_id as contact_id,
        raw_account.due_date as due_date
    from
        {{ ref('raw_account') }} as raw_account
    {% if is_incremental() %}
    where
        raw_account.date_partition > (select max (date_partition) from {{ this }})
    {% endif %}
)


select *
from ods_account

