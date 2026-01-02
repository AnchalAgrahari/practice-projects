create table usres (
    id serial primary key,
    name varchar(100) not null,
    balance int not null default '1000000'
);
select * from usres