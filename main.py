import uuid
from fastapi import FastAPI,HTTPException,Depends,status
from fastapi.responses import JSONResponse,HTMLResponse
from flask import jsonify
from pydantic import BaseModel,validator
from typing import  List, Optional
from typing_extensions import Annotated
from typing import List, Optional
import models
from uuid import uuid4, UUID
from datetime import date, datetime, time, timedelta
from database import engine,SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
import httpx
from pydantic.dataclasses import dataclass
from fastapi.middleware.cors import CORSMiddleware
from urllib.parse import urljoin

app=FastAPI(title="Fleetrez B2C" ,description="For serving better quality of API without lagging")
models.Base.metadata.create_all(bind=engine)

origins = [
    "*",
    "/*",
    "http://localhost",
    "http://localhost:8000",
    "http://localhost",
    "http://localhost:3000",
    "https://localhost",
    "https://localhost:8000",
    "http://127.0.0.1:5500/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# class PostBase(BaseModel):
#     title:str
#     content: str
#     user_id: int
#     class Config:
#         orm_mode=True

# class UserBase(BaseModel):
#     name: str
#     class Config:
#         orm_mode=True

        
date_str = "2023-10-11T15:30:00"
class location_searchBase(BaseModel):
    pick_up_locations: str
    drop_off_locations: str
    pick_up_date_time: datetime
    drop_off_date_time: datetime
    promo_code:str
    driver_age:int

 
@validator("pick_up_date_time", "drop_off_date_time", pre=True, always=True)
def parse_datetime_fields(cls, value):
        try:
            # Define your custom datetime format here
            custom_format = "%Y-%m-%d %H:%M"
            return datetime.strptime(value, custom_format)
        except (ValueError, TypeError):
            raise ValueError("Invalid datetime format")
        
class categoryVehicle(BaseModel):
    name:str

class ManagebookingBase(BaseModel):
    email:str
    booking_reference:str
    
class categoryBase(BaseModel):
    name:str

class AcrissBase(BaseModel):
    name:str
    class Config:
        orm_mode=True


class locationBase(BaseModel):
    location_name:str
    days:UUID = uuid4()
    class Config:
        orm_mode=True

class modifysearchBase(BaseModel):
    pick_up_locations: str
    drop_off_locations: str
    pick_up_date_time: datetime
    drop_off_date_time: datetime
    vehicle_type:list
    driver_age:int
    paymentType:list 


class vehicleBase(BaseModel):
    name:str
    vehicle_type:str
    location_name:str
    excess_amount:float
    local_fee:int
    price:float
    image:str
    rating:float
    payment_method:str
    rating_count:int
    acriss_id:UUID = uuid4()
    image:str
    attribute_id:UUID = uuid4()
    location_id:UUID = uuid4()
    vehicle_group_id:UUID = uuid4()
    inclusion_id:UUID = uuid4()
    category_id:UUID = uuid4()
    class Config:
        orm_mode=True


class locationBase(BaseModel):
    location_name:str
    image:str
    days:UUID = uuid4()
    class Config:
        orm_mode=True

class inclusionBase(BaseModel):
    name:str


class vehicleGroupBase(BaseModel):
    name:str
    class Config:
        orm_mode=True


class t_cBase(BaseModel):
    title:str
    description:str 
    class Config:
        orm_mode=True

class rental_t_cBase(BaseModel):
    title:str
    description:str 
    class Config:
        orm_mode=True


class attributeBase(BaseModel):
    attribute_name:str
    class Config:
        orm_mode=True

class insuranceBase(BaseModel):
    name:Optional[str]
    amount:Optional[float]
    type:Optional[str]
    description:str
    class Config:
        orm_mode=True

class extraBase(BaseModel):
    name:Optional[str]
    amount:Optional[float]
    type:Optional[str]
    image:Optional[str]
    quantity:Optional[int]
    class Config:
        orm_mode=True

class booking_vehicleBase(BaseModel):
    name:Optional[str] = None
    booking_ref:Optional[str] = None
    pickup_Date:Optional[datetime] = None
    dropoff_Date:Optional[datetime] = None
    vehicle_type:Optional[str] = None
    excess_amount:Optional[float] = None
    fee:Optional[float] = None
    rating:Optional[float] = None
    rating_count:Optional[int] = None
    image:Optional[str] = None
    total:Optional[int] = None
    car_rental:Optional[int] = None
    Insurance:Optional[int] = None
    tax:Optional[int] = None
    paid:Optional[int] = None
    dueCheck_out:Optional[int] = None
    acriss_id:UUID = uuid4()
    driver_detail_id:UUID = uuid4()
    t_cid:UUID = uuid4()
    inclusionid:UUID = uuid4()
    locationid:UUID = uuid4()
    class Config:
        orm_mode=True

class driver_detailBase(BaseModel):
    first_name:str
    last_name:str
    title:str
    email:str
    phone_code:str
    phone_number:int
    driver_age:int
    address:Optional[str]
    city:Optional[str]
    postal_code:Optional[str]
    country:Optional[str]
    remark:Optional[str]
    insurance_id:Optional[UUID] = None
    extra_id:Optional[UUID] = None
    class Config:
        orm_mode=True

class days_hoursBase(BaseModel):
    opening_hour:time
    closing_hour:time
    class Config:
        orm_mode=True

class daysBase(BaseModel):
    day_hour_id: UUID = uuid4()
    weekday:str
    is_closed:bool
    class Config:
        orm_mode=True

class vehicle_categoryBase(BaseModel):
    name:str
    class Config:
        orm_mode=True

class cancellationBase(BaseModel):
    reason:str
    charges:Optional[int]
    class Config:
        orm_mode=True

# @dataclass
# class modifiedData(BaseModel):
#     list2:List[inclusionBase]

def get_db():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session,Depends(get_db)]

# #create USers
# @app.post("/users/",status_code=status.HTTP_201_CREATED)
# async def create_user(user: UserBase, db: db_dependency):
#     db_user = models.user(**user.dict())
#     db.add(db_user)
#     db.commit()
#     return db_user


#locationSearch
@app.post("/locationSearch")
async def location_search(location: location_searchBase,db: Session = Depends(get_db)):
    query = db.query(models.vehicleClass)
    if location:
        query = query.filter(func.lower(models.vehicleClass.location_name) == func.lower(location.pick_up_locations))
        locationdata= query.all()
        
    if locationdata is None:
        raise HTTPException(status_code=404, detail="location not found")
    # vehicledata=db.query(models.locationClass).all()
    vehicledataList = []

    for vehicle in locationdata:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://127.0.0.1:8000/attribute/all")
            response1 = await client.get("http://127.0.0.1:8000/acrissById/771976e9-89d5-4da0-b49a-ca63261ef5db")
            response2= await client.get("http://127.0.0.1:8000/inclusion/all")
            # response3=await client.get("http://127.0.0.1:8000/locationById/1")
            attribute_data = response.json()
            acriss_data=response1.json()
            inclusion_data=response2.json()
            # location_data=response3.json()
            
        vehicledataList.append({
            "id": vehicle.id,
            "name": vehicle.name,
            "image": vehicle.image,
            "price": vehicle.price,
            "location":vehicle.location_name,
            "vehicle_type": vehicle.vehicle_type,
            "local_fee": vehicle.local_fee,
            "rating": vehicle.rating,
            "rating_count": vehicle.rating_count,
            "payment_method": vehicle.payment_method,
            "excess_amount": vehicle.excess_amount,
            "vehicle_group": vehicle.vehicle_group_id,
            # "location": location_data,
            "inclusion": inclusion_data,
            "attributes": attribute_data
        })
    
    return {'vehicledata':vehicledataList}

