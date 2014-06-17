drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  title string not null,
  'text' text not null,
  'datetime' string not null
);
