from __future__ import annotations

import datetime
import logging
from copy import deepcopy
from dataclasses import dataclass
from typing import Sequence

import numpy as np
from dateutil.parser import isoparse
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.ticker import ScalarFormatter
from nuclei.client import NucleiClient
from nuclei.client.utils import serialize_jsonifyable_object

from baec.measurements import plot_utils
from baec.measurements.measured_settlement_series import MeasuredSettlementSeries

BASE_URL = "https://crux-nuclei.com/api/settlecore/v1/"


@dataclass
class FitCoreModel:
    """Object containing the results of a fit call."""

    primarySettlement: float
    """Primary settlement [%]"""
    shift: float
    """Shift [days]"""
    hydrodynamicPeriod: float
    """Hydrodynamic period [year]"""
    finalSettlement: float
    """Final settlement [m]"""


@dataclass
class FitCoreResult:
    """Object containing the results of a predict call."""

    settlement: Sequence
    """Settlement [m]"""


class FitCoreModelGenerator:

    def __init__(
        self,
        series: MeasuredSettlementSeries,
        client: NucleiClient,
    ):
        """


        Parameters
        ----------
        series : MeasuredSettlementSeries
            Represents a series of measurements for a single settlement rod.
        client : NucleiClient
        """

        self._series = series
        self._client = client
        self._hash_settlements_ = deepcopy(tuple(self.series.settlements).__hash__())
        self._model = self.fit(force=True)

    @property
    def series(self) -> MeasuredSettlementSeries:
        """Represents a series of measurements for a single settlement rod."""
        return self._series

    def fit(self, force: bool = True) -> FitCoreModel:
        """
        Fit the settlement measurements for a single settlement rod on
        a simplification of the Koppejan formula based on Arcadis
        Handleiding ZBASE en ZBASE analyse, versie 7.0; d.d. 31-10-2011

        Returns
        -------
        model : FitCoreModel
        """

        # check if the __hash__ of the MeasuredSettlementSeries has changed
        # if not no need to refit the series
        if (
            not force
            and self._hash_settlements_ == tuple(self.series.settlements).__hash__()
        ):
            logging.info("Series has not changed. Use cached FitCoreModel")
            return self._model

        # create payload for the fit API call
        payload = {
            "timeSeries": [
                isoparse(x.isoformat()) for x in self.series.to_dataframe()["date_time"]
            ],
            "settlementSeries": np.clip(self.series.settlements, 0, None).tolist(),
            "startDay": 0,
        }

        # call endpoint
        response = self._client.session.post(
            url=BASE_URL + "simpleKoppejan/fit",
            json=serialize_jsonifyable_object(payload),
        )

        if not response.ok:
            raise RuntimeError(response.text)

        # update cache properties
        self._hash_settlements_ = deepcopy(tuple(self.series.settlements).__hash__())
        self._model = FitCoreModel(**response.json()["popt"])

        return self._model

    def predict(self, days: Sequence[int]) -> FitCoreResult:
        """
        Predict the settlement for any day with on a simplification of
        the Koppejan formula based on Arcadis Handleiding ZBASE en
        ZBASE analyse, versie 7.0; d.d. 31-10-2011


        Parameters
        ----------
        days : Sequence[int]
            TimeDelta of the start settlement based from start of measurements [days]

        Returns
        -------
        result : FitCoreResult
        """

        payload = {"days": days} | self.fit(force=False).__dict__

        response = self._client.session.post(
            url=BASE_URL + "simpleKoppejan/predict",
            json=serialize_jsonifyable_object(payload),
        )

        if not response.ok:
            raise RuntimeError(response.text)

        return FitCoreResult(**response.json())

    def plot_settlement_time(
        self,
        axes: Axes | None = None,
        log_time: bool = True,
        min_log_time: float = 1.0,
        add_date_time: bool = True,
        datetime_format: str = "%d-%m-%Y",
        end_date_time: datetime.datetime | int = 500,
        invert_yaxis: bool = True,
        add_model_parameters: bool = True,
    ) -> Axes:
        """
        Plot the settlement of the initial ground profile rod over time.

        Parameters
        ----------
        axes: plt.Axes | None, optional
            Axes to create the figure. If None creates new Axes.
            Default is None.
        log_time: bool, optional
            If True, the time axis is logarithmic (linear otherwise).
            Note that time is plotted in days.
            Default is True.
        min_log_time: float, optional
            The minimum value for the time axis in [days] in case of a logarithmic plot.
            It must be greater than 0.0.
            Default is 1.0.
        add_date_time: bool, optional
            If True, the date and time are added as a secondary x-axis.
            Default is True.
        datetime_format: str, optional
            The format of the date and time on the x-axis (only used if `add_date_time` is True).
            It must be an acceptable format for the strftime method of the datetime.datetime class.
            Default is "%d-%m-%Y".
        end_date_time: datetime.datetime | int, optional
            End date time of the predicted settlement, Can be datetime object or integer. If integer number
            corresponds to the number of days from `start_date_time` of the MeasuredSettlementSeries.
            Default is 100
        invert_yaxis: bool, optional
            Whether the yaxis is oriented in the "inverse" direction.
            Default is True
        add_model_parameters: bool, optional
            Whether the model parameters are added to the plot
            Default is True

        Returns
        -------
        plt.Axes

        Raises
        ------
        TypeError
            If the types of the input parameters are incorrect.
        ValueError
            If the `datetime_format` is not a valid format for the strftime method of the
            datetime.datetime class.
            If the `min_log_time` is not greater than 0.0.
        """

        # Validate input plot parameters
        plot_utils.validate_plot_parameter_axes(axes)
        plot_utils.validate_plot_parameter_log_time(log_time)
        plot_utils.validate_plot_parameter_min_log_time(min_log_time)
        plot_utils.validate_plot_parameter_add_date_time(add_date_time)
        plot_utils.validate_plot_parameter_datetime_format(datetime_format)

        # calculate the end date for the prediction
        if isinstance(end_date_time, datetime.datetime):
            if end_date_time < self.series.start_date_time:
                raise ValueError("End datetime cannot be before start datetime.")
            end_time_delta = end_date_time - self.series.start_date_time
        elif isinstance(end_date_time, int):
            end_time_delta = datetime.timedelta(days=end_date_time)
        else:
            raise ValueError(
                f"Attribute `end_time_delta` must be a datetime object or an int got a {type(end_date_time)}"
            )

        # If axes is None create new Axes.
        if axes is None:
            plt.figure()
            axes = plt.gca()

        # Plot the property data over time
        days = np.arange(0, end_time_delta.days, step=1, dtype=float)
        settlement = self.predict(days).settlement
        axes.plot(days, settlement)

        if log_time:
            axes.set_xlim(min_log_time, max(days) + 1.0)
            axes.set_xscale("log")

        axes.set_ylim(min(settlement) - 0.5, max(settlement) + 0.5)
        if invert_yaxis:
            axes.invert_yaxis()

        axes.xaxis.set_major_formatter(ScalarFormatter())
        axes.xaxis.set_minor_formatter(ScalarFormatter())
        axes.grid(visible=True, which="both")

        axes.set_ylabel(
            f"Settlement [{self.series.coordinate_reference_systems.vertical_units}]"
        )
        axes.set_xlabel("Time [days]")
        axes.set_title(
            f"Predicted settlement of initial ground surface for object: {self.series.object_id}"
        )

        # Add secondary xaxis with the date_time
        if add_date_time:
            axes = self.series._add_datetime_as_secondary_axis(
                axes=axes, datetime_format=datetime_format
            )

        # Add text to the Axes.
        if add_model_parameters:
            model = self.fit(force=False)
            label = """FitCore model parameters:
                \n final settlement = {:.2f}
                \n hydrodynamic period = {:.2f}
                \n shift = {:.2f}
                \n primary settlement = {:.2f}""".format(
                model.finalSettlement,
                model.hydrodynamicPeriod,
                model.shift,
                model.primarySettlement,
            )
            axes.text(
                np.mean(days),
                0,
                label,
                style="italic",
                bbox={"facecolor": "lightgray", "alpha": 0.5, "pad": 10},
                horizontalalignment="center",
                verticalalignment="center",
            )

        return axes

    def plot_fill_settlement_time(
        self,
        log_time: bool = True,
        min_log_time: float = 1.0,
        add_date_time: bool = True,
        datetime_format: str = "%d-%m-%Y",
        end_date_time: datetime.datetime | int = 500,
    ) -> Figure:
        """
        Plot in a new fill thickness and the settlement of the initial ground profile
        relative to the zero measurement over time.

        Parameters
        ----------
        log_time: bool, optional
            If True, the time axis is logarithmic (linear otherwise).
            Note that time is plotted in days.
            Default is True.
        min_log_time: float, optional
            The minimum value for the time axis in [days] in case of a logarithmic plot.
            It must be greater than 0.0.
            Default is 1.0.
        add_date_time: bool, optional
            If True, the date and time are added as a secondary x-axis.
            Default is True.
        datetime_format: str, optional
            The format of the date and time on the x-axis (only used if `add_date_time` is True).
            It must be an acceptable format for the strftime method of the datetime.datetime class.
            Default is "%d-%m-%Y".
        end_date_time: datetime.datetime | int, optional
            End date time of the predicted settlement, Can be datetime object or integer. If integer number
            corresponds to the number of days from `start_date_time` of the MeasuredSettlementSeries.
            Default is 100

        Returns
        -------
        plt.Axes

        Raises
        ------
        TypeError
            If the types of the input parameters are incorrect.
        ValueError
            If the `datetime_format` is not a valid format for the strftime method of the
            datetime.datetime class.
            If the `min_log_time` is not greater than 0.0.
        """
        fig, axes = plt.subplots(2, 1, figsize=(10, 20), sharex=True)

        self.series.plot_fill_time(
            axes=axes[0],
            log_time=log_time,
            min_log_time=min_log_time,
            add_date_time=add_date_time,
            datetime_format=datetime_format,
        )
        axes[0].set_title("")
        axes[0].set_xlabel("")

        # add settlement prediction secondary axes
        self.plot_settlement_time(
            axes=axes[1],
            log_time=False,
            min_log_time=min_log_time,
            add_date_time=False,
            datetime_format=datetime_format,
            end_date_time=end_date_time,
            invert_yaxis=False,
            add_model_parameters=True,
        )

        self.series.plot_settlement_time(
            axes=axes[1],
            log_time=log_time,
            min_log_time=min_log_time,
            add_date_time=False,
            datetime_format=datetime_format,
        )
        axes[1].set_title("")

        if add_date_time:
            fig.subplots_adjust(top=0.825, hspace=0.075)

        fig.suptitle(
            f"Fill thickness and settlement for object: {self.series.object_id}"
        )

        return fig