#ModifylocationSearch
@app.post("/modifylocationSearch")
async def location_search(location: modifysearchBase,db: Session = Depends(get_db)):
    query = db.query(models.vehicleClass)

    if location:
        query = query.filter(func.lower(models.vehicleClass.location_name) == func.lower(location.pick_up_locations))
        locationdata= query.all()
        
    if locationdata is None:
        raise HTTPException(status_code=404, detail="location not found")
    # vehicledata=db.query(models.locationClass).all()
    print(locationdata,"LocationData")
    vehicledataList = []
    for item in locationdata:
        if location.vehicle_type and location.paymentType:
            if any(v.lower() in item.vehicle_type.lower() for v in location.vehicle_type):
                vehicledataList.append(item)
        elif location.vehicle_type:
            if any(v.lower() in item.vehicle_type.lower() for v in location.vehicle_type):
                vehicledataList.append(item)
        elif location.paymentType:
            if any(v.lower() in item.payment_method.lower() for v in location.paymentType):
                vehicledataList.append(item)

                
        async with httpx.AsyncClient() as client:
            response = await client.get("http://127.0.0.1:8000/attribute/all")
            response1 = await client.get("http://127.0.0.1:8000/acrissById/771976e9-89d5-4da0-b49a-ca63261ef5db")
            response2= await client.get("http://127.0.0.1:8000/inclusion/all")
            # response3=await client.get("http://127.0.0.1:8000/locationById/1")
            attribute_data = response.json()
            acriss_data=response1.json()
            inclusion_data=response2.json()
            
    data=[]
    data.append({
        "inclusion":inclusion_data,
        "attribute":attribute_data
    })
   
    responseData=[]
    for data in vehicledataList:
        responseData.append({
            "id": data.id,
            "name": data.name,
            "image": data.image,
            "price": data.price,
            "location":data.location_name,
            "vehicle_type": data.vehicle_type,
            "local_fee": data.local_fee,
            "rating": data.rating,
            "rating_count": data.rating_count,
            "payment_method": data.payment_method,
            "excess_amount": data.excess_amount,
            "vehicle_group": data.vehicle_group_id,
            "inclusion": inclusion_data,
            "attributes": attribute_data
        })
    
    return {'vehicledata':responseData}


@app.post("/categoryVehicle")
async def vehicleCategory(cvehicle: categoryVehicle,db:Session=Depends(get_db)):
    query = db.query(models.vehicleClass)
    quer1=db.query(models.categoryClass)
    cataegory_data=quer1.all()
    
    if cvehicle:
        query = query.filter(models.vehicleClass.vehicle_type == cvehicle.name)
    vehicle_data= query.all()
    if vehicle_data is None:
        raise HTTPException(status_code=404, detail="vehicle cannot found for this category")
    vehicledataList = []
    for categoryvehicles in vehicle_data:
        vehicledataList.append({
            "Vehicle_name":categoryvehicles.name,
            "Vehicle_image":categoryvehicles.image,
            "Vehicle_category":categoryvehicles.vehicle_type
        })
    print(cataegory_data)
    return {'vehicledata':vehicledataList}



@app.post("/managebooking")
async def managebooking(managebooking:ManagebookingBase,db: Session = Depends(get_db)):
    query = db.query(models.booking_vehicleClass)
    # query1= db.query(models.driverDetailClass)
    if managebooking:
        query = query.filter(models.booking_vehicleClass.booking_ref == managebooking.booking_reference)
    bookingVehicledata= query.first()
    driverid=bookingVehicledata.driver_detail_id
    # print("+++++++++++++++++++++++",driverid)
    if managebooking:
        query = query.filter(models.driverDetailClass.email == managebooking.email and models.booking_vehicleClass.booking_ref == managebooking.booking_reference)
    bookingVehicledata= query.first()
    if bookingVehicledata is None:
        raise HTTPException(status_code=404, detail="bookings  not found")
    vehicledataList = []
    locations=[]
    drurl="http://127.0.0.1:8000/driver_detailId/"
    driverurl=urljoin(drurl,str(driverid))
    print("id",driverurl)
    async with httpx.AsyncClient() as client:
        response = await client.get("http://127.0.0.1:8000/rental_t_c/all")
        response1=await client.get("http://127.0.0.1:8000/locationById/9c08533a-71e5-40a4-b7c0-b02504b99f00")
        locationss=await client.get("http://127.0.0.1:8000/locationById/61d17365-12a0-4e4a-8c93-d567e42f00ab")
        response2=await client.get("http://127.0.0.1:8000/inclusion/all")
        response4=await client.get(driverurl)
        t_cdata = response.json()
        inclusion_data=response2.json()
        location1_data=response1.json()
        location2_data=locationss.json()
        driver_data=response4.json()
        locations.append({
                "location1":location1_data,
                "location2":location2_data
            })
        vehicledataList.append({
            "id":bookingVehicledata.id,
            "name":bookingVehicledata.name,
            "booking_ref":bookingVehicledata.booking_ref,
            "pickupDate":bookingVehicledata.pickup_Date,
            "dropoffDate":bookingVehicledata.dropoff_Date,
            "vehicle_type":bookingVehicledata.vehicle_type,
            "excess_amount":bookingVehicledata.excess_amount,
            "car_rental":bookingVehicledata.car_rental,
            "extra":300,
            "total":bookingVehicledata.total,
            "Insurance":bookingVehicledata.Insurance,
            "tax":bookingVehicledata.tax,
            "paid":bookingVehicledata.paid,
            "Due_at_Checkout":bookingVehicledata.dueCheck_out,
            "Fee":bookingVehicledata.fee,
            "Rating":bookingVehicledata.rating,
            "Rating_count":bookingVehicledata.rating_count,
            "image":bookingVehicledata.image,
            "location": locations,
            "inclusion": inclusion_data,
            "Rental_t_c": t_cdata,
            "driver_detail":driver_data
        })
    
    return {'vehicledata':vehicledataList}
                        



# create acriss
@app.post("/acriss",status_code=status.HTTP_201_CREATED,tags=["Acriss"])
async def create_acriss(acriss: AcrissBase, db: db_dependency):
    db_acriss = models.acrissClass(**acriss.dict())
    db.add(db_acriss)
    db.commit()
    return acriss


# #display vehicle by id
@app.get("/acrissById/{acriss_id}",status_code=status.HTTP_200_OK,tags=["Acriss"])
async def read_acriss(acriss_id:UUID, db:db_dependency):
    acriss=db.query(models.acrissClass).filter(models.acrissClass.id==acriss_id).first()   
    if acriss is None:
        raise HTTPException(status_code=404, detail='acriss not found')
    return {acriss}




#show all acriss
@app.get("/acriss/all",status_code=status.HTTP_200_OK,tags=["Acriss"])
async def get_All(db: Session = Depends(get_db)):
    acriss_data=db.query(models.acrissClass).all()
    return {'status':'sucess', 'acriss':acriss_data}

