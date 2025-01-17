def create_tables_and_views(connection):
    cursor = connection.cursor()
    print("Connected to database")
    cursor.execute("create database if not exists pokemon_db;")

    cursor.execute("""
    create table if not exists trainer (
        trainer_id int auto_increment primary key,
        name varchar(50) not null,
        age int not null,
        team varchar(50) not null
    );
    """)

    cursor.execute("""
    create table if not exists pokemon (
        pokemon_id int auto_increment primary key,
        name varchar(50) not null,
        type enum('Fire', 'Water', 'Grass') not null,
        level int not null,
        trainer_id int null,
        foreign key (trainer_id) references trainer(trainer_id) on delete set null
    );
    """)

    cursor.execute("""
    create table if not exists gym (
        gym_id int auto_increment primary key,
        name varchar(50) not null,
        city varchar(50) not null
    );
    """)

    cursor.execute("""
    create table if not exists trainer_gym (
        trainer_id int,
        gym_id int,
        primary key (trainer_id, gym_id),
        foreign key (trainer_id) references trainer(trainer_id) on delete cascade,
        foreign key (gym_id) references gym(gym_id) on delete cascade
    );
    """)

    cursor.execute("""
    create table if not exists pokemon_stats (
        stats_id int auto_increment primary key,
        pokemon_id int not null,
        speed float not null,
        strength float not null,
        defense float not null,
        foreign key (pokemon_id) references pokemon(pokemon_id) on delete cascade
    );
    """)

    cursor.execute("""
    create or replace view pokemon_type_report as
    select type, count(*) as total_pokemon
    from pokemon
    group by type;
    """)

    cursor.execute("""
    create or replace view trainer_stats as
    select t.name as trainer_name, count(p.pokemon_id) as total_pokemon, avg(p.level) as avg_level
    from trainer t
    left join pokemon p on t.trainer_id = p.trainer_id
    group by t.trainer_id;
    """)

    connection.commit()
    print("Tables and views have been created.")
