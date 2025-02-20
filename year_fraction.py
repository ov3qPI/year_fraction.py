from skyfield.api import load
from skyfield.almanac import find_discrete, seasons
from skyfield.toposlib import Topos

def main():
    # Load high-precision ephemeris data
    eph = load('de440s.bsp')  # More accurate than de421.bsp
    ts = load.timescale()

    # Define observer location
    observer_lat = 38.478752
    observer_lon = -107.877739
    observer = Topos(latitude_degrees=observer_lat, longitude_degrees=observer_lon)

    # Compute longitudinal time offset based on observer's longitude
    longitudinal_offset_hours = observer_lon / 15.0  # Convert longitude to hour offset

    # Determine the most recent and next December solstices
    now = ts.now()
    t_start = ts.tt_jd(now.tt - 365)  # Go back ~1 year
    t_end = ts.tt_jd(now.tt + 365)    # Look ~1 year ahead

    times, events = find_discrete(t_start, t_end, seasons(eph))

    # Identify December solstices (event index 3)
    december_solstices = [t for t, e in zip(times, events) if e == 3]

    # Find the most recent and next December solstice
    recent_solstice = max([t for t in december_solstices if t.tt < now.tt])
    next_solstice = min([t for t in december_solstices if t.tt > now.tt])

    # Apply longitudinal time correction
    longitudinal_time_tt = now.tt + (longitudinal_offset_hours / 24.0)
    longitudinal_time = ts.tt_jd(longitudinal_time_tt)

    # Calculate the year fraction
    year_duration = next_solstice.tt - recent_solstice.tt  # Total length of year in Julian days
    elapsed_time = longitudinal_time.tt - recent_solstice.tt  # Time passed since recent solstice

    # Compute divisions
    year_fraction = elapsed_time / year_duration
    division_2 = int(year_fraction * 2) + 1
    division_4 = int(year_fraction * 4) + 1
    division_8 = int(year_fraction * 8) + 1
    division_16 = int(year_fraction * 16) + 1
    division_32 = int(year_fraction * 32) + 1
    division_64 = int(year_fraction * 64) + 1

    # Print results
    print(f"{division_2}/2")
    print(f"{division_4}/4")
    print(f"{division_8}/8")
    print(f"{division_16}/16")
    print(f"{division_32}/32")
    print(f"{division_64}/64")

if __name__ == "__main__":
    main()