# @app.get("/acriss/{acriss_id}")
# def get_acriss_with_booking_vehicle(acriss_id: int, db: Session = Depends(get_db)):
#     acriss = db.query(models.acrissClass).filter(models.acrissClass.id == acriss_id).first()
#     if acriss is None:
#         raise HTTPException(status_code=404, detail="Acriss not found")
#     return {"acriss": acriss.name, "booking_vehicles": acriss.booking_vehicle}

# #show all acriss
# @app.get("/vehicles/all",status_code=status.HTTP_200_OK,tags=["vehicle"])
# async def get_All(db: Session = Depends(get_db)):
#     vehicle_data=db.query(models.vehicleClass).all()
#     for vehicle in vehicle_data:
#         vehicle.acriss
#     return vehicle.acriss



#delete Acriss
@app.delete("/acriss/{acriss_id}",status_code=status.HTTP_200_OK,tags=["Acriss"])
async def delete_acriss(acriss_id:UUID ,db:db_dependency):
    db_acriss=db.query(models.acrissClass).filter(models.acrissClass.id==acriss_id).first()
    if db_acriss is None:
        raise HTTPException(status_code=404 , detail="acriss was not founded")
    db.delete(db_acriss)
    db.commit()
    return db_acriss

#update acriss
@app.put("/acriss/{acriss_id}",status_code=status.HTTP_200_OK,response_model=AcrissBase,tags=["Acriss"])
async def update_acriss(acriss_id:int ,db:db_dependency,acriss:AcrissBase):
    try:
        db_acriss_update=db.query(models.acrissClass).filter(models.acrissClass.id==acriss_id).first()
        db_acriss_update.name=acriss.name
        db.add(db_acriss_update)
        db.commit()
        return db_acriss_update
    except:
        return HTTPException(status_code=404, detail="acriss not found")


# create acriss
@app.post("/inclusion",status_code=status.HTTP_201_CREATED,tags=["Inclusion"])
async def create_insclusion(inclusion: inclusionBase, db: db_dependency):
    db_inclusion = models.inclusionClass(**inclusion.dict())
    db.add(db_inclusion)
    db.commit()
    return inclusion

#show all acriss
@app.get("/inclusion/all",status_code=status.HTTP_200_OK,tags=["Inclusion"])
async def get_All(db: Session = Depends(get_db)):
    inclusion_data=db.query(models.inclusionClass).all()
    return {'insclusions':inclusion_data}

# #display vehicle by id
@app.get("/inclusionById/{inclusion_id}",status_code=status.HTTP_200_OK,tags=["Inclusion"])
async def read_inclusion(inclusion_id:UUID, db:db_dependency):
    insclusion=db.query(models.inclusionClass).filter(models.inclusionClass.id==inclusion_id).first()   
    if insclusion is None:
        raise HTTPException(status_code=404, detail='insclusion not found')
    return {insclusion}

#delete location
@app.delete("/inclusion/{inclusion_id}",status_code=status.HTTP_200_OK,tags=["Inclusion"])
async def delete_location(inclusion_id:UUID ,db:db_dependency):
    db_location=db.query(models.inclusionClass).filter(models.inclusionClass.id==inclusion_id).first()
    if db_location is None:
        raise HTTPException(status_code=404 , detail="inclsuin was not founded")
    db.delete(db_location)
    db.commit()
    return db_location


# create vehicle
@app.post("/vehicleInsert",status_code=status.HTTP_201_CREATED,tags=["vehicle"])
async def create_vehicle(vehicle: vehicleBase, db: db_dependency):
    db_vehicle = models.vehicleClass(**vehicle.dict())
    db.add(db_vehicle)
    db.commit()
    return {'vehicles':vehicle}

#show all vehicle
@app.get("/vehicle/all",status_code=status.HTTP_200_OK,tags=["vehicle"])
async def get_All(db: Session = Depends(get_db)):
    vehicledata=db.query(models.vehicleClass).all()
    return {'status':'sucess', 'vehicles':vehicledata}


#show all vehicle
@app.post("/vehicle",status_code=status.HTTP_200_OK,tags=["vehicle"])
async def vehicleSearch(db: Session = Depends(get_db)):
    vehicledata=db.query(models.vehicleClass).all()
    return {'status':'sucess', 'vehicles':vehicledata}
        

#show all vehicle
@app.get("/vehicleSearched",status_code=status.HTTP_200_OK,tags=["vehicle"])
async def get_All(db: Session = Depends(get_db)):
    vehicledata=db.query(models.vehicleClass).all()
    vehicledataList = []
    for vehicle in vehicledata:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://127.0.0.1:8000/attribute/all")
            response1 = await client.get("http://127.0.0.1:8000/acrissById/771976e9-89d5-4da0-b49a-ca63261ef5db")
            response2= await client.get("http://127.0.0.1:8000/inclusion/all")
            # response3=await client.get("http://127.0.0.1:8000/locationById/1")
            attribute_data = response.json()
            acriss_data=response1.json()
            inclusion_data=response2.json()
            # location_data=response3.json()
            
        vehicledataList.append({
            "id": vehicle.id,
            "name": vehicle.name,
            "image": vehicle.image,
            "price": vehicle.price,
            "location":vehicle.location_name,
            "vehicle_type": vehicle.vehicle_type,
            "local_fee": vehicle.local_fee,
            "rating": vehicle.rating,
            "rating_count": vehicle.rating_count,
            "payment_method": vehicle.payment_method,
            "excess_amount": vehicle.excess_amount,
            "vehicle_group": vehicle.vehicle_group_id,
            "inclusion": inclusion_data,
            "attributes": attribute_data
        })
    
    return {'vehicledata':vehicledataList}


#delete vehicle
@app.delete("/vehicle/{vehicle_id}",status_code=status.HTTP_200_OK,tags=["vehicle"])
async def delete_vehicle(vehcile_id:UUID ,db:db_dependency):
    db_vehicle=db.query(models.vehicleClass).filter(models.vehicleClass.id==vehcile_id).first()
    if db_vehicle is None:
        raise HTTPException(status_code=404 , detail="vehcile was not founded")
    db.delete(db_vehicle)
    db.commit()
    return db_vehicle

# #display vehicle by id
@app.get("/vehicleById/{vehicle_id}",status_code=status.HTTP_200_OK,tags=["vehicle"])
async def read_vehicle(vehicle_id:UUID, db:db_dependency):
    vehicle=db.query(models.vehicleClass).filter(models.vehicleClass.id==vehicle_id).first()   
    if vehicle is None:
        raise HTTPException(status_code=404, detail='vehicle not found')
    return {"vehicle": vehicle}


# #show all acriss
@app.get("/vehicleById",status_code=status.HTTP_200_OK,tags=["vehicle"])
async def read_vehicle(vehicle_id:UUID, db:db_dependency):
    vehicle=db.query(models.vehicleClass).filter(models.vehicleClass.id==vehicle_id).first()   
    if vehicle is None:
        raise HTTPException(status_code=404, detail='vehicle not found')
    return {"vehicle": vehicle}


#update vehicle
@app.put("/vehicle/{vehcile_id}",status_code=status.HTTP_200_OK,response_model=vehicleBase,tags=["vehicle"])
async def update_vehicle(vehicle_id:UUID ,db:db_dependency,vehicle:vehicleBase):
    try:
        db_vehcile_update=db.query(models.vehicleClass).filter(models.vehicleClass.id==vehicle_id).first()
        db_vehcile_update.id=vehicle.id
        db_vehcile_update.name=vehicle.name
        db_vehcile_update.vehicle_type=vehicle.vehicle_type
        db_vehcile_update.excess_amount=vehicle.excess_amount
        db_vehcile_update.local_fee=vehicle.local_fee
        db_vehcile_update.price=vehicle.price
        db_vehcile_update.image=vehicle.image
        db_vehcile_update.rating=vehicle.rating
        db_vehcile_update.payment_method=vehicle.payment_method
        db_vehcile_update.rating_count=vehicle.rating_count
        db.add(db_vehcile_update)
        db.commit()
        return db_vehcile_update
    except:
        return HTTPException(status_code=404, detail="vehicle can't update ")



