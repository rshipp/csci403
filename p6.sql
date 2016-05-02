drop table if exists volume cascade;
drop table if exists segments cascade;

create table segments (
        id         serial,      
        segment_id integer,
        road       text not null,
        fromroad   text not null,
        toroad     text not null,
        direction  text not null,
        primary key (id)
);

create table volume (
        id         serial,
        segment_id integer references segments(id),
        datetime   timestamp,
        volume     float,
        primary key (id)
);
