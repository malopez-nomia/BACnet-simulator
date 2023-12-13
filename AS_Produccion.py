# Author: Tomáš Kretek
# Created for test purposes on VUT Brno, Czech Republic

# tested BAC0 version: 21.12.03

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from time import sleep
from sys import exit

from BAC0.core.devices.local.object import ObjectFactory
from bacpypes.basetypes import DeviceObjectPropertyReference, DailySchedule, TimeValue
from bacpypes.constructeddata import ArrayOf
from bacpypes.object import ScheduleObject,MultiStateValueObject,MultiStateOutputObject
from bacpypes.primitivedata import Real
from BAC0 import lite
from BAC0.core.devices.local.models import (
    analog_input,
    analog_output,
    binary_output,
    binary_input,
    analog_value
)




# Parse command line arguments
parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument("-a", "--address", default=None, help="IPV4 address of device interface with network mask, "
                                                          "e.g. 10.0.0.34/24")
parser.add_argument("-p", "--port", default=47809, type=int, help="Port of BACnet device that will be created")
parser.add_argument("-di", "--deviceId", default=101, type=int, help="ID of BACnet device that will be created")
parser.add_argument("-st", "--sleepTime", default=0.4, type=float, help="Main loop sleep time (simulation speed)")
parser.add_argument("-log", "--logging", default=False, type=bool, help="Enable logging to console")
args = vars(parser.parse_args())

# Check ip address
if args["address"] is None:
    print("No IP address provided.")
    parser.print_help()
    exit(0)

# Define device
device = lite(ip=args["address"], port=args["port"], deviceId=args["deviceId"])


# Define device objects
# _new_objects = binary_output(
#     instance=58,
#     name="Lamp1",
#     description="Luces Exterior 1",
#     presentValue=True,
# )
# binary_output(
#     instance=59,
#     name="Lamp2",
#     description="Luces Exterior 2",
#     presentValue=True,
# )
# binary_output(
#     instance=57,
#     name="Lamp3",
#     description="Luces Exterior 3",
#     presentValue=True,
# )
# binary_output(
#     instance=73,
#     name="Lamp4",
#     description="Luces Exterior 4",
#     presentValue=True,
# )



#Datos Ala Central
#VAV
_new_objects = analog_value(
    instance=102,
    name="Consigna VA1V ",
    description="VAV SP Temperature",
    properties={"units": "degreesCelsius"},
    presentValue=23.0,
)
analog_value(
    instance=101,
    name="Consigna VAV",
    properties={"units": "degreesCelsius"},
    description="VAV SP Temperature",
    presentValue=19.0,
)

ObjectFactory(
    ScheduleObject,
    instance =20,
    objectName = "VAVSchedule",
    properties={
        "presentValue":1,
        "priorityForWriting": 15,
        "weeklySchedule": ArrayOf(DailySchedule)(
            [
                DailySchedule(
                    daySchedule=[
                        TimeValue(time=(8, 0, 0, 0), value=Real(1)),
                        TimeValue(time=(14, 0, 0, 0), value=Real(2)),
                        TimeValue(time=(17, 0, 0, 0), value=Real(2)),
                    ]
                ),
            ] * 7),
    },
    description="VAV schedule for room all",

)

#Termostatos

#Consigna Global
analog_value(
    instance=94,
    name="Consigna Termostatos",
    description="Termostatos SP Temperature",
    properties={"units": "degreesCelsius"},
    presentValue=21.0,
)
ObjectFactory(
    ScheduleObject,
    instance =18,
    objectName = "TermostatosSchedule",
    properties={
        'listOfObjectPropertyReferences': [
             DeviceObjectPropertyReference(
                 objectIdentifier=("CmdFancoil4", 47),
                 propertyIdentifier="presentValue",
             )
         ],
        "presentValue":1,
        "priorityForWriting": 15,
        "weeklySchedule": ArrayOf(DailySchedule)(
            [
                DailySchedule(
                    daySchedule=[
                        TimeValue(time=(8, 0, 0, 0), value=Real(1)),
                        TimeValue(time=(14, 0, 0, 0), value=Real(2)),
                        TimeValue(time=(17, 0, 0, 0), value=Real(2)),
                    ]
                ),
            ] * 7),
    },
    description="VAV schedule for room all",

)
ObjectFactory(
MultiStateValueObject,
    instance =112,
    objectName="Estado VAV",
    description="Estado VAV",
    presentValue=1,
    properties={
        "valueSourceArray": [
        ("Auto", 1),
        ("Low", 2),
        ("Medium", 3),
        ("High", 4),
    ]
    }
)


