"""
This module is used to check the general variables
Sometimes all variables are set to 0 and this makes it appear that the vehicle was off,
however, the problem is that the vehicle is not transmitting information

This module takes all the record of a vehicle where all its variables are at 0 and every 6
continuos records are counted as a failure

Vehicle disconnection
"""
import pandas as pd
from availability_checker.checker.common.common import CommonCalcsForAvailability
from availability_checker.checker.common.utils import validate_if_required_columns_are_in_data


class VehicleDisconnectionAvailabilityChecker:
    """
    Entry point for the availability checker
    """

    def __init__(self, data: pd.DataFrame):
        """
        Constructor for the availability checker

        Parameters:
            data (pd.DataFrame): The data to check (Complete data)
        """
        self.data = data

    def _has_required_columns(self) -> bool:
        """
        Method to check if the required columns are in the data
        """
        required_columns = [
            "idVehiculo",
            "fechaHoraLecturaDato",
            "velocidadVehiculo",
            "temperaturaMotor",
            "presionAceiteMotor",
            "revolucionesMotor",
            "estadoDesgasteFrenos",
            "kilometrosOdometro",
            "consumoCombustible",
            "nivelTanqueCombustible",
        ]
        return validate_if_required_columns_are_in_data(self.data, required_columns)

    def _mark_invalid_records(self) -> pd.DataFrame:
        """
        Method to mark the invalid records in the data

        ***
        A record is invalid if the all the variables are 0, but only if there are at least 6
        continuous records with all the variables at 0 in the same vehicle and date is
        considered a failure
        ***

        Returns:
            pd.DataFrame: The DataFrame with the availability check results

        Raises:
            ValueError: If the required columns are not found in the data
        """
        # Validate if the required columns are in the data
        if not self._has_required_columns():
            raise ValueError("Required columns not found in the data to get the availability for vehicleDisconnection")

        self.data["vehicleDisconnectionFailures"] = 0
        unique_vehicles = self.data["idVehiculo"].unique()

        for vehicle in unique_vehicles:
            vehicle_data = self.data[self.data["idVehiculo"] == vehicle].sort_values(by="fechaHoraLecturaDato")

            vehicle_data["all_zero"] = (
                (vehicle_data["velocidadVehiculo"] == 0)
                & (vehicle_data["temperaturaMotor"] == 0)
                & (vehicle_data["presionAceiteMotor"] == 0)
                & (vehicle_data["revolucionesMotor"] == 0)
                & (vehicle_data["estadoDesgasteFrenos"] == 0)
                & (vehicle_data["kilometrosOdometro"] == 0)
                & (vehicle_data["consumoCombustible"] == 0)
                & (vehicle_data["nivelTanqueCombustible"] == 0)
            )

            # Contar si hay 6 registros consecutivos donde 'all_zero' sea True
            vehicle_data["consecutive_zeros"] = (
                vehicle_data["all_zero"]
                .rolling(window=6, min_periods=6)
                .apply(lambda x: all(x), raw=True)
                .shift(-5)
                .fillna(0)
                .astype(bool)
            )

            vehicle_data["vehicleDisconnectionFailures"] = vehicle_data["consecutive_zeros"].astype(int)
            self.data.loc[vehicle_data.index, "vehicleDisconnectionFailures"] = vehicle_data["consecutive_zeros"].astype(int)

        return self.data

    def get_availability(self) -> dict:
        """
        Method to get the availability for the general variables

        Returns:
            dict: The availability data and the data for the global availability

        """
        self.data = self._mark_invalid_records()
        common_calcs = CommonCalcsForAvailability(self.data, "vehicleDisconnectionFailures")
        availability_data: pd.DataFrame = common_calcs.calculate_availability()
        availability_data["variable"] = "vehicleDisconnection"

        response = {
            "availability_data": availability_data,
            "data_for_global": self.data[["idVehiculo", "fechaHoraLecturaDato", "vehicleDisconnectionFailures"]],
        }

        return response
