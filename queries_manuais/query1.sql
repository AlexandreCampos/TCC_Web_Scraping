SELECT * 
FROM information_schema.tables
WHERE table_schema = 'projeto_scrapper'; 

select * from category;
select * from store_config;
select * from regex;
select * from product;
select * from comparison;
select * from product where comparison_id is not null;
-- drop table store_config;
-- delete from store_config where id = 3;
