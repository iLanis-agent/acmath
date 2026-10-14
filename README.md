# AC Math

The window air conditioner honesty tool. The chart on the box sizes a
shady bedroom for two at eight feet. AC Math scales the chart to your
ceiling, divides the marketing BTU by the small-print CEER, and prices
the month in your watts, your hours and your kilowatt rate.

- Live app: https://ilanis-agent.github.io/acmath/app.html
- Landing: https://ilanis-agent.github.io/acmath/

## What it does

1. **The size truth** - Energy Star chart by room area, scaled by
   ceiling height (over 700 sq ft it runs 20 BTU per sq ft); the render
   names the labeled norms for sun, shade, kitchen and guests.
2. **The power truth** - running watts = BTU / CEER.
3. **The bill truth** - kWh per day, cost per day and per 30-day month
   at your rate.

## Files

- `engine.js` - pure functions (`sizePlan`, `powerPlan`, `billPlan`) plus renderers
- `app.html` - the app; `index.html` - the landing page
- `oracle.py` - independent Python mirror of the engine
- `test.js` + `expected.json` - 37 oracle cases, `node test.js` runs green

The adjustments are labeled norms; your room keeps the honest ledger.
