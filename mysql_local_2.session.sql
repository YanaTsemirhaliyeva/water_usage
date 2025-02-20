/* SELECT * FROM water_usage; */

-- Выведем 5 стран с наибольшим потреблением воды на душу населения
SELECT country, yearly_water_used, daily_water_used_per_capita, population 
FROM water_usage
ORDER BY daily_water_used_per_capita DESC
LIMIT 5;

-- Выведем 5 стран с наименьшим потреблением воды на душу населения
SELECT country, yearly_water_used, daily_water_used_per_capita, population 
FROM water_usage
ORDER BY daily_water_used_per_capita
LIMIT 5;

-- Вывод среднего потребления воды
SELECT AVG(yearly_water_used), AVG(daily_water_used_per_capita)
FROM water_usage;

-- Вывод суммарного потребления (годового, на человека)
SELECT SUM(yearly_water_used), SUM(daily_water_used_per_capita)
FROM water_usage;

-- Посмотрим какой расход воды в Беларуси
SELECT country, yearly_water_used, daily_water_used_per_capita, population
FROM water_usage
WHERE country = 'Belarus'