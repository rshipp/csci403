-- drop tables
drop table if exists rshipp.artists cascade;
drop table if exists rshipp.albums cascade;
drop table if exists rshipp.labels cascade;
drop table if exists rshipp.tracks cascade;
drop table if exists rshipp.artist_groups cascade;

-- create tables
create table rshipp.artists (
        id      serial,
        name    text not null,
        type    text not null,
        primary key (id)
);

create table rshipp.labels (
        id      serial,
        name    text not null,
        location text,
        primary key (id)
);

create table rshipp.albums (
        id      serial,
        title   text not null,
        year    numeric(4),
        genre   text not null,
        released_by integer references rshipp.artists(id),
        published_by integer references rshipp.labels(id),
        primary key (id)
);

create table rshipp.tracks (
        id      serial,
        name    text not null,
        number  text not null,
        is_on   integer references rshipp.albums(id),
        primary key (id)
);

create table rshipp.artist_groups (
        id      serial,
        artist_id integer references rshipp.artists(id),
        group_id integer references rshipp.artists(id),
        begin_year numeric(4),
        end_year numeric(4),
        primary key (id)
);

-- migrate data

-- artists
insert into rshipp.artists (name, type)
    select artist_name, artist_type
        from public.project4
        group by artist_name, artist_type;

insert into rshipp.artists (name, type)
    select member_name, 'Person' as type
        from public.project4
        where member_name not in (select name from rshipp.artists)
        group by member_name;

-- labels
insert into rshipp.labels (name, location)
    select label, headquarters 
        from public.project4
        group by label, headquarters;

-- albums
insert into rshipp.albums (title, year, genre, released_by, published_by)
    select p.album_title, p.album_year, p.genre, a.id, l.id
        from public.project4 as p, rshipp.artists as a, rshipp.labels as l
        where p.artist_name = a.name and p.label = l.name
        group by p.album_title, p.album_year, p.genre, a.id, l.id;

-- tracks
insert into rshipp.tracks (name, number, is_on)
    select p.track_name, p.track_number, a.id
        from public.project4 as p, rshipp.albums as a
        where p.album_title = a.title
        group by p.track_name, p.track_number, a.id;

-- relation table
insert into rshipp.artist_groups (artist_id, group_id, begin_year, end_year)
    select a1.id, a2.id, p.member_begin_year, p.member_end_year
    from public.project4 as p, rshipp.artists as a1, rshipp.artists as a2
    where p.member_name = a1.name and p.artist_name = a2.name
    group by a1.id, a2.id, p.member_begin_year, p.member_end_year;


-- run queries
-- 1
select a.name, x.begin_year, x.end_year
    from rshipp.artists as a, rshipp.artist_groups as x, rshipp.artists as g
    where g.name = 'The Who' and x.group_id = g.id and x.artist_id = a.id
    order by x.begin_year, a.name;
-- 2
select g.name
    from rshipp.artists as a, rshipp.artists as g, rshipp.artist_groups as x
    where a.name = 'Chris Thile' and x.artist_id = a.id and x.group_id = g.id;
-- 3
select r.title, r.year, a.name, l.name
    from rshipp.albums as r,
         rshipp.artists as a,
         rshipp.labels as l
    where (r.released_by in (
            select g.id
                from rshipp.artists as a, rshipp.artists as g, rshipp.artist_groups as x
                where a.name = 'Chris Thile' and x.artist_id = a.id and x.group_id = g.id
            ) or
            r.released_by in (select id from rshipp.artists where name = 'Chris Thile')) and
          r.published_by = l.id and
          a.id = r.released_by
    group by r.title, r.year, a.name, l.name
    order by r.year;
-- 4
select a.name, r.title, r.year
    from rshipp.albums as r, rshipp.artists as a
    where r.genre = 'electronica' and r.released_by = a.id
    order by r.year, a.name;
-- 5
select t.name, t.number
    from rshipp.tracks as t, rshipp.artists as a, rshipp.albums as r
    where t.is_on = r.id and
          r.title = 'Houses of the Holy' and
          r.released_by = a.id and
          a.name = 'Led Zeppelin'
    order by t.number;
-- 6
select r.genre
    from rshipp.albums as r
    where (r.released_by in (
            select g.id
                from rshipp.artists as a, rshipp.artists as g, rshipp.artist_groups as x
                where a.name = 'James Taylor' and x.artist_id = a.id and x.group_id = g.id
            ) or
            r.released_by in (select id from rshipp.artists where name = 'James Taylor'))
    group by r.genre;
-- 7
select a.name, r.title, r.year, l.name
    from rshipp.artists as a, rshipp.albums as r, rshipp.labels as l
    where l.location = 'Hollywood' and r.published_by = l.id and r.released_by = a.id;
