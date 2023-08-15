use diesel;

diesel::table! {
    records {
        id -> Integer,
        name -> VarChar,
    }
}