# create locations
@app.post("/location",status_code=status.HTTP_201_CREATED,tags=["Locations"])
async def create_location(location: locationBase, db: db_dependency):
    db_location = models.locationClass(**location.dict())
    db.add(db_location)
    db.commit()
    return location

#show all loctaions
@app.get("/locations",status_code=status.HTTP_200_OK)
async def get_All(db: Session = Depends(get_db)):
    locations_data=db.query(models.locationClass).all()
    return {'locations':locations_data}

# #display location by id
@app.get("/locationById/{location_id}",status_code=status.HTTP_200_OK,tags=["Locations"])
async def read_vehicle(location_id:UUID, db:db_dependency):
    location=db.query(models.locationClass).filter(models.locationClass.id==location_id).first()   
    if location is None:
        raise HTTPException(status_code=404, detail='location not found')
    return {location}

# #display location with 
@app.get("/locationByIdDays/{location_id}",status_code=status.HTTP_200_OK,tags=["Locations"])
async def read_vehicle(location_id:UUID, db:db_dependency):
    location=db.query(models.locationClass).filter(models.locationClass.id==location_id).first()
    locationdataList = []
    async with httpx.AsyncClient() as client:
            response = await client.get("http://127.0.0.1:8000/day_hoursById/1")
            response1 = await client.get("http://127.0.0.1:8000/daysById/1")
            dayHours_data = response.json()
            days_data=response1.json()
            
            locationdataList.append({
            "id": location.id,
            "name": location.location_name,
            "day_hour": dayHours_data,
            "days":days_data
        })
    
    return {'Locations':locationdataList}

#update locations
@app.put("/location/{location_id}",status_code=status.HTTP_200_OK,response_model=locationBase,tags=["Locations"])
async def update_location(location_id:UUID ,db:db_dependency,location:locationBase):
    try:
        db_location_update=db.query(models.locationClass).filter(models.locationClass.id==location_id).first()
        db_location_update.location_name=location.location_name
        db_location_update.days=location.days
        db_location_update.image=location.image
        db.add(db_location_update)
        db.commit()
        return db_location_update
    except:
        return HTTPException(status_code=404, detail="location not found")

#delete location
@app.delete("/location/{location_id}",status_code=status.HTTP_200_OK,tags=["Locations"])
async def delete_location(location_id:UUID ,db:db_dependency):
    db_location=db.query(models.locationClass).filter(models.locationClass.id==location_id).first()
    if db_location is None:
        raise HTTPException(status_code=404 , detail="location was not founded")
    db.delete(db_location)
    db.commit()
    return db_location

# create days_hours
@app.post("/days_hours",status_code=status.HTTP_201_CREATED,tags=["Locations"])
async def create_days_hours(day_hours: days_hoursBase, db: db_dependency):
    db_days_hours = models.days_hoursClass(**day_hours.dict())
    db.add(db_days_hours)
    db.commit()
    return day_hours

#show all days_hours
@app.get("/days_hours",status_code=status.HTTP_200_OK,tags=["Locations"])
async def get_All(db: Session = Depends(get_db)):
    days_hours_data=db.query(models.days_hoursClass).all()
    return {'status':'sucess', 'days_hours':days_hours_data}


# #display day_hours by id
@app.get("/day_hoursById/{day_hours_id}",status_code=status.HTTP_200_OK,tags=["Locations"])
async def read_day_hours(day_hours_id:UUID, db:db_dependency):
    day_hours=db.query(models.days_hoursClass).filter(models.days_hoursClass.id==day_hours_id).first()   
    if day_hours is None:
        raise HTTPException(status_code=404, detail='day_hours not found')
    return {"day_hours": day_hours}

#update locations
@app.put("/days_hours/{days_hours_id}",status_code=status.HTTP_200_OK,response_model=days_hoursBase,tags=["Locations"])
async def update_days_hours(days_hours_id:UUID ,db:db_dependency,days_hours:days_hoursBase):
    try:
        db_days_hours_update=db.query(models.days_hoursClass).filter(models.days_hoursClass.id==days_hours_id).first()
        db_days_hours_update.opening_hour=days_hours.opening_hour
        db_days_hours_update.closing_hour=days_hours.closing_hour
        db.add(db_days_hours_update)
        db.commit()
        return db_days_hours_update
    except:
        return HTTPException(status_code=404, detail="days_hours  not found")

#delete location
@app.delete("/days_hours/{days_hours_id}",status_code=status.HTTP_200_OK,tags=["Locations"])
async def delete_days_hours(days_hours_id:UUID ,db:db_dependency):
    db_days_hours=db.query(models.days_hoursClass).filter(models.days_hoursClass.id==days_hours_id).first()
    if db_days_hours is None:
        raise HTTPException(status_code=404 , detail="days_hours was not founded")
    db.delete(db_days_hours)
    db.commit()
    return db_days_hours




# create days
@app.post("/days",status_code=status.HTTP_201_CREATED,tags=["Locations"])
async def create_days(day: daysBase, db: db_dependency):
    db_day = models.daysClass(**day.dict())
    db.add(db_day)
    db.commit()
    return {'status':'sucess', 'booking_vehicles':day}


#show all days
@app.get("/days",status_code=status.HTTP_200_OK,tags=["Locations"])
async def get_All(db: Session = Depends(get_db)):
    days_data=db.query(models.daysClass).all()
    return {'status':'sucess', 'day_Data':days_data}

# #display days by id
@app.get("/daysById/{days_id}",status_code=status.HTTP_200_OK,tags=["Locations"])
async def read_days(days_id:UUID, db:db_dependency):
    days=db.query(models.daysClass).filter(models.daysClass.id==days_id).first()   
    if days is None:
        raise HTTPException(status_code=404, detail='days not found')
    return {"days": days}

#update days
@app.put("/days/{day_id}",status_code=status.HTTP_200_OK,response_model=daysBase,tags=["Locations"])
async def update_days(day_id:UUID ,db:db_dependency,days:daysBase):
    try:
        db_days_update=db.query(models.daysClass).filter(models.daysClass.id==day_id).first()
        db_days_update.weekday=days.weekday
        db_days_update.is_closed=days.is_closed
        db_days_update.day_hour_id=days.day_hour_id
        db.add(db_days_update)
        db.commit()
        return db_days_update
    except:
        return HTTPException(status_code=404, detail="days not found")

#delete days
@app.delete("/days/{days_id}",status_code=status.HTTP_200_OK,tags=["Locations"])
async def delete_days(days_id:UUID ,db:db_dependency):
    db_days=db.query(models.daysClass).filter(models.daysClass.id==days_id).first()
    if db_days is None:
        raise HTTPException(status_code=404 , detail="days was not founded")
    db.delete(db_days)
    db.commit()
    return db_days




