# What I checked, and what the agent got wrong

## What the agent got wrong

While reviewing the agent's write-up of the helper-module sweep, I noticed it claimed that
`chunk_list()` in `fleet_utils.py` "was copied from Stack Overflow in 2013." When I checked the
actual comment in the file, it only says `chunk_list (never called)` — there is no mention of
Stack Overflow, or any source, anywhere. The agent invented a specific, plausible-sounding detail
that isn't backed up by anything in the codebase. It's a small thing on its own, but it's exactly
the kind of confident, unverifiable claim that's easy to accept at face value in a long, otherwise
accurate-looking summary — which is why I went back and checked the source line instead of taking
the write-up as given.

## What I checked before I accepted its work

I ran `python verify.py` myself and watched it move from failing checks to 10 of 11 passing after
the fixes and the risk analysis were in place. Beyond the pass/fail count, I specifically confirmed
that `SERVICE_INTERVAL_KM` and `WARN_AT_PERCENT` were untouched — still `15000` and `80` in both
`km_wachter.py` and `settings.cfg` — since those were explicitly not supposed to change. I also
checked the wear calculation directly: a car at 14,900 of 15,000 km now reports 99.3% instead of
the old floored 0%, which is the core bug the whole task hinges on.

## What the data actually said

Before looking at `fleet_history.csv`, I expected total mileage (`odometer_km`) to be the strongest
predictor of a breakdown — more kilometres, more wear, seemed obvious. The numbers said otherwise:
mean odometer readings were almost identical between cars that broke down and cars that didn't
(~53,302 km vs ~53,448 km, p ≈ 0.98), and `age_years` showed the same non-pattern. What actually
separated the two groups was `km_since_service` (7,261 vs 11,678 km, the largest gap by far),
along with `avg_daily_km` and `load_factor` — in other words, how overdue a car is for service and
how hard it's being driven since then, not how many total kilometres it's ever done.
