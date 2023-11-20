-- create
create table if not exists A (
id integer primary key,
type text,
parent_id integer null,
extra json null,
foreign key(parent_id) references A(id)
);

-- insert
INSERT INTO A VALUES(1, 'root', null, null);
INSERT INTO A VALUES(2, 'root', null, null);
INSERT INTO A VALUES(3, 'root', null, null);
INSERT INTO A VALUES(4, 'branch', 1, null);
INSERT INTO A VALUES(5, 'branch', 1, null);
INSERT INTO A VALUES(6, 'branch', 1, null);
INSERT INTO A VALUES(7, 'branch', 2, null);
INSERT INTO A VALUES(8, 'branch', null, null);
INSERT INTO A VALUES(9, 'leaf', 4, '{"color":"green"}');
INSERT INTO A VALUES(10, 'leaf', 4, '{"color":"green"}');
INSERT INTO A VALUES(11, 'leaf', 4, '{"color":"yellow"}');
INSERT INTO A VALUES(12, 'leaf', 5, '{}');
INSERT INTO A VALUES(13, 'leaf', 5, '{"color":"green"}');
INSERT INTO A VALUES(14, 'leaf', 5, '{"color":"red"}');
INSERT INTO A VALUES(15, 'leaf', 7, '{"color":"green"}');
INSERT INTO A VALUES(16, 'leaf', 7, null);
INSERT INTO A VALUES(17, 'leaf', null, '{"color":"green"}');

SELECT * FROM A;

---------------SOLUTION------------------------------------
SELECT
    root.id AS root_id,
    COUNT(DISTINCT branch.id) AS branch_count,
    ARRAY_REMOVE(ARRAY_AGG(DISTINCT leaf.extra->>'color' ORDER BY leaf.extra->>'color' NULLS LAST), NULL) AS leaf_colors
FROM
    A AS root
LEFT JOIN
    A AS branch ON branch.parent_id = root.id AND branch.type = 'branch'
LEFT JOIN
    A AS leaf ON leaf.parent_id = branch.id AND leaf.type = 'leaf'
WHERE
    root.type = 'root'
GROUP BY
    root.id;
----------------------------------------------------------
