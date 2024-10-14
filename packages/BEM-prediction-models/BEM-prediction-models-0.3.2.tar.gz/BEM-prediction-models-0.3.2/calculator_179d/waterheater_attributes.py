# Commercial:

# Standby Loss (SL): The average hourly energy, expressed in Btu per hour, required to maintain the stored water temperature 
#                    based on a 70°F temperature differential between stored water and ambient room temperature.
#                    https://www.energystar.gov/products/water_heaters/commercial_water_heaters/key_product_criteria


# modeled UA units= W/K

 # Inputs:
    # water_heater_type
     # Commerical
         # standyloss
         # Thermal efficiency

         # Outputs:  ua_w_per_k, eta_burner_final

     # Residential
         # first_hour_rating [gallons]
         # uef
         # Capacity [btu/h]

         # Outputs: ua_w_per_k, eta_burner_final

import math

def waterheater_attributes(args):

    if (('water_heating_standby_loss' in args) and (args['water_heating_standby_loss']>0)):

        Btuperh2Watts = 0.29307107

        Temperaturedifferential = 70 #degF
        TemperaturedifferentialKelvin = Temperaturedifferential*(5/9)

        ua_w_per_k = (args['water_heating_standby_loss']*Btuperh2Watts)/TemperaturedifferentialKelvin

        eta_burner_final = args['water_heating_thermal_efficiency']/100

        return ua_w_per_k, eta_burner_final

    else:
        # define constant properties
        density = 8.2938 # lb/gal
        cp = 1.0007 # Btu/lb-F
        t_in = 58.0 # F
        t_env = 67.5 # F
        t = 125.0 # F

        ef = 0.9066 * args['water_heating_uef'] + 0.0711
        if ef >= 0.75:
          recovery_efficiency = 0.561 * ef + 0.439
        else:
          recovery_efficiency = 0.252 * ef + 0.608

        if (args['water_heating_first_hour_rating'] >= 0 and args['water_heating_first_hour_rating'] < 18):
            volume_drawn = 10.0 # gal
        elif (args['water_heating_first_hour_rating'] >= 18 and args['water_heating_first_hour_rating'] < 51):
            volume_drawn = 38.0 # gal
        elif (args['water_heating_first_hour_rating'] >= 51 and args['water_heating_first_hour_rating'] < 75):
            volume_drawn = 55.0 # gal
        elif (args['water_heating_first_hour_rating'] >= 75 and args['water_heating_first_hour_rating'] <= 130):
            volume_drawn = 84.0 # gal
        else:
            raise ValueError('first_hour_rating is beyond modeling range (< 130)')


        # calc ua_w_per_k and eta_burner_final
        draw_mass = volume_drawn * density # lb
        q_load = draw_mass * cp * (t - t_in) # Btu/day
        poww = args['water_heating_capacity']
        ua_btu_per_hr_r = ((recovery_efficiency / args['water_heating_uef']) - 1.0) / ((t - t_env) * (24.0 / q_load) - ((t - t_env) / (poww * args['water_heating_uef']))) # Btu/hr-F
        eta_burner_final = recovery_efficiency + ((ua_btu_per_hr_r * (t - t_env)) / poww) # conversion efficiency is slightly larger than recovery efficiency
        ua_w_per_k = ua_btu_per_hr_r/ 3.41 * 0.555556 # Btu/hr-R to W/K, 1 Btu/hr = 1/3.41 W, 1 R = 0.555556 K

        return ua_w_per_k, eta_burner_final