#Termostato 4
analog_output(
    instance=47,
    name="CmdFancoil4",
    description="CMD Fancoil 4",
    presentValue=1.0,
)
analog_output(
    instance=48,
    name="SPTemperatura4",
    properties={"units": "degreesCelsius"},
    description="Consigna Temperatura 4",
    presentValue=19.0,
)
analog_output(
    instance=46,
    name="SpdVentilador4",
    description="Velocidad Ventilador 4",
    presentValue=0.0,
)
analog_input(
    instance=136,
    name="TRAmbiente4",
    properties={"units": "degreesCelsius"},
    description="Temperatura Ambiente 4",
    presentValue=24.0,
)
#Termostato 5
analog_output(
    instance=50,
    name="CmdFancoil5",
    description="CMD Fancoil 5",
    presentValue=1.0,
)
analog_output(
    instance=51,
    name="SPTemperatura5",
    properties={"units": "degreesCelsius"},
    description="Consigna Temperatura 5",
    presentValue=19.0,
)
analog_output(
    instance=49,
    name="SpdVentilador5",
    description="Velocidad Ventilador 5",
    presentValue=0.0,
)
analog_input(
    instance=137,
    name="TRAmbiente5",
    properties={"units": "degreesCelsius"},
    description="Temperatura Ambiente 5",
    presentValue=24.0,
)

#Termostato 12
analog_output(
    instance=71,
    name="CmdFancoil12",
    description="CMD Fancoil 12",
    presentValue=1.0,
)
analog_output(
    instance=72,
    name="SPTemperatura12",
    properties={"units": "degreesCelsius"},
    description="Consigna Temperatura 12",
    presentValue=19.0,
)
analog_output(
    instance=70,
    name="SpdVentilador12",
    description="Velocidad Ventilador 12",
    presentValue=0.0,
)
analog_input(
    instance=144,
    name="TRAmbiente12",
    properties={"units": "degreesCelsius"},
    description="Temperatura Ambiente 12",
    presentValue=24.0,
)
#Termostato 6

analog_output(
    instance=53,
    name="CmdFancoil6",
    description="CMD Fancoil 6",
    presentValue=1.0,
)
analog_output(
    instance=54,
    name="SPTemperatura6",
    properties={"units": "degreesCelsius"},
    description="Consigna Temperatura 6",
    presentValue=19.0,
)
analog_output(
    instance=52,
    name="SpdVentilador6",
    description="Velocidad Ventilador 6",
    presentValue=0.0,
)
analog_input(
    instance=138,
    name="TRAmbiente6",
    properties={"units": "degreesCelsius"},
    description="Temperatura Ambiente 6",
    presentValue=24.0,
)

# Assign objects to device
_new_objects.add_objects_to_application(device)

# Constants
# Rozměry: 2.5x4x4, VxŠxH
# 1) https://www.prirodnistavba.cz/popup/soucinitel-tepelne-vodivosti-33e.html
# 2) https://stavba.tzb-info.cz/tabulky-a-vypocty/58-hodnoty-fyzikalnich-velicin-vybranych-stavebnich-materialu
# 3) https://cs.wikipedia.org/wiki/M%C4%9Brn%C3%A1_tepeln%C3%A1_kapacita
# 4) https://e-konstrukter.cz/prakticka-informace/vlastnosti-vzduchu

# outside_temperature = 5
# inner_wall_depth = 0.16
# outer_wall_depth = 0.35
# wall_surface = 10  # 2.5x4m
# inner_wall_sigma = 0.6  # objemová hmotnost 1700kg/m3, měrná tepelná kapacita 840 J/kg*K, řádek 60 - 2 web
# outer_wall_sigma = 0.8  # objemová hmotnost 1000kg/m3
# inner_wall_heat_transfer_const = inner_wall_sigma * wall_surface / inner_wall_depth
# outer_wall_heat_transfer_const = outer_wall_sigma * wall_surface / outer_wall_depth

# # air_sigma = 0.0262
# # objemová hmotnost 1.205 kg/m3 při 20 stupních, měrná tepelná kapacita 1005 J/kg*K při 20 stupních, 4 web
# room_capacity = 1005 * 1.205 * wall_surface * 4  # 2.5x4x4m

