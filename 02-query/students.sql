-- Drop tables
drop table rshipp.hogwarts_dada;
drop table rshipp.hogwarts_students;
drop table rshipp.hogwarts_houses;


-- Create tables
create table rshipp.hogwarts_dada AS
    select * from public.hogwarts3;

create table rshipp.hogwarts_houses AS
    select * from public.hogwarts2;
alter table rshipp.hogwarts_houses 
    add id serial primary key,
    alter house set not null,
    add constraint house_key unique (house);

create table rshipp.hogwarts_students (
        last    text not null,
        first   text not null,
        house   text references rshipp.hogwarts_houses(house),
        start   numeric(4),
        finish  numeric(4),
        primary key (last, first)
);


insert into rshipp.hogwarts_students (last, first, house, start, finish)
    select last,
       first,
       case when house='?' then NULL
            when house='Griffindor' then 'Gryffindor'
            else house
       end,
       case when start='?' then NULL
            else to_number(start, '9999')
       end,
       case when finish='?' then NULL
            else to_number(finish, '9999')
       end
    from public.hogwarts1;

-- Run queries
-- 1
select last, first from rshipp.hogwarts_students
    where start=1991 and house='Gryffindor'
    order by last, first;
-- 2
select count(*) from rshipp.hogwarts_students
    where house='Slytherin';
-- 3
select start from rshipp.hogwarts_students
    order by start
    limit 1;
--4 
select count(*) from rshipp.hogwarts_students
    where start is null
        or finish is null
        or house is null;
-- 5
select count(*) from rshipp.hogwarts_students
    where start is not null
        and finish is not null
        and house is not null;
-- 6
select founder from rshipp.hogwarts_houses
    where house=(select house from rshipp.hogwarts_students
                    where last='McDougal' and first='Morag');
-- 7
select last, first from rshipp.hogwarts_students
    where house=(select house from rshipp.hogwarts_houses
                    where animal='Badger')
    order by last, first;
-- 8
select house, count(*) from rshipp.hogwarts_students
    group by house;
-- 9
select last, first from rshipp.hogwarts_students
    order by start
    limit 1;
-- 10
select house, count(*) from rshipp.hogwarts_students
    where start=(select start from rshipp.hogwarts_dada
                    where last='Moody' and first='Alastor')
    group by house;
-- 11
select last, first from rshipp.hogwarts_students
    where house='Gryffindor'
        and start <= (select finish from rshipp.hogwarts_dada
                        where last='Lockhart' and first='Gilderoy')
        and finish >= (select start from rshipp.hogwarts_dada
                        where last='Lockhart' and first='Gilderoy');
-- 12
select d.last, d.first from rshipp.hogwarts_dada as d,
                            rshipp.hogwarts_students as s
    where d.first=s.first and d.last=s.last;
-- 13
select left(last, 1) from rshipp.hogwarts_students
    where house is null
        or start is null
        or finish is null
    group by left(last, 1)
    having count(*)=8;
