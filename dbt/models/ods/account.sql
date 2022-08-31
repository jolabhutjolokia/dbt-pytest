with account as (
    select
        ext_account.date_partition as date_partition,
        ext_account.value->>'Id' as id,
        ext_account.value->>'ContactId' as contact_id,
        ext_account.value->>'SystemModStamp' as system_mod_stamp,
        ext_account.value->>'AmountDue' as amount_due,
        ext_account.value->>'DontCareAboutThis' as dont_care_about_this
    from
        {{ ref('ext_account') }} as ext_account
)


select * from account