# create vehicle_group
@app.post("/vehicleGroup",status_code=status.HTTP_201_CREATED,tags=["vehicle Group"])
async def create_vehicleGroup(vehicleGroup: vehicleGroupBase, db: db_dependency):
    db_vehicleGroup = models.vehicleGroupClass(**vehicleGroup.dict())
    db.add(db_vehicleGroup)
    db.commit()
    return vehicleGroup

#show all vehile_group
@app.get("/vehicleGroup",status_code=status.HTTP_200_OK,tags=["vehicle Group"])
async def get_All(db: Session = Depends(get_db)):
    vehicle_group_data=db.query(models.vehicleGroupClass).all()
    return {'status':'sucess', 'vehicle_groups':vehicle_group_data}

# #display vehile_group by id
@app.get("/vehile_groupById/{vehile_group_id}",status_code=status.HTTP_200_OK,tags=["vehicle Group"])
async def read_vehile_group(vehile_group_id:UUID, db:db_dependency):
    vehile_group=db.query(models.vehicleGroupClass).filter(models.vehicleGroupClass.id==vehile_group_id).first()   
    if vehile_group is None:
        raise HTTPException(status_code=404, detail='vehile_group not found')
    return {"vehicle_group": vehile_group}


#update vehicleGroup
@app.put("/vehicleGroup/{vehicleGroup_id}",status_code=status.HTTP_200_OK,response_model=vehicleGroupBase,tags=["vehicle Group"])
async def update_vehicleGroup(vehicleGroup_id:UUID ,db:db_dependency,vehicleGroup:vehicleGroupBase):
    try:
        db_vehicleGroup_update=db.query(models.vehicleGroupClass).filter(models.vehicleGroupClass.id==vehicleGroup_id).first()
        db_vehicleGroup_update.name=vehicleGroup.name
        db.add(db_vehicleGroup_update)
        db.commit()
        return db_vehicleGroup_update
    except:
        return HTTPException(status_code=404, detail="vehicleGroup not found")

#delete vehicleGroup
@app.delete("/vehicleGroup/{vehicleGroup_id}",status_code=status.HTTP_200_OK,tags=["vehicle Group"])
async def delete_vehicleGroup(vehicleGroup_id:UUID ,db:db_dependency):
    db_vehicleGroup=db.query(models.vehicleGroupClass).filter(models.vehicleGroupClass.id==vehicleGroup_id).first()
    if db_vehicleGroup is None:
        raise HTTPException(status_code=404 , detail="vehicleGroup was not founded")
    db.delete(db_vehicleGroup)
    db.commit()
    return db_vehicleGroup



# create t_c
@app.post("/t_c",status_code=status.HTTP_201_CREATED,tags=["T & C"])
async def create_t_c(t_c: t_cBase, db: db_dependency):
    db_t_c = models.t_cClass(**t_c.dict())
    db.add(db_t_c)
    db.commit()
    return t_c

#show all t_c
@app.get("/t_c/all",status_code=status.HTTP_200_OK,tags=["T & C"])
async def get_All(db: Session = Depends(get_db)):
    t_c_data=db.query(models.t_cClass).all()
    return {'t_c':t_c_data}


# #display t&c by id
@app.get("/t&cById/{t_c_id}",status_code=status.HTTP_200_OK,tags=["T & C"])
async def read_t_c(t_c_id:UUID, db:db_dependency):
    t_c=db.query(models.t_cClass).filter(models.t_cClass.id==t_c_id).first()   
    if t_c is None:
        raise HTTPException(status_code=404, detail='t_c not found')
    return {"t_c": t_c}

#update t&c
@app.put("/t_c/{t_c_id}",status_code=status.HTTP_200_OK,response_model=t_cBase,tags=["T & C"])
async def update_t_c(t_c_id:UUID ,db:db_dependency,t_c:t_cBase):
    try:
        db_t_c_update=db.query(models.t_cClass).filter(models.t_cClass.id==t_c_id).first()
        db_t_c_update.title=t_c.title
        db_t_c_update.description=t_c.description
        db.add(db_t_c_update)
        db.commit()
        return db_t_c_update
    except:
        return HTTPException(status_code=404, detail="t_c not found")

#delete t&c
@app.delete("/t_c/{t_c_id}",status_code=status.HTTP_200_OK,tags=["T & C"])
async def delete_t_c(t_c_id:UUID ,db:db_dependency):
    db_t_c=db.query(models.t_cClass).filter(models.t_cClass.id==t_c_id).first()
    if db_t_c is None:
        raise HTTPException(status_code=404 , detail="t_c was not founded")
    db.delete(db_t_c)
    db.commit()
    return db_t_c

# create attribute
@app.post("/attribute",status_code=status.HTTP_201_CREATED,tags=["Attribute"])
async def create_attribute(attribute: attributeBase, db: db_dependency):
    db_attribute = models.attributeClass(**attribute.dict())
    db.add(db_attribute)
    db.commit()
    return attribute

#show all attribute
@app.get("/attribute/all",status_code=status.HTTP_200_OK,tags=["Attribute"])
async def get_All(db: Session = Depends(get_db)):
    attribute_data=db.query(models.attributeClass).all()
    return {'attributes':attribute_data}

# #display attribute by id
@app.get("/attributeId/{attribute_id}",status_code=status.HTTP_200_OK,tags=["Attribute"])
async def readattribute(attribute_id:int, db:db_dependency):
    attribute=db.query(models.attributeClass).filter(models.attributeClass.id==attribute_id).first()   
    if attribute is None:
        raise HTTPException(status_code=404, detail='attribute not found')
    return {attribute}

#update attribute
@app.put("/attribute/{attribute_id}",status_code=status.HTTP_200_OK,response_model=attributeBase,tags=["Attribute"])
async def update_attribute(attribute_id:int ,db:db_dependency,attribute:attributeBase):
    try:
        db_attribute_update=db.query(models.attributeClass).filter(models.attributeClass.id==attribute_id).first()
        db_attribute_update.attribute_name=attribute.attribute_name
        db.add(db_attribute_update)
        db.commit()
        return db_attribute_update
    except:
        return HTTPException(status_code=404, detail="t_c not found")

#delete attribute
@app.delete("/attribute/{attribute_id}",status_code=status.HTTP_200_OK,tags=["Attribute"])
async def delete_attribute(attribute_id:int ,db:db_dependency):
    db_attribute=db.query(models.attributeClass).filter(models.attributeClass.id==attribute_id).first()
    if db_attribute is None:
        raise HTTPException(status_code=404 , detail="attribute was not founded")
    db.delete(db_attribute)
    db.commit()
    return db_attribute




# create extra
@app.post("/extra",status_code=status.HTTP_201_CREATED,tags=["Extra"])
async def create_extra(extras: extraBase, db: db_dependency):
    db_extra = models.extraClass(**extras.dict())
    db.add(db_extra)
    db.commit()
    return {'extras':extras}

#show all extra
@app.get("/extra/all",status_code=status.HTTP_200_OK,tags=["Extra"])
async def get_All(db: Session = Depends(get_db)):
    extras_data=db.query(models.extraClass).all()
    return {"extra":extras_data}

# #display extra by id
@app.get("/extraId/{extra_id}",status_code=status.HTTP_200_OK,tags=["Extra"])
async def readextra(extra_id:int, db:db_dependency):
    extra=db.query(models.extraClass).filter(models.extraClass.id==extra_id).first()   
    if extra is None:
        raise HTTPException(status_code=404, detail='extra not found')
    return {extra}


