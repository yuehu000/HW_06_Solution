import numpy as np
from deampy.discrete_event_sim import SimulationCalendar

from ModelEntities import UrgentCare, Patient
from ModelEvents import CloseUrgentCare, Arrival


class UrgentCareModel:
    def __init__(self, id, parameters):
        """
        :param id: ID of this urgent care model
        :param parameters: parameters of this model
        """

        self.id = id
        self.params = parameters    # model parameters
        self.simCal = None          # simulation calendar
        self.urgentCare = None      # urgent care

    def simulate(self, sim_duration):
        """ simulate the urgent care
        :param sim_duration: duration of simulation (hours)
         """

        # random number generator
        rng = np.random.RandomState(seed=self.id)

        # initialize the simulation
        self.__initialize(rng=rng)

        # while there is an event scheduled in the simulation calendar
        # and the simulation time is less than the simulation duration
        while self.simCal.n_events() > 0 and self.simCal.time <= sim_duration:
            self.simCal.get_next_event().process(rng=rng)

    def __initialize(self, rng):
        """ initialize the simulation model
        :param rng: random number generator
        """

        # simulation calendar
        self.simCal = SimulationCalendar()

        # urgent care
        self.urgentCare = UrgentCare(id=id,
                                     parameters=self.params,
                                     sim_cal=self.simCal)

        # schedule the closing event
        self.simCal.add_event(
            event=CloseUrgentCare(time=self.params.hoursOpen,
                                  urgent_care=self.urgentCare)
        )

        # find the arrival time of the first patient
        arrival_time = self.params.arrivalTimeDist.sample(rng=rng)

        # find the depression status of the next patient
        if_with_depression = False
        if rng.random_sample() < self.params.probDepression:
            if_with_depression = True

        # schedule the arrival of the first patient
        self.simCal.add_event(
            event=Arrival(time=arrival_time,
                          patient=Patient(id=0, if_with_depression=if_with_depression),
                          urgent_care=self.urgentCare)
        )

