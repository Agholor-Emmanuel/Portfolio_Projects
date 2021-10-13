select * 
from nashville_housing nh ;


#Populate Property Address Data

update nashville_housing 
set propertyAddress = null 
where propertyaddress  = '';

select *
from nashville_housing nh 
where PropertyAddress is null
order by parcelid;

select nh1.UniqueID, nh1.ParcelID, nh1.PropertyAddress, nh2.UniqueID, nh2.ParcelID, nh2.PropertyAddress,
IFNULL(nh1.PropertyAddress, nh2.PropertyAddress) as PopulatedAddress
from nashville_housing nh1
join nashville_housing nh2
on nh1.ParcelID = nh2.ParcelID and nh1.UniqueID <> nh2.UniqueID
where nh1.PropertyAddress is null;


update nashville_housing nh1
join nashville_housing nh2
on nh1.ParcelID = nh2.ParcelID and nh1.UniqueID <> nh2.UniqueID
set nh1.PropertyAddress = IFNULL(nh1.PropertyAddress, nh2.PropertyAddress)
where nh1.PropertyAddress is null;

#Check to see if PropertyAddress have been Updated

select propertyaddress
from nashville_housing nh 
where PropertyAddress is null;



#Breaking Out Property Address into Individual Column (Address, City)

select propertyaddress
from nashville_housing nh;

select
substring(PropertyAddress, 1, instr(PropertyAddress, ',' ) -1) as Address,
substring(PropertyAddress, instr(PropertyAddress, ',' ) +1, length(PropertyAddress) ) as City
from nashville_housing nh;

alter table nashville_housing
add Property_Address varchar(255);

update nashville_housing 
set Property_Address = substring(PropertyAddress, 1, instr(PropertyAddress, ',' ) -1);


alter table nashville_housing
add Property_City varchar(255);

update nashville_housing 
set Property_City = substring(PropertyAddress, instr(PropertyAddress, ',' ) +1, length(PropertyAddress) );

select *
from nashville_housing nh;



#Breaking Out Owner Address into Individual Column (Address, City, State)

select OwnerAddress 
from nashville_housing nh;


select
substring_index(OwnerAddress, ',', 1) as Owner_Address,
substring_index(substring_index(OwnerAddress, ',', 2), ',' , -1) as Owner_City,
substring_index(OwnerAddress, ',', -1) as Owner_State
from nashville_housing nh;

alter table nashville_housing 
add Owner_Address varchar(255),
add Owner_City varchar(255),
add Owner_State varchar(10);

update nashville_housing 
set 
Owner_Address = substring_index(OwnerAddress, ',', 1),
Owner_City = substring_index(substring_index(OwnerAddress, ',', 2), ',' , -1),
Owner_State = substring_index(OwnerAddress, ',', -1);

select *
from nashville_housing nh;



#Change Y and N to Yes and No in "SoldAsVacant" field

select distinct(SoldAsVacant), count(SoldAsVacant) 
from nashville_housing nh
group by SoldAsVacant 
order by 2; 


select SoldAsVacant, 
	case when SoldAsVacant = 'Y' then 'YES'
	 	 when SoldAsVacant = 'N' then 'NO'
		 else SoldAsVacant 
	end
from nashville_housing nh;

update nashville_housing 
set SoldAsVacant = 
	case when SoldAsVacant = 'Y' then 'YES'
	 	 when SoldAsVacant = 'N' then 'NO'
		 else SoldAsVacant 
	end;
		
		

		
#Removing Duplicate values

with Row_Num_CTE as 
(
select *, 
	row_number() over 
	(partition by
				parcelid,
				propertyaddress,
				saleprice,
				saledate,
				legalreference
	 order by 
	 			uniqueid) as Row_num
from nashville_housing nh
#order by ParcelID;
)

delete from nashville_housing using nashville_housing 
join Row_Num_CTE
on nashville_housing.UniqueID = Row_Num_CTE.uniqueid
where row_num > 1;



#Run together with the CTE query above to confirm that duplicates have been deleted

select * from nashville_housing 
join Row_Num_CTE
on nashville_housing.UniqueID = Row_Num_CTE.uniqueid
where row_num > 1;


#Delete Unused Columns

alter table nashville_housing 
drop column propertyaddress, 
drop column owneraddress;


select * from nashville_housing;
	
		
		
