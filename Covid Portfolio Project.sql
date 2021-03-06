#select * from covid_deaths_csv cdc 
#order by 4,5;

#select * from covid_vaccination_csv cvc
#order by 4,5;

#Clean data

update covid_deaths_csv 
set continent = null 
where continent = '';


#SELECT DATA THAT WE WILL BE USING FOR QUERIES

select location, date, total_cases, new_cases, total_deaths, population
from covid_deaths_csv cdc
where continent is not null
order by 1,2;

#TOTAL DEATHS PER TOTAL CASES

#SHOWS THE LIKELYHOOD OF DYING IF YOU CONTRACTED COVID IN YOUR COUNTRY - NIGERIA 

select location, date, total_cases, total_deaths, (total_deaths/total_cases)*100 as Death_Rate
from covid_deaths_csv cdc
where location like '%nigeria%'
order by 1,2;

#INFECTION RATE PER POPULATION 

select location, date, population, total_cases, (total_cases/population)*100 as Infected_Percentage
from covid_deaths_csv cdc
#where location like '%nigeria%'
order by 1,2;


#QUERYING BY COUNTRIES

#HIGHEST INFECTION RATES PER POPULATION BY COUNTRIES

select location, population, max(total_cases) as Highest_Infection_Count, 
(max(total_cases)/population)*100 as Percent_Population_Infected
from covid_deaths_csv cdc
where continent is not null
group by 1,2
order by 4 desc;

#HIGHEST DEATH COUNT PER POPULATION BY COUNTRIES

select location, population, max(total_deaths) as Highest_Death_Count
from covid_deaths_csv cdc
where continent is not null 
group by 1,2
order by 3 desc;


#QUERYING BY CONTINENT

#DEATH COUNT BY CONTINENT

select continent, last_value(sum(new_deaths)) over (partition by continent order by continent, date) as Current_Death_Count
from covid_deaths_csv cdc
where continent is not null 
group by 1
order by 2 desc;

#FACT CHECK

select location, max(total_deaths) as Current_Death_Count
from covid_deaths_csv cdc
where continent is null 
group by 1
order by 2 desc;



#INFECTION COUNT BY CONTINENT

select continent, last_value(sum(new_cases)) over (partition by continent order by continent, date) as Current_Infection_Count
from covid_deaths_csv cdc
where continent is not null
group by 1
order by 2 desc;

#FACT CHECK

select location, max(total_cases) as Current_Infection_Count
from covid_deaths_csv cdc
where continent is null 
group by 1
order by 2 desc;



#Global_Death_Count_Per_Infection_Cases 

select date, sum(new_cases) as New_Cases, sum(total_cases) as Total_Cases, sum(new_deaths) as New_Deaths, 
sum(total_deaths) as Total_Deaths, (sum(total_deaths)/sum(total_cases))*100 as Death_Per_Infection 
from covid_deaths_csv cdc
where continent is not null 
group by 1
order by 1,2;



#Percent_Population_Vacinnated Using CTE 

with population_vaccinated (Continent, Location, date, Population, New_Vaccine, Total_Vaccinations) 
as 
(
select cdc.continent, cdc.location, cdc.date, cdc.population, cvc.new_vaccinations, 
sum(new_vaccinations) over (partition by location order by location, date) as Total_Vaccinations
from covid_deaths_csv cdc 
join covid_vaccination_csv cvc 
on cdc.location = cvc.location and  cdc.date = cvc.date
where cdc.continent is not null
#order by 2,3
)

select *, (total_vaccinations/population)*100 as PercentPopulationVaccinated 
from population_vaccinated;



#Total_Tests_Per_Population Using Temp Table

drop temporary table PercentPopulationTests;
Create Temporary Table PercentPopulationTests 
(
	Continent varchar(255),
	Location varchar(255),
	Date date,
	Population numeric,
	New_Tests numeric,
	Total_Tests numeric
)
as 
(
select cdc.continent, cdc.location, cdc.date, cdc.population, cvc.new_tests, 
sum(new_tests) over (partition by location order by location, date) as Total_Tests
from covid_deaths_csv cdc 
join covid_vaccination_csv cvc 
on cdc.location = cvc.location and cdc.date = cvc.date 
where cdc.continent is not null 
order by 2,3
);


select *, (total_tests/population)*100 as PercentPopulationTests
from PercentPopulationTests;



#Creating Views to store data for visualization

#population_vaccinated

create view population_vaccinated as 
select cdc.continent, cdc.location, cdc.date, cdc.population, cvc.new_vaccinations, 
sum(new_vaccinations) over (partition by location order by location, date) as Total_Vaccinations
from covid_deaths_csv cdc 
join covid_vaccination_csv cvc 
on cdc.location = cvc.location and  cdc.date = cvc.date
where cdc.continent is not null
order by 2,3;


#Tests_Per_Population

create view Tests_Per_Population as
select cdc.continent, cdc.location, cdc.date, cdc.population, cvc.new_tests, 
sum(new_tests) over (partition by location order by location, date) as Total_Tests
from covid_deaths_csv cdc 
join covid_vaccination_csv cvc 
on cdc.location = cvc.location and cdc.date = cvc.date 
where cdc.continent is not null
order by 2,3;


#Global_Death_Count_Per_Infection_Cases

create view Global_Death_Count_Per_Infection_Cases as
select date, sum(new_cases) as New_Cases, sum(total_cases) as Total_Cases, sum(new_deaths) as New_Deaths, 
sum(total_deaths) as Total_Deaths, (sum(total_deaths)/sum(total_cases))*100 as Death_Per_Infection 
from covid_deaths_csv cdc
where continent is not null 
group by 1
order by 1,2;


#Infection_Count_Per_Continent

create view Infection_Count_Per_Continent as
select continent, last_value(sum(new_cases)) over (partition by continent order by continent, date) as Current_Infection_Count
from covid_deaths_csv cdc
where continent is not null
group by 1
order by 2 desc;


#DEATH COUNT BY CONTINENT

create view Death_Count_Per_Continent as
select continent, last_value(sum(new_deaths)) over (partition by continent order by continent, date) as Current_Death_Count
from covid_deaths_csv cdc
where continent is not null 
group by 1
order by 2 desc;


#TOTAL DEATHS PER TOTAL CASES IN NIGERIA

create view Nigeria_Death_Count_Per_Infection_Cases as
select location, date, total_cases, total_deaths, (total_deaths/total_cases)*100 as Death_Rate
from covid_deaths_csv cdc
where location like '%nigeria%'
order by 1,2;



