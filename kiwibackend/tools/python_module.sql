SET group_concat_max_len = 1024000;


select concat(yy.a, '\n', yy.bb) as tt from (
select xx.a, group_concat(xx.b SEPARATOR '\n') as bb from(

select tmp.tbl as a,
CONCAT('    ',tmp.col,' = ', tmp.typ) as b
from (
SELECT 
concat('\nclass ', TABLE_NAME, '(models.Model):') as tbl, 
COLUMN_NAME as col, 
 case `DATA_TYPE`
     when 'float' then 'models.FloatField()'
     when 'double' then 'models.FloatField()'
     when 'int' then 'models.IntegerField()'
     when 'tinyint' then 'models.BooleanField()'
     when 'varchar' then 'models.CharField(max_length=200)'
end as typ
FROM `information_schema`.`COLUMNS` where `TABLE_SCHEMA`='develop' order by TABLE_NAME, col,typ
) tmp
) xx
group by a ) yy
