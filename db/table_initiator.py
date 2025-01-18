def create_tables_and_views(connection):
    cursor = connection.cursor()
    print("Připojeno k databázi")
    cursor.execute("create database if not exists pokemon_db;")

    cursor.execute("""
    create table if not exists trainer (
        id int auto_increment primary key,
        name varchar(50) not null,
        age int not null,
        team varchar(50) not null,
        created_at datetime default current_timestamp,
        updated_at datetime default current_timestamp on update current_timestamp
    );
    """)

    cursor.execute("""
    create table if not exists pokemon (
        id int auto_increment primary key,
        name varchar(50) not null,
        type enum('Fire', 'Water', 'Grass') not null,
        level int not null,
        trainer_id int null,
        created_at datetime default current_timestamp,
        updated_at datetime default current_timestamp on update current_timestamp,
        foreign key (trainer_id) references trainer(id) on delete set null
    );
    """)

    cursor.execute("""
    create table if not exists gym (
        id int auto_increment primary key,
        name varchar(50) not null,
        city varchar(50) not null
    );
    """)

    cursor.execute("""
    create table if not exists trainer_gym (
        trainer_id int,
        gym_id int,
        primary key (trainer_id, gym_id),
        foreign key (trainer_id) references trainer(id) on delete cascade,
        foreign key (gym_id) references gym(id) on delete cascade
    );
    """)

    cursor.execute("""
    create table if not exists pokemon_stats (
        id int auto_increment primary key,
        pokemon_id int not null,
        speed float not null,
        strength float not null,
        defense float not null,
        is_alive bool default true,
        foreign key (pokemon_id) references pokemon(id) on delete cascade
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
    select trainer.name as trainer_name, count(pokemon.id) as total_pokemon, avg(pokemon.level) as avg_level
    from trainer
    left join pokemon on trainer.id = pokemon.trainer_id
    group by trainer.id;
    """)

    cursor.execute("""
    drop procedure if exists insert_trainer_and_pokemon;               
    """)

    cursor.execute("""
    create procedure insert_trainer_and_pokemon(
        in trainer_name varchar(50),
        in trainer_age int,
        in trainer_team varchar(50),
        in pokemon_name varchar(50),
        in pokemon_type enum('Fire', 'Water', 'Grass'),
        in pokemon_level int
    )
    begin
        declare trainer_id int;
        insert into trainer (name, age, team)
        values (trainer_name, trainer_age, trainer_team);
        set trainer_id = last_insert_id();
        insert into pokemon (name, type, level, trainer_id)
        values (pokemon_name, pokemon_type, pokemon_level, trainer_id);
    end          
    """)

    connection.commit()
    print("Tabulky, pohledy a procedura byly vytvořeny.")

