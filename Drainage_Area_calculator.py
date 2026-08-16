# -*- coding: utf-8 -*-
"""
Drainage Area Composite C and CN Calculation Engine
"""

UNIT_CONVERSIONS_TO_SQFT = {
    "sq ft (ft²)": 1.0,
    "acres": 43560.0,
    "sq miles (mi²)": 27878400.0,
    "sq yards (yd²)": 9.0,
}


def get_subarea_label(index: int) -> str:
  """Generates alphabetical labels: 0->A, 1->B, 2->C ... 25->Z, 26->AA, etc."""
  label = ""
  while index >= 0:
    label = chr(65 + (index % 26)) + label
    index = (index // 26) - 1
  return label


def convert_to_sqft(value, unit):
  """Converts any supported area unit to square feet."""
  if value is None:
    return None
  factor = UNIT_CONVERSIONS_TO_SQFT.get(unit, 1.0)
  return float(value) * factor


def convert_from_sqft(value_sqft, target_unit):
  """Converts square feet back to the target display unit."""
  if value_sqft is None:
    return None
  factor = UNIT_CONVERSIONS_TO_SQFT.get(target_unit, 1.0)
  return value_sqft / factor


def compute_composite_c(sub_areas, total_area_val=None, total_area_unit="acres"):
  """Computes composite Runoff Coefficient (C)."""
  total_sqft_input = (
      convert_to_sqft(total_area_val, total_area_unit)
      if total_area_val is not None and str(total_area_val).strip() != ""
      else None
  )

  parsed = []
  missing_count = 0
  missing_index = -1

  for i, sa in enumerate(sub_areas):
    area_val = sa.get("area")
    unit = sa.get("unit", "acres")
    c = float(sa.get("c", 0.0))
    default_name = f"Sub-area {get_subarea_label(i)}"
    name = sa.get("name", default_name).strip() or default_name

    if area_val is None or str(area_val).strip() == "":
      missing_count += 1
      missing_index = i
      area_sqft = None
    else:
      try:
        area_sqft = convert_to_sqft(float(area_val), unit)
      except ValueError:
        raise ValueError(f"Invalid area value entered for '{name}'.")

    parsed.append(
        {"name": name, "area_sqft": area_sqft, "c": c, "unit": unit}
    )

  if missing_count > 1:
    raise ValueError(
        "At most one sub-area area can be left blank when solving against"
        " Total Drainage Area."
    )

  if missing_count == 1:
    if total_sqft_input is None:
      raise ValueError(
          "Total Drainage Area must be provided if one sub-area area is"
          " missing."
      )
    known_sum = sum(
        sa["area_sqft"] for sa in parsed if sa["area_sqft"] is not None
    )
    if total_sqft_input <= known_sum:
      raise ValueError(
          "Total Drainage Area must be greater than the sum of known sub-areas."
      )
    missing_sqft = total_sqft_input - known_sum
    parsed[missing_index]["area_sqft"] = missing_sqft
    parsed[missing_index]["area_display"] = convert_from_sqft(
        missing_sqft, parsed[missing_index]["unit"]
    )
    total_sqft = total_sqft_input
  else:
    total_sqft = sum(sa["area_sqft"] for sa in parsed)
    for sa in parsed:
      sa["area_display"] = convert_from_sqft(sa["area_sqft"], sa["unit"])

  if total_sqft <= 0:
    raise ValueError("Total drainage area must be greater than zero.")

  sum_c_a = sum(sa["c"] * sa["area_sqft"] for sa in parsed)
  c_composite = sum_c_a / total_sqft

  return {
      "sub_areas": parsed,
      "total_sqft": total_sqft,
      "total_acres": convert_from_sqft(total_sqft, "acres"),
      "c_composite": round(c_composite, 3),
      "solved_index": missing_index if missing_count == 1 else -1,
  }


def compute_composite_cn(
    sub_areas, total_area_val=None, total_area_unit="acres"
):
  """Computes composite Curve Number (CN)."""
  total_sqft_input = (
      convert_to_sqft(total_area_val, total_area_unit)
      if total_area_val is not None and str(total_area_val).strip() != ""
      else None
  )

  parsed = []
  missing_count = 0
  missing_index = -1

  for i, sa in enumerate(sub_areas):
    area_val = sa.get("area")
    unit = sa.get("unit", "acres")
    cn = float(sa.get("cn", 0.0))
    default_name = f"Sub-area {get_subarea_label(i)}"
    name = sa.get("name", default_name).strip() or default_name

    if area_val is None or str(area_val).strip() == "":
      missing_count += 1
      missing_index = i
      area_sqft = None
    else:
      try:
        area_sqft = convert_to_sqft(float(area_val), unit)
      except ValueError:
        raise ValueError(f"Invalid area value entered for '{name}'.")

    parsed.append(
        {"name": name, "area_sqft": area_sqft, "cn": cn, "unit": unit}
    )

  if missing_count > 1:
    raise ValueError(
        "At most one sub-area area can be left blank when solving against"
        " Total Drainage Area."
    )

  if missing_count == 1:
    if total_sqft_input is None:
      raise ValueError(
          "Total Drainage Area must be provided if one sub-area area is"
          " missing."
      )
    known_sum = sum(
        sa["area_sqft"] for sa in parsed if sa["area_sqft"] is not None
    )
    if total_sqft_input <= known_sum:
      raise ValueError(
          "Total Drainage Area must be greater than the sum of known sub-areas."
      )
    missing_sqft = total_sqft_input - known_sum
    parsed[missing_index]["area_sqft"] = missing_sqft
    parsed[missing_index]["area_display"] = convert_from_sqft(
        missing_sqft, parsed[missing_index]["unit"]
    )
    total_sqft = total_sqft_input
  else:
    total_sqft = sum(sa["area_sqft"] for sa in parsed)
    for sa in parsed:
      sa["area_display"] = convert_from_sqft(sa["area_sqft"], sa["unit"])

  if total_sqft <= 0:
    raise ValueError("Total drainage area must be greater than zero.")

  sum_cn_a = sum(sa["cn"] * sa["area_sqft"] for sa in parsed)
  cn_composite = sum_cn_a / total_sqft

  return {
      "sub_areas": parsed,
      "total_sqft": total_sqft,
      "total_acres": convert_from_sqft(total_sqft, "acres"),
      "cn_composite": round(cn_composite, 2),
      "solved_index": missing_index if missing_count == 1 else -1,
  }