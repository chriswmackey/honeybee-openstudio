# coding=utf-8
"""Module taken from OpenStudio-standards.

https://github.com/NREL/openstudio-standards/blob/master/
lib/openstudio-standards/thermal_zone/thermal_zone.rb
"""
from __future__ import division


def thermal_zone_get_outdoor_airflow_rate(thermal_zone):
    """Calculates the zone outdoor airflow requirement (Voz).

    The result will be based on the inputs in the DesignSpecification:OutdoorAir
    objects in all spaces in the zone.

    Args:
        thermal_zone: [OpenStudio::Model::ThermalZone] OpenStudio ThermalZone object.

    Returns:
        [Double] the zone outdoor air flow rate in cubic meters per second (m^3/s).
    """
    tot_oa_flow_rate = 0.0
    spaces = thermal_zone.spaces()
    sum_floor_area = 0.0
    sum_number_of_people = 0.0
    sum_volume = 0.0

    # Variables for merging outdoor air
    sum_oa_for_people = 0.0
    sum_oa_for_floor_area = 0.0
    sum_oa_rate = 0.0
    sum_oa_for_volume = 0.0

    # Find common variables for the new space
    for space in spaces:
        floor_area = space.floorArea()
        sum_floor_area += floor_area

        number_of_people = space.numberOfPeople()
        sum_number_of_people += number_of_people

        volume = space.volume()
        sum_volume += volume

        dsn_oa = space.designSpecificationOutdoorAir()
        if not dsn_oa.is_initialized():
            continue

        dsn_oa = dsn_oa.get()

        # compute outdoor air rates in case we need them
        oa_for_people = number_of_people * dsn_oa.outdoorAirFlowperPerson()
        oa_for_floor_area = floor_area * dsn_oa.outdoorAirFlowperFloorArea()
        oa_rate = dsn_oa.outdoorAirFlowRate()
        oa_for_volume = volume * dsn_oa.outdoorAirFlowAirChangesperHour() / 3600

        # First check if this space uses the Maximum method and other spaces do not
        if dsn_oa.outdoorAirMethod() == 'Maximum':
            sum_oa_rate += max([oa_for_people, oa_for_floor_area, oa_rate, oa_for_volume])
        elif dsn_oa.outdoorAirMethod() == 'Sum':
            sum_oa_for_people += oa_for_people
            sum_oa_for_floor_area += oa_for_floor_area
            sum_oa_rate += oa_rate
            sum_oa_for_volume += oa_for_volume

    tot_oa_flow_rate += sum_oa_for_people
    tot_oa_flow_rate += sum_oa_for_floor_area
    tot_oa_flow_rate += sum_oa_rate
    tot_oa_flow_rate += sum_oa_for_volume

    return tot_oa_flow_rate
