var AcMath = (function () {
  function num(x) { return typeof x === "number" && isFinite(x); }
  function r1(x) { return Math.round(x * 10) / 10; }
  function money(x) { return Math.round(x * 100) / 100; }
  function jsnum(x) { if (typeof x === "number" && isFinite(x) && x === Math.trunc(x)) return String(Math.trunc(x)); return String(x); }
  function comma(x) { return String(x).replace(/\B(?=(\d{3})+(?!\d))/g, ","); }
  function money2(x) { return money(x).toFixed(2); }
  function chart(sqft) {
    if (sqft <= 150) return 5000;
    if (sqft <= 250) return 6000;
    if (sqft <= 300) return 7000;
    if (sqft <= 350) return 8000;
    if (sqft <= 400) return 9000;
    if (sqft <= 450) return 10000;
    if (sqft <= 550) return 12000;
    if (sqft <= 700) return 14000;
    return sqft * 20;
  }
  function sizePlan(sqft, heightFt) {
    if (!num(sqft)) return { error: "the room area must be a number" };
    if (!num(heightFt)) return { error: "the ceiling height must be a number" };
    if (sqft <= 0) return { error: "the room area must be above zero" };
    if (heightFt <= 0) return { error: "the ceiling height must be above zero" };
    return { btu: Math.round(chart(sqft) * heightFt / 8) };
  }
  function renderSize(r, sqft, heightFt) {
    return "Your " + jsnum(sqft) + " sq ft room with " + jsnum(heightFt) + " ft ceilings wants about " + comma(r.btu)
      + " BTU before conditions - add 10% for full sun, drop 10% for deep shade, add 4,000 for a kitchen, and 600 per person past two.";
  }
  function powerPlan(btu, ceer) {
    if (!num(btu)) return { error: "the BTU rating must be a number" };
    if (!num(ceer)) return { error: "the CEER must be a number" };
    if (btu <= 0) return { error: "the BTU rating must be above zero" };
    if (ceer <= 0) return { error: "the CEER must be above zero" };
    return { watts: r1(btu / ceer) };
  }
  function renderPower(r, btu, ceer) {
    return "The " + comma(btu) + " BTU unit at CEER " + jsnum(ceer) + " pulls about " + jsnum(r.watts)
      + " watts while the compressor runs - the box prints the BTU big and the efficiency that divides it small.";
  }
  function billPlan(watts, hours, rate) {
    if (!num(watts)) return { error: "the wattage must be a number" };
    if (!num(hours)) return { error: "the hours must be a number" };
    if (!num(rate)) return { error: "the rate must be a number" };
    if (watts <= 0) return { error: "the wattage must be above zero" };
    if (hours < 0) return { error: "the hours cannot be negative" };
    if (hours > 24) return { error: "a day only has 24 hours" };
    if (rate <= 0) return { error: "the rate must be above zero" };
    var kwh = watts / 1000 * hours;
    return { kwh: r1(kwh), day: money(kwh * rate), month: money(kwh * rate * 30) };
  }
  function renderBill(r, watts, hours, rate) {
    return "At " + jsnum(watts) + " watts for " + jsnum(hours) + " hours a day and $" + money2(rate)
      + " per kWh, the room uses " + jsnum(r.kwh) + " kWh and costs about $" + money2(r.day) + " a day, $" + money2(r.month)
      + " over a 30-day month - the yellow sticker priced a shorter season at a cheaper kilowatt.";
  }
  return { sizePlan: sizePlan, renderSize: renderSize, powerPlan: powerPlan, renderPower: renderPower, billPlan: billPlan, renderBill: renderBill };
})();
if (typeof module !== "undefined" && module.exports) module.exports = AcMath;
