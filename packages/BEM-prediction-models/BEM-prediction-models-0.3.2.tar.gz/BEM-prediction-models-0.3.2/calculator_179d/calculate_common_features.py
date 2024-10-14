import calculator_179d.SurrogateModelMetricConversion as smc
import calculator_179d.waterheater_attributes as wha
import numpy as np

def calculate_ext_wall_surface_area(calculator_user_inputs):

    if calculator_user_inputs["building_type"] == "small office":
        floor_to_floor_height= 10*0.3048 # floor height in m
    elif "retail" in calculator_user_inputs["building_type"]:
        floor_to_floor_height = 17*0.3048 # floor height for retail stripmall
    #floor area in m^2
    AF = (
        calculator_user_inputs['gross_floor_area']/
        calculator_user_inputs['number_of_floors']
    )
    #gross ext wall surface area in m^2
    ext_wall_surface_area_gross= (
        2*floor_to_floor_height*(
            np.sqrt(
                calculator_user_inputs['aspect_ratio']*AF
            )+
            np.sqrt(
                AF/calculator_user_inputs['aspect_ratio']
            )
        )
    )*calculator_user_inputs['number_of_floors']
    #opaque ext wall surface area in m^2
    ext_wall_surface_area = (
        (1-calculator_user_inputs['window_wall_ratio'])*
        ext_wall_surface_area_gross
    )

    return ext_wall_surface_area

def calculate_window_area(calculator_user_inputs):

    #opaque ext wall surface area
    ext_wall_surface_area = calculate_ext_wall_surface_area(calculator_user_inputs)
    #gross ext wall surface area 
    ext_wall_surface_area_gross = (
        ext_wall_surface_area/
        (1-calculator_user_inputs['window_wall_ratio'])
    )
    window_area = (
        calculator_user_inputs['window_wall_ratio']*
        ext_wall_surface_area_gross
    )

    return window_area


def calculate_roof_area(calculator_user_inputs):

    gross_floor_area = calculator_user_inputs['gross_floor_area']
    n_stories = calculator_user_inputs['number_of_floors']
    roof_area = (gross_floor_area/n_stories)

    return roof_area


def calculate_ACH_infiltration(calculator_user_inputs):

    #bldg_type = calculator_user_inputs['building_type']
    #if bldg_type == 'small office':
    AF = (
        calculator_user_inputs['gross_floor_area']/
        calculator_user_inputs['number_of_floors']
    )

    I = 0.0115824 
    ACH_infiltration = (
        (I*120*(
            np.sqrt(calculator_user_inputs['aspect_ratio']*AF)+
            np.sqrt(AF/calculator_user_inputs['aspect_ratio'])
            )
        )/(
            AF*calculator_user_inputs['number_of_floors']
        )
    )*calculator_user_inputs['number_of_floors']

    return ACH_infiltration


def calculate_ua_bldg(calculator_user_inputs):

    # calculate external wall surface area
    ext_wall_surface_area = calculate_ext_wall_surface_area(calculator_user_inputs)
    #calculate roof area
    roof_area = calculate_roof_area(calculator_user_inputs)
    # calculate window area
    window_area = calculate_window_area(calculator_user_inputs)

    #calculate ua_bldg
    ua_bldg = (
        roof_area*calculator_user_inputs['roof_thermal_perf_type'] +
        ext_wall_surface_area*calculator_user_inputs['wall_thermal_perf_type'] +
        window_area*calculator_user_inputs['window_u_factor']
    )

    return ua_bldg


def calculate_sa_to_vol_ratio(calculator_user_inputs):

    # calculate roof area
    roof_area = calculate_roof_area(calculator_user_inputs)
    #calculate surface to volume ratio
    sa_to_vol_ratio = (
        2. * ((
            calculator_user_inputs['aspect_ratio']/roof_area
            ) ** 0.5 + 
            (1./(calculator_user_inputs['aspect_ratio']*roof_area)
            ) **0.5) +
        (1./(10.*calculator_user_inputs["number_of_floors"]))
    )

    return sa_to_vol_ratio


def calculate_cooling_and_heating_cop(calculator_user_inputs):
    ##COP values from ahri
    ahri_args = {}
    #get cooling and heating cop
    cooling_ahri_metric = False
    heating_ahri_metric = False
    for feature,value in calculator_user_inputs.items():
        if feature in ['SEER','EER','SEER2','EER2']:
            ahri_args[feature] = value
            cooling_ahri_metric = True
        if feature in [
            'HSPF','HSPF2','HeatingCOP','boiler_average_efficiency','gas_coil_average_efficiency'
            ]:
            ahri_args[feature] = value
            heating_ahri_metric = True

        if cooling_ahri_metric and heating_ahri_metric:
            break
    ahri_args['hvac_system'] = calculator_user_inputs['hvac_system']
    [cooling_cop,heating_cop] = smc.AHRI2COP(ahri_args)

    return [cooling_cop,heating_cop]

def calculate_wh_ua_and_efficiency(calculator_user_inputs):
    # COP values from ahri
    ahri_args = {}
    # get cooling and heating cop
    for feature,value in calculator_user_inputs.items():
        if feature in [
            'water_heating_standby_loss',
            'water_heating_thermal_efficiency',
            'water_heating_first_hour_rating',
            'water_heating_uef',
            'water_heating_capacity'
        ]:
            ahri_args[feature] = value


    [ua_w_per_K,eta_burner_final] = wha.waterheater_attributes(ahri_args)

    return [ua_w_per_K,eta_burner_final]
