/*****************************/
/* PROJECT 5 SCHEMA CREATION */
/*****************************/
drop table if exists album_genre cascade;
drop table if exists genre cascade;
drop table if exists album cascade;
drop table if exists artist cascade;

create table artist (
	id serial, 
	name text NOT NULL, 
	primary key(id));

create table album (
	id serial,
	artist_id integer,
	title text NOT NULL,
	year numeric(4),
	primary key (id),
	foreign key (artist_id) references artist (id));

create table genre (genre text PRIMARY KEY);

create table album_genre (
	album_id integer,
	genre text,
	primary key (album_id, genre),
	foreign key (album_id) references album(id),
	foreign key (genre) references genre(genre));

/******************/
/* DATA MIGRATION */
/******************/

/* populate artist table */
insert into artist (name)
select distinct artist_name from project4;

/* populate album table */
insert into album (artist_id, title, year)
select distinct 
	a.id,
	p.album_title,
	p.album_year
from
	artist a,
	project4 p
where a.name = p.artist_name;

/* populate genre tables */
insert into genre
select distinct genre from project4;

insert into album_genre 
select distinct a.id, p.genre
from album a, project4 p
where p.album_title = a.title;

