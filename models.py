from datetime import datetime
from typing_extensions import Annotated
from fastapi_utils.guid_type import GUID
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime,Text,TIME,BigInteger,Float
from sqlalchemy.orm import relationship,Mapped
from database import Base
from fastapi import Body
from sqlalchemy.ext.declarative import declarative_base

# class user(Base):
#     __tablename__='user'
#     id=Column(Integer,primary_key=True)
#     name=Column(String(255))

#create acrissTable  
class acrissClass(Base):
    __tablename__='acriss'

    id= Column(GUID ,primary_key=True , index=True)
    name=Column(String(255))
    booking_vehicle= relationship('booking_vehicleClass', back_populates='acriss')
    vehicle =  relationship("vehicleClass", back_populates='acriss')

#create booking
class booking_vehicleClass(Base):
    __tablename__ = 'booking_vehicle'
    
    id =Column(GUID, primary_key=True , index=True)
    name = Column(String(255))
    booking_ref=Column(String(255))
    pickup_Date=Column(DateTime)
    dropoff_Date=Column(DateTime)
    vehicle_type= Column(String(255))
    excess_amount = Column(Float)
    fee=Column(Float)
    car_rental=Column(BigInteger)
    Insurance=Column(BigInteger)
    tax=Column(BigInteger)
    paid=Column(BigInteger)
    dueCheck_out=Column(BigInteger)
    rating_count=Column(Integer)
    rating=Column(Float)
    image = Column(String(1024))
    total= Column(Integer)
    acriss_id = Column(GUID,ForeignKey("acriss.id"))
    t_cid=Column(GUID,ForeignKey("t_c.id"))
    inclusionid=Column(GUID,ForeignKey("inclusion.id"))
    locationid=Column(GUID,ForeignKey("location.id"))
    driver_detail_id=Column(GUID,ForeignKey("driver_detail.id"))
    acriss =  relationship("acrissClass", back_populates='booking_vehicle')
    driver_detail= relationship("driverDetailClass")
    t_c=relationship("t_cClass")
    inclusions=relationship("inclusionClass")
    locations=relationship("locationClass")
    

class inclusionClass(Base):
    __tablename__= 'inclusion'

    id=Column(GUID, primary_key=True, index=True)
    name=Column(String(255))
    vehicle =  relationship("vehicleClass", back_populates='inclusion')
    booking_vehicle=relationship("booking_vehicleClass")



class categoryClass(Base):
    __tablename__= 'category'

    id= Column(GUID, primary_key=True,index=True)
    name=Column(String(255))
    vehicle =  relationship("vehicleClass", back_populates='category')

#create VehicleTable
class vehicleClass(Base):
    __tablename__ = 'vehicle'
    
    id =Column(GUID, primary_key=True , index=True)
    name = Column(String(255), unique=True)
    vehicle_type= Column(String(255))
    excess_amount = Column(Float)
    local_fee=Column(Float)
    price=Column(Float)
    rating=Column(Float)
    rating_count=Column(Integer)
    payment_method=Column(String(255))
    image = Column(String(1024))
    location_name = Column(String(255))
    acriss_id = Column(GUID,ForeignKey("acriss.id"))
    attribute_id=Column(GUID,ForeignKey("attribute.id"))
    vehicle_group_id=Column(GUID,ForeignKey("vehicle_group.id"))
    location_id=Column(GUID,ForeignKey("location.id"))
    inclusion_id=Column(GUID,ForeignKey("inclusion.id"))
    acriss =  relationship("acrissClass")
    attribute= relationship("attributeClass")
    category_id=Column(GUID,ForeignKey("category.id"))
    vehicle_group= relationship("vehicleGroupClass")
    location=relationship("locationClass", back_populates='vehicle')
    category=relationship("categoryClass", back_populates='vehicle')
    inclusion=relationship("inclusionClass")
    
#create LcationTable
class locationClass(Base):
    __tablename__='location'

    id= Column(GUID ,primary_key=True , index=True)
    location_name=Column(String(255))
    image=Column(String(255))
    days = Column(GUID,ForeignKey("days.id"))
    day_relation =  relationship("daysClass")
    vehicle =  relationship("vehicleClass", back_populates='location')
    booking_vehicle=relationship("booking_vehicleClass")

class daysClass(Base):
    __tablename__='days'

    id=Column(GUID,primary_key=True,index=True)
    weekday=Column(String(255))
    is_closed=Column(Boolean,default=True)
    day_hour_id = Column(GUID,ForeignKey("days_hours.id"))
    day_hours =  relationship("days_hoursClass")

class days_hoursClass(Base):
    __tablename__='days_hours'

    id=Column(GUID,primary_key=True,index=True)
    opening_hour=Column(TIME)
    closing_hour=Column(TIME)

#create vehicleGroup
class vehicleGroupClass(Base):
    __tablename__='vehicle_group'

    id= Column(GUID ,primary_key=True , index=True)
    name=Column(String(255))
    vehicle =  relationship("vehicleClass", back_populates='vehicle_group')

#create t_c
class t_cClass(Base):
    __tablename__='t_c'

    id=Column(GUID, primary_key=True , index=True)
    title=Column(String(255))
    description=Column(Text)
    booking_vehicle=relationship("booking_vehicleClass")

#create t_c
class rental_t_cClass(Base):
    __tablename__='rental_t_c'

    id=Column(GUID, primary_key=True , index=True)
    title=Column(String(255))
    description=Column(Text)

#create Attribute
class attributeClass(Base):
    __tablename__='attribute'

    id=Column(GUID , primary_key=True, index=True)
    attribute_name=Column(String(255))
    vehicle =  relationship("vehicleClass", back_populates='attribute')
   
#create insurance
class insuranceClass(Base):
    __tablename__='insurance'

    id=Column(GUID, primary_key=True, index=True)
    name=Column(String(255))
    amount=Column(Float, index=True)
    type=Column(String(255))
    description=Column(Text)
    driver_detail= relationship("driverDetailClass")

#create extra
class extraClass(Base):
    __tablename__='extra'

    id=Column(GUID, primary_key=True, index=True)
    name=Column(String(255))
    amount=Column(Float, index=True)
    type=Column(String(255))
    image=Column(String(1024))
    quantity=Column(Integer)
    driver_detail= relationship("driverDetailClass")


class driverDetailClass(Base):
    __tablename__ = 'driver_detail'

    id=Column(GUID,primary_key=True, index=True)
    first_name= Column(String(255))
    last_name=Column(String(255))
    title=Column(String(255))
    email=Column(String(255))
    phone_code=Column(String(255))
    phone_number=Column(BigInteger)
    driver_age=Column(Integer)
    address=Column(String(1024))
    city=Column(String(255))
    postal_code=Column(Integer)
    country=Column(String(255))
    remark=Column(String(255))
    insurance_id=Column(GUID,ForeignKey("insurance.id"))
    insurance= relationship("insuranceClass")
    extra_id=Column(GUID,ForeignKey("extra.id"))
    extra= relationship("extraClass")
    
class cancellationClass(Base):
    __tablename__='cancellation'

    id=Column(GUID, primary_key=True)
    reason=Column(String(1024))
    charges=Column(Float)

