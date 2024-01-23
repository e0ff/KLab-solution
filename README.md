# KLab-solution
1. Есть таблица A с полями id, type, parent_id, extra, у которой есть foreign key A.parent_id to A.id. 
Поле type может иметь 3 значения root/branch/leaf. leaf могут содержать в extra параметр color. 
Некоторые leaf имеют связь с branch по parent_id.
Некоторые branch имеют связь с root по parent_id.
Нужно составить SQL запрос без создания функций в котором в строке будут следующие данные:
- root_id: идентификатор корня;
- branch_count: количество связанных с корнем веток;
- leaf_colors: массив уникальных цветов листьев без null;

Пример:
| id 	| type 	 | parent_id | extra 		 |
| 1  	| root 	 | null	     | null  		 |
| 2     | root   | null      | null  		 |
| 3     | root   | null      | null  		 |
| 4  	| branch | 1	     | null   		 |
| 5	| branch | 1	     | null              |
| 6	| branch | 1	     | null              |
| 7     | branch | 2         | null              |
| 8	| branch | null	     | null              |
| 9     | leaf   | 4         | {"color":"green"} |
| 10    | leaf   | 4         | {"color":"green"} |
| 11    | leaf   | 4         | {"color":"yellow"}|
| 12    | leaf   | 5         | {}		 |
| 13    | leaf   | 5         | {"color":"green"} |
| 14    | leaf   | 5         | {"color":"red"}   |
| 15    | leaf   | 7         | {"color":"green"} |
| 16    | leaf   | 7         | null		 |
| 17    | leaf   | null      | {"color":"green"} |

Результат запроса
| root_id | branch_count | leaf_colors 		     |
| 1	  | 3		 | {"green","yellow", "red"} |
| 2	  | 1		 | {"green"}		     |
| 3	  | 0		 | {}			     |

2. Написать простое REST веб приложение представляющее из себя таблицу в БД.
Данные хранятся в оперативной памяти.
Доступные колонки в таблице id, value.
Приложение должно содержать базовые роуты /select (просто возврат всего в таблице), /insert (по value), /delete (по id),
а так же роуты для работы с вложенными транзакциями, /begin, /commit, /rollback. 
Транзакции должны открываться независимо друг от друга, а так же иметь возможность быть вложенными (Условно могут быть открыты одновременно 2 транзакции или транзакция внутри транзакции).

## Задание 1, на sql
смотри в файле solution.sql
использовал PostgreSQL 15

## Задание 2, веб-приложение
смотри в папке simple_rest_app
использовал poetry, fastapi, pytest