#update extra
@app.put("/extra/{extra_id}",status_code=status.HTTP_200_OK,response_model=extraBase,tags=["Extra"])
async def update_extra(extra_id:int ,db:db_dependency,extra:extraBase):
    try:
        db_extra_update=db.query(models.extraClass).filter(models.extraClass.id==extra_id).first()
        db_extra_update.name=extra.name
        db_extra_update.type=extra.type
        db_extra_update.quantity=extra.quantity
        db_extra_update.image=extra.image
        db_extra_update.amount=extra.amount
        db.add(db_extra_update)
        db.commit()
        return db_extra_update
    except:
        return HTTPException(status_code=404, detail="t_c not found")

#delete EXTRA
@app.delete("/extra/{extra_id}",status_code=status.HTTP_200_OK,tags=["Extra"])
async def delete_extra(extra_id:int ,db:db_dependency):
    db_extra=db.query(models.extraClass).filter(models.extraClass.id==extra_id).first()
    if db_extra is None:
        raise HTTPException(status_code=404 , detail="extra was not founded")
    db.delete(db_extra)
    db.commit()
    return db_extra



# create insurance
@app.post("/insurance",status_code=status.HTTP_201_CREATED,tags=["Insurances"])
async def create_insurance(insurance: insuranceBase, db: db_dependency):
    db_insurance = models.insuranceClass(**insurance.dict())
    db.add(db_insurance)
    db.commit()
    return {'status':'sucess', 'insurances':insurance}

#show all insurance
@app.get("/insurance/all",status_code=status.HTTP_200_OK,tags=["Insurances"])
async def get_All(db: Session = Depends(get_db)):
    insurances_data=db.query(models.insuranceClass).all()
    return {'status':'sucess', 'insurances':insurances_data}

# #display insurance by id
@app.get("/insuranceId/{insurance_id}",status_code=status.HTTP_200_OK,tags=["Insurances"])
async def readinsurance(insurance_id:UUID, db:db_dependency):
    insurance=db.query(models.insuranceClass).filter(models.insuranceClass.id==insurance_id).first()   
    if insurance is None:
        raise HTTPException(status_code=404, detail='insurance not found')
    return {insurance}

#update insurance
@app.put("/insurance/{insurance_id}",status_code=status.HTTP_200_OK,response_model=insuranceBase,tags=["Insurances"])
async def update_insurance(insurance_id:UUID ,db:db_dependency,insurance:insuranceBase):
    try:
        db_insurance_update=db.query(models.insuranceClass).filter(models.insuranceClass.id==insurance_id).first()
        db_insurance_update.name=insurance.name
        db_insurance_update.type=insurance.type
        db_insurance_update.amount=insurance.amount
        db_insurance_update.description=insurance.description
        db.add(db_insurance_update)
        db.commit()
        return db_insurance_update
    except:
        return HTTPException(status_code=404, detail="insurance not found")

#delete insurance
@app.delete("/insurance/{insurance_id}",status_code=status.HTTP_200_OK,tags=["Insurances"])
async def delete_insurance(insurance_id:UUID ,db:db_dependency):
    db_insurance=db.query(models.insuranceClass).filter(models.insuranceClass.id==insurance_id).first()
    if db_insurance is None:
        raise HTTPException(status_code=404 , detail="insurance was not founded")
    db.delete(db_insurance)
    db.commit()
    return db_insurance


# create booking_vehicle
@app.post("/booking_vehicle",status_code=status.HTTP_201_CREATED,tags=["booking vehicle"])
async def create_booking_vehicle(booking_vehicle: booking_vehicleBase, db: db_dependency):
    db_booking_vehicle = models.booking_vehicleClass(**booking_vehicle.dict())
    db.add(db_booking_vehicle)
    db.commit()
    return {'status':'sucess', 'booking_vehicles':booking_vehicle}

#show all booking_vehicle
@app.get("/booking_vehicle/all",status_code=status.HTTP_200_OK,tags=["booking vehicle"])
async def get_All(db: Session = Depends(get_db)):
    booking_vehicle_data=db.query(models.booking_vehicleClass).all()
    return {'booking_vehicle':booking_vehicle_data}

#show all booking_vehicle
@app.get("/booking_conformation",status_code=status.HTTP_200_OK)
async def get_conformation(db: Session = Depends(get_db)):
    booking_vehicles=db.query(models.booking_vehicleClass).all()
    booking_vehicle_data=booking_vehicles[-1]
    # tc=db.query(models.t_cClass).all()
    driverid=booking_vehicle_data.driver_detail_id
    drurl="http://127.0.0.1:8000/driver_detailId/"
    driverurl=urljoin(drurl,str(driverid))
    print("id",driverurl)
    vehicledataList = []
    locations=[]
    async with httpx.AsyncClient() as client:
            response1= await client.get("http://127.0.0.1:8000/inclusion/all")
            response2=await client.get("http://127.0.0.1:8000/locationById/9c08533a-71e5-40a4-b7c0-b02504b99f00")
            locationss=await client.get("http://127.0.0.1:8000/locationById/bfc8c292-1a1c-4cde-b162-72e4a5543cc2")
            response3=await client.get("http://127.0.0.1:8000/driver_detail_latest")
            response4=await client.get("http://127.0.0.1:8000/t_c/all")
            inclusion_data= response1.json()
            location1_data=response2.json()
            location2_data=locationss.json()
            driver_detail_data=response3.json()
            t_c_data=response4.json()
            locations.append({
                "loacation1":location1_data,
                "location2":location2_data
            })
            vehicledataList.append({
            "id": booking_vehicle_data.id,
            "name": booking_vehicle_data.name,
            "vehicle_type":booking_vehicle_data.vehicle_type,
            "booking_reference" :booking_vehicle_data.booking_ref,
            "pickupDate":booking_vehicle_data.pickup_Date,
            "dropoffDate":booking_vehicle_data.dropoff_Date,
            "excess_amount": booking_vehicle_data.excess_amount,
            "car_rental":booking_vehicle_data.car_rental,
            "Insurance":booking_vehicle_data.Insurance,
            "tax":booking_vehicle_data.tax,
            "paid":booking_vehicle_data.paid,
            "Due_at_Checkout":booking_vehicle_data.dueCheck_out,
            "Fee": booking_vehicle_data.fee,
            "rating": booking_vehicle_data.rating,
            "rating_count":booking_vehicle_data.rating_count,
            "image":booking_vehicle_data.image,
            "locations": locations,
            "inclusion": inclusion_data,
            "t_c": t_c_data,
            "drivers":driver_detail_data
        })
            print(vehicledataList)
    
    return {'ConformationData':vehicledataList}
    


# #display booking_vehicle by id
@app.get("/booking_vehicleId/{booking_vehicle}",status_code=status.HTTP_200_OK,tags=["booking vehicle"])
async def readbooking_vehicle(booking_vehicle_id:UUID, db:db_dependency):
    booking_vehicle=db.query(models.booking_vehicleClass).filter(models.booking_vehicleClass.id==booking_vehicle_id).first()   
    if booking_vehicle is None:
        raise HTTPException(status_code=404, detail='booking_vehicle not found')
    return {"booking_vehicle": booking_vehicle}