# eps = 0.5  # Degrees Celsius
# radiator_power = 1000  # Watts
# r1_radiator_state = True if device["RoomOneRadiatorState"].presentValue == "active" else False
# r2_radiator_state = True if device["RoomTwoRadiatorState"].presentValue == "active" else False

# # Main loop
print("Simulation started")
while True:
    sleep(args["sleepTime"])
    # r1_temperature = device["RoomOneTemperature"].presentValue
    # r2_temperature = device["RoomTwoTemperature"].presentValue
    # r1_set_point = device["RoomOneSetPoint"].presentValue
    # r2_set_point = device["RoomTwoSetPoint"].presentValue
    # r1_heating = True if device["RoomOneHeatingEnabled"].presentValue == "active" else False
    # r2_heating = True if device["RoomTwoHeatingEnabled"].presentValue == "active" else False

    # r1_temp_diff = r1_set_point - r1_temperature
    # r2_temp_diff = r2_set_point - r2_temperature

    # # Radiator relay regulators
    # if r1_heating:
    #     if r1_radiator_state and r1_temp_diff < -eps:
    #         r1_radiator_state = False
    #     elif r1_temp_diff > eps:
    #         r1_radiator_state = True
    # else:
    #     r1_radiator_state = False

    # if r2_heating:
    #     if r2_radiator_state and r2_temp_diff < -eps:
    #         r2_radiator_state = False
    #     elif r2_temp_diff > eps:
    #         r2_radiator_state = True
    # else:
    #     r2_radiator_state = False

    # # temp differs calculation
    # inner_wall_heat_flow = inner_wall_heat_transfer_const * (r1_temperature - r2_temperature)
    # room_wall_temp_diff = 1 / room_capacity * inner_wall_heat_flow

    # r1_outer_wall_heat_flow = outer_wall_heat_transfer_const * (r1_temperature - outside_temperature)
    # r1_outer_wall_temp_diff = 1 / room_capacity * r1_outer_wall_heat_flow

    # r2_outer_wall_heat_flow = outer_wall_heat_transfer_const * (r2_temperature - outside_temperature)
    # r2_outer_wall_temp_diff = 1 / room_capacity * r1_outer_wall_heat_flow

    # r1_radiator_heat_flow = radiator_power * r1_radiator_state
    # r1_radiator_temp_diff = 1 / room_capacity * r1_radiator_heat_flow

    # r2_radiator_heat_flow = radiator_power * r2_radiator_state
    # r2_radiator_temp_diff = 1 / room_capacity * r2_radiator_heat_flow

    # new_r1_temp = r1_temperature - room_wall_temp_diff - r1_outer_wall_temp_diff + r1_radiator_temp_diff
    # new_r2_temp = r2_temperature + room_wall_temp_diff - r2_outer_wall_temp_diff + r2_radiator_temp_diff

    # # logging into console
    # if args["logging"]:
    #     print("Room 1 temperature: ", r1_temperature)
    #     print("Room 1 set point: ", r1_set_point)
    #     print("Room 1 radiator state: ", r1_radiator_state)
    #     print("Room 2 temperature: ", r2_temperature)
    #     print("Room 2 set point: ", r2_set_point)
    #     print("Room 2 radiator state: ", r2_radiator_state)

    # # Assigning new values
    # device["RoomOneRadiatorState"].presentValue = r1_radiator_state
    # device["RoomTwoRadiatorState"].presentValue = r2_radiator_state
    # device["RoomOneTemperature"].presentValue = new_r1_temp
    # device["RoomTwoTemperature"].presentValue = new_r2_temp

    # # Wait for next iteration
    # sleep(args["sleepTime"])


# useful commands

# bacnet = BAC0.lite(ip="192.168.1.101/24", port=47810)
# mycontroller = BAC0.device("192.168.1.101/24:47809", 101, bacnet)
# mycontroller["WT"] = 50
# mycontroller["WT"].out_of_service()
# mycontroller["WT"] = "auto" releasuje override priority 8 zapsané pomocí kontroler příkazu výše na defaultní hodnotu
#   mycontroller["WT"].default(number)
# mycontroller["WT"].write(34, priority=13)
# mycontroller["WT"].write("null", priority=13)

# bacnet.write('192.168.1.101/24:47809 analogOutput 0 presentValue 50 - 14')
# priorities = bacnet.read('192.168.1.101/24:47809 analogOutput 0 priorityArray')

# prop = ('analogOutput', 0, 'priorityArray')
# device.points
# device["WT"].write_property(, value=25, priority=14)
# print(device.read(prop))
