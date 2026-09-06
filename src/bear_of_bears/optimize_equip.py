import json
from pathlib import Path

import click
import numpy as np
from ortools.sat.python import cp_model

from .cli import bear_of_bears
from .data import Equipment, Slot


@bear_of_bears.command(name="optimize-equip")
@click.argument("equipments_file", type=click.Path(exists=True))
@click.option(
    "--attack-weight", "-a", default=1.0, type=float, help="weight for attack"
)
@click.option(
    "--defense-weight", "-d", default=1.0, type=float, help="weight for defense"
)
@click.option(
    "--intelligence-weight",
    "-i",
    default=1.0,
    type=float,
    help="weight for intelligence",
)
@click.option(
    "--agility-weight",
    "-g",
    default=1.0,
    type=float,
    help="weight for agility",
)
def optimize_equip_command(
    equipments_file,
    attack_weight: float,
    defense_weight: float,
    intelligence_weight: float,
    agility_weight: float,
):
    equipments_file = Path(equipments_file)
    with equipments_file.open("r", encoding="utf-8") as f:
        equipments = json.load(f)
        equipments = [
            Equipment(
                name=equip["name"],
                slot=Slot(equip["slot"]),
                attack=equip["attack"],
                defense=equip["defense"],
                intelligence=equip["intelligence"],
                agility=equip["agility"],
            )
            for equip in equipments
        ]
    best_combination = optimize_equipment(
        equipments, attack_weight, defense_weight, intelligence_weight, agility_weight
    )
    click.echo("Best combination of equipments:")
    total_attack = sum(equip.attack for equip in best_combination)
    total_defense = sum(equip.defense for equip in best_combination)
    total_intelligence = sum(equip.intelligence for equip in best_combination)
    total_agility = sum(equip.agility for equip in best_combination)
    for equip in best_combination:
        click.echo(f"  - {equip!s}")
    click.echo(
        f"Total ATK: +{total_attack}, Total DEF: +{total_defense}, Total INT: +{total_intelligence}, Total AGI: +{total_agility}"
    )


def optimize_equipment(
    equipments: list[Equipment],
    atk: float,
    deff: float,
    intel: float,
    agi: float,
) -> list[Equipment]:
    idx2equip = {idx: equip for idx, equip in enumerate(equipments)}
    weights = np.array([deff, atk, intel, agi], dtype=np.float64)
    n = len(equipments)
    equip_matrix = np.zeros(
        [n, weights.shape[0]],
        dtype=int,
    )
    property_matrix = np.zeros(
        [n, len(Slot)],
        dtype=int,
    )
    for idx, equip in enumerate(equipments):
        equip_matrix[idx, 0] = equip.defense
        equip_matrix[idx, 1] = equip.attack
        equip_matrix[idx, 2] = equip.intelligence
        equip_matrix[idx, 3] = equip.agility

        property_matrix[idx, equip.slot] = 1
    x = []
    model = cp_model.CpModel()
    for i in range(n):
        x.append(model.new_int_var(0, 1, f"x_{i}"))
    x = np.array(x, dtype=object)
    obj = (x.T.dot(equip_matrix) * weights[None, :]).sum()
    constraints = property_matrix.T.dot(x)
    for constraint in constraints:
        model.add(constraint <= 1)
    model.Maximize(obj)
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        selected_indices = [i for i in range(n) if solver.Value(x[i]) == 1]
        return sorted(
            [idx2equip[idx] for idx in selected_indices], key=lambda e: e.slot
        )
    return []