#update booking_vehicle
@app.put("/booking_vehicle/{booking_vehicle_id}",status_code=status.HTTP_200_OK,response_model=booking_vehicleBase,tags=["booking vehicle"])
async def update_booking_vehicle(booking_vehicle_id:UUID ,db:db_dependency,booking_vehicle:booking_vehicleBase):
    try:
        db_booking_vehicle_update=db.query(models.booking_vehicleClass).filter(models.booking_vehicleClass.id==booking_vehicle_id).first()
        db_booking_vehicle_update.name=booking_vehicle.name
        db_booking_vehicle_update.booking_ref=booking_vehicle.booking_ref
        db_booking_vehicle_update.vehicle_type=booking_vehicle.vehicle_type
        db_booking_vehicle_update.excess_amount=booking_vehicle.excess_amount
        db_booking_vehicle_update.fee=booking_vehicle.fee
        db_booking_vehicle_update.rating=booking_vehicle.rating
        db_booking_vehicle_update.rating_count=booking_vehicle.rating_count
        db_booking_vehicle_update.image=booking_vehicle.image
        db.add(db_booking_vehicle_update)
        db.commit()
        return db_booking_vehicle_update
    except:
        return HTTPException(status_code=404, detail="booking_vehicle not found")




# @app.get("/acriss")
# def get_acriss_with_booking_vehicle(db: Session = Depends(get_db)):
#     acriss = db.query(models.acrissClass).all()
#     return {"acriss": acriss, "booking_vehicles": acriss.booking_vehicle}


#delete boking_vehicle
@app.delete("/booking_vehicle/{booking_vehicle_id}",status_code=status.HTTP_200_OK,tags=["booking vehicle"])
async def delete_booking_vehicle(booking_vehicle_id:UUID ,db:db_dependency):
    db_booking_vehicle=db.query(models.booking_vehicleClass).filter(models.booking_vehicleClass.id==booking_vehicle_id).first()
    if db_booking_vehicle is None:
        raise HTTPException(status_code=404 , detail="booking_vehicle was not founded")
    db.delete(db_booking_vehicle)
    db.commit()
    return booking_vehicle_id 


# create driver_detail
@app.post("/driver_Detail",status_code=status.HTTP_201_CREATED,tags=["Driver_Details"])
async def create_driver_detail(driver: driver_detailBase, db: db_dependency):
    db_driver = models.driverDetailClass(**driver.dict())
    db.add(db_driver)
    db.commit()
    return driver

@app.get("/driver_detail_latest",status_code=status.HTTP_200_OK,tags=["Driver_Details"])
async def get_All(db: Session = Depends(get_db)):
    driver_data=db.query(models.driverDetailClass).all()
    return {"driver_detail":driver_data[-1]}

#show all days
@app.get("/driver_detail",status_code=status.HTTP_200_OK,tags=["Driver_Details"])
async def get_All(db: Session = Depends(get_db)):
    driver_data=db.query(models.driverDetailClass).all()
    return driver_data

# #display driver_detail by id
@app.get("/driver_detailId/{driver_detail_id}",status_code=status.HTTP_200_OK,tags=["Driver_Details"])
async def read_driver_detail(driver_detail_id:UUID, db:db_dependency):
    driver_detail=db.query(models.driverDetailClass).filter(models.driverDetailClass.id==driver_detail_id).first()   
    if driver_detail is None:
        raise HTTPException(status_code=404, detail='driver_detail not found')
    return {"driver_detail": driver_detail}


#update days
@app.put("/driver_detail/{driver_detail_id}",status_code=status.HTTP_200_OK,response_model=driver_detailBase,tags=["Driver_Details"])
async def update_days(driver_detail_id:UUID ,db:db_dependency,drivers_detail:driver_detailBase):
    try:
        db_driver_detail_update=db.query(models.driverDetailClass).filter(models.driverDetailClass.id==driver_detail_id).first()
        db_driver_detail_update.first_name=drivers_detail.first_name
        db_driver_detail_update.last_name=drivers_detail.last_name
        db_driver_detail_update.title=drivers_detail.title
        db_driver_detail_update.email=drivers_detail.email
        db_driver_detail_update.phone_code=drivers_detail.phone_code
        db_driver_detail_update.phone_number=drivers_detail.phone_number
        db_driver_detail_update.driver_age=drivers_detail.driver_age
        db_driver_detail_update.address=drivers_detail.address
        db_driver_detail_update.city=drivers_detail.city
        db_driver_detail_update.postal_code=drivers_detail.postal_code
        db_driver_detail_update.country=drivers_detail.country
        db_driver_detail_update.remark=drivers_detail.remark
        

        db.add(db_driver_detail_update)
        db.commit()
        return db_driver_detail_update
    except:
        return HTTPException(status_code=404, detail="driver_details not found")

#delete driver_Detail
@app.delete("/driver_detail/{driver_detail_id}",status_code=status.HTTP_200_OK,tags=["Driver_Details"])
async def delete_driver_details(driver_detail_id:UUID ,db:db_dependency):
    db_driver_details=db.query(models.driverDetailClass).filter(models.driverDetailClass.id==driver_detail_id).first()
    if db_driver_details is None:
        raise HTTPException(status_code=404 , detail="driverDetail was not founded")
    db.delete(db_driver_details)
    db.commit()
    return driver_detail_id




# create cancelalation_Charges
@app.post("/cancellation",status_code=status.HTTP_201_CREATED)
async def create_cancellation(cancellation: cancellationBase, db: db_dependency):
    db_cancellation = models.cancellationClass(**cancellation.dict())
    db.add(db_cancellation)
    db.commit()
    return cancellation


# #display cancelalation_Charges by id
@app.get("/cancellationById/{cancellation_id}",status_code=status.HTTP_200_OK)
async def read_cancellation(cancellation_id: UUID, db:db_dependency):
    cancellation=db.query(models.cancellationClass).filter(models.cancellationClass.id==cancellation_id).first()   
    if cancellation is None:
        raise HTTPException(status_code=404, detail='cancellation not found')
    return {cancellation}



#show all cancelalation_Charges
@app.get("/cancellation/all",status_code=status.HTTP_200_OK,tags=["Cancellation"])
async def get_All(db: Session = Depends(get_db)):
    cancellation_data=db.query(models.cancellationClass).all()
    return {'cancellations':cancellation_data}



#delete cancelalation_Charges
@app.delete("/cancellation/{cancellation_id}",status_code=status.HTTP_200_OK,tags=["Cancellation"])
async def delete_cancellation(cancellation_id:UUID ,db:db_dependency):
    db_cancellation=db.query(models.cancellationClass).filter(models.cancellationClass.id==cancellation_id).first()
    if db_cancellation is None:
        raise HTTPException(status_code=404 , detail="cancellation was not founded")
    db.delete(db_cancellation)
    db.commit()
    return cancellation_id

#update cancelalation_Charges
@app.put("/cancellation/{cancellation_id}",status_code=status.HTTP_200_OK,response_model=cancellationBase,tags=["Cancellation"])
async def update_cancellation(cancellation_id:UUID ,db:db_dependency,cancellation:cancellationBase):
    try:
        db_cancellation_update=db.query(models.cancellationClass).filter(models.cancellationClass.id==cancellation_id).first()
        db_cancellation_update.reason=cancellation.reason
        db_cancellation_update.charges=cancellation.charges
        db.add(db_cancellation_update)
        db.commit() 
        return db_cancellation_update
    except:
        return HTTPException(status_code=404, detail="cancellation not found")



