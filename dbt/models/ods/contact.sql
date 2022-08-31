with contact as (
    select
        ext_account.date_partition as date_partition,
        ext_account.value->>'Id' as id,
        ext_account.value->>'SystemModStamp' as system_mod_stamp,
        ext_account.value->>'Mobile' as mobile,
        ext_account.value->>'DateOfBirth' as date_of_birth
    from
        {{ ref('ext_contact') }} as ext_contact
)


select * from contact