#modify
@app.put("/modifyBooking/{booking_vehicle_id}",status_code=status.HTTP_200_OK,response_model=booking_vehicleBase)
async def update_booking_vehicle(booking_vehicle_id:UUID ,db:db_dependency,booking_vehicle:booking_vehicleBase):
    try:
        db_booking_vehicle_update=db.query(models.booking_vehicleClass).filter(models.booking_vehicleClass.id==booking_vehicle_id).first()
        db_booking_vehicle_update.name=booking_vehicle.name
        db_booking_vehicle_update.booking_ref=booking_vehicle.booking_ref
        db_booking_vehicle_update.vehicle_type=booking_vehicle.vehicle_type
        db_booking_vehicle_update.excess_amount=booking_vehicle.excess_amount
        db_booking_vehicle_update.fee=booking_vehicle.fee
        db_booking_vehicle_update.rating=booking_vehicle.rating
        db_booking_vehicle_update.rating_count=booking_vehicle.rating_count
        db_booking_vehicle_update.image=booking_vehicle.image
        db.add(db_booking_vehicle_update)
        db.commit()
        return db_booking_vehicle_update
    except:
        return HTTPException(status_code=404, detail="booking_vehicle not found")


# #display booking_vehicle by id
@app.get("/modifiedData/{booking_vehicle_id}",status_code=status.HTTP_200_OK)
async def readbooking_vehicle(booking_vehicle_id:UUID, db:db_dependency):
    booking_vehicle=db.query(models.booking_vehicleClass).filter(models.booking_vehicleClass.id==booking_vehicle_id).first()
    driverid=booking_vehicle.driver_detail_id
    drurl="http://127.0.0.1:8000/driver_detailId/"
    driverurl=urljoin(drurl,str(driverid))
    async with httpx.AsyncClient() as client:
            response1= await client.get("http://127.0.0.1:8000/inclusion/all")
            response2= await client.get("http://127.0.0.1:8000/attribute/all")
            response3=await client.get("http://127.0.0.1:8000/locationById/69823c50-c87d-4f7e-820b-26657eba3ee4")
            locationss=await client.get("http://127.0.0.1:8000/locationById/bfc8c292-1a1c-4cde-b162-72e4a5543cc2")
            response4=await client.get(driverurl)
            response5=await client.get("http://127.0.0.1:8000/extra/all")
            response6=await client.get("http://127.0.0.1:8000/insuranceId/cceb9b84-eba1-48b8-ab51-91cb4847cd26")
            response7=await client.get("http://127.0.0.1:8000/insuranceId/a5fb4cf1-de9c-43e4-8b03-c5000dae6ab1")
            inclusionData=response1.json()
            attributeData=response2.json()
            location1_data=response3.json()
            location2_data=locationss.json()
            driverData=response4.json()
            extras=response5.json()
            insurance1_data=response6.json()
            insurance2_data=response7.json()
    modifiedData=[]
    locations=[]
    insuranceData=[]
    locations.append({
            "location1":location1_data,
            "location2":location2_data
            })
    locationsdata = {"locations": []}
    for key, value in locations[0].items():
            locationsdata["locations"].extend(value)

    responsed_data = {"locations": {}}
    for index, item in enumerate(locationsdata["locations"]):
        location_key = f"locations{index + 1}"
        responsed_data["locations"][location_key] = item

    insuranceData.append({
        "insurance1":insurance1_data,
        "insurance2":insurance2_data
    })
    response_data = {"insurances": []}
    for key, value in insuranceData[0].items():
        response_data["insurances"].extend(value)

    # print(locations.json())
    modifiedData.append({
        "id":booking_vehicle.id,
        "name":booking_vehicle.name,
        "pickup_date":booking_vehicle.pickup_Date,
        "dropoff_date":booking_vehicle.dropoff_Date,
        "booking_ref":booking_vehicle.booking_ref,
        "vehicle_type":booking_vehicle.vehicle_type,
        "excess_amount":booking_vehicle.excess_amount,
        "Fee":booking_vehicle.fee,
        "Rating":booking_vehicle.rating,
        "car_rental":booking_vehicle.car_rental,
        "Insurance":booking_vehicle.Insurance,
        "tax":booking_vehicle.tax,
        "paid":booking_vehicle.paid,
        "total":booking_vehicle.total,
        "Rating_count":booking_vehicle.rating_count,
        "image":booking_vehicle.image,
        "attributes":attributeData,
        "inclusion":inclusionData,
        "locations":responsed_data,
        "extras":extras,
        "driver":driverData,
        "insurances":response_data
        
    })
    if booking_vehicle is None:
        raise HTTPException(status_code=404, detail='booking_vehicle not found')
    return {"ModifiedData": modifiedData}


#show all categories
@app.get("/category/all",status_code=status.HTTP_200_OK)
async def get_All(db: Session = Depends(get_db)):
    category_data=db.query(models.categoryClass).all()
    return {'categories':category_data}

# create category
@app.post("/category",status_code=status.HTTP_201_CREATED,tags=["Category"])
async def create_category(category: categoryBase, db: db_dependency):
    db_category = models.categoryClass(**category.dict())
    db.add(db_category)
    db.commit()
    return category

# create rental_t_c
@app.post("/rental_t_c",status_code=status.HTTP_201_CREATED,tags=["Rental T & C"])
async def create_rental_t_c(r_t_c: rental_t_cBase, db: db_dependency):
    db_r_t_c = models.rental_t_cClass(**r_t_c.dict())
    db.add(db_r_t_c)
    db.commit()
    return r_t_c

#show all t_c
@app.get("/rental_t_c/all",status_code=status.HTTP_200_OK,tags=["Rental T & C"])
async def get_All(db: Session = Depends(get_db)):
    r_t_c_data=db.query(models.rental_t_cClass).all()
    return r_t_c_data


# #display t&c by id
@app.get("/r_t&cById/{r_t_c_id}",status_code=status.HTTP_200_OK,tags=["Rental T & C"])
async def read_t_c(r_t_c_id:UUID, db:db_dependency):
    rental_t_c=db.query(models.rental_t_cClass).filter(models.rental_t_cClass.id==r_t_c_id).first()   
    if rental_t_c is None:
        raise HTTPException(status_code=404, detail='Rentl t_c not found')
    return rental_t_c

#update t&c
@app.put("/rentalt_c/{r_t_c_id}",status_code=status.HTTP_200_OK,response_model=rental_t_cBase,tags=["Rental T & C"])
async def update_rental_t_c(r_t_c_id:UUID ,db:db_dependency,r_t_c:rental_t_cBase):
    try:
        db_r_t_c_update=db.query(models.rental_t_cClass).filter(models.rental_t_cClass.id==r_t_c_id).first()
        db_r_t_c_update.title=r_t_c.title
        db_r_t_c_update.description=r_t_c.description
        db.add(db_r_t_c_update)
        db.commit()
        return db_r_t_c_update
    except:
        return HTTPException(status_code=404, detail="t_c not found")

#delete t&c
@app.delete("/r_t_c/{r_t_c_id}",status_code=status.HTTP_200_OK,tags=["Rental T & C"])
async def delete_r_t_c(r_t_c_id:UUID ,db:db_dependency):
    db_r_t_c=db.query(models.rental_t_cClass).filter(models.rental_t_cClass.id==r_t_c_id).first()
    if db_r_t_c is None:
        raise HTTPException(status_code=404 , detail="r_t_c was not founded")
    db.delete(db_r_t_c)
    db.commit()
    return db_r_t_c
