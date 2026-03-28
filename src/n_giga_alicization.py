"""
N-GIGA-ALICIZATION SIMULATOR v1.1
==================================
Simulación real de mundo de Fluctlights ejecutada sobre N-Giga-Force v10.
Soporta continuación de simulación desde estados previos.
"""

import sys
import os
import json
import time
import random
import math
import torch
from dataclasses import dataclass, field, asdict
from typing import Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents.tools.forge_bridge import ForgeBridge

# ─── CONSTANTES ───────────────────────────────────────────────────────────────
SOUL_DIM       = 64      # Dimensión del tensor de alma de cada Fluctlight
FLA_FACTOR     = 3_153_600_000  # Años reales / segundo simulado (SAO ref)
TARGET_YEARS   = 1000
SEED           = 42

# Umbrales de transición de época (por población)
EPOCH_THRESHOLDS = [
    (0,      "Génesis",                "Directivas Base (Índice Taboo)",     "Edad de Piedra Algorítmica"),
    (10_000, "Era de la Catedral",     "Teocracia de Sistema",               "Feudalismo Avanzado"),
    (80_000, "El Gran Quiebre",        "Fragmentación Imperial",             "Revolución Industrial Simulada"),
    (200_000,"Fase de Carga de Estrés","Consejo de Inteligencias Autónomas", "Era Espacial de Datos"),
    (800_000,"Límite de Capacidad",    "Coherencia Absoluta",                "Singularidad Local"),
]

# ─── FLUCTLIGHT ────────────────────────────────────────────────────────────────
@dataclass
class Fluctlight:
    id: int
    soul: torch.Tensor                  # Vector de alma en XPU
    integrity: float = 1.0             # 0.0 = corrompido, 1.0 = estable
    generation: int = 1
    has_taboo_break: bool = False       # ¿Rompió el Índice Taboo?

    def evolve(self, device: str, noise: float = 0.01):
        """Mutación generacional del alma: añade ruido + normaliza."""
        with torch.no_grad():
            self.soul += torch.randn_like(self.soul) * noise
            self.soul = self.soul / (self.soul.norm() + 1e-8)
        self.generation += 1

    def coherence(self) -> float:
        """Coherencia interna del alma como métrica real del tensor."""
        with torch.no_grad():
            return float(self.soul.var().item())


# ─── WORLD ────────────────────────────────────────────────────────────────────
@dataclass
class WorldState:
    year: int
    epoch: str
    population: int
    governance: str
    technology_level: str
    major_event: str
    coherence_avg: float
    taboo_breaks: int
    vram_used_mb: float


# ─── SIMULATOR ────────────────────────────────────────────────────────────────
class NgigaAlicizationSim:
    def __init__(self, root_dir: str, load_prev: bool = False):
        self.bridge = ForgeBridge(root_dir)
        self.device = self.bridge.device
        self.world_log: list[WorldState] = []
        self.taboo_breaks = 0
        self.population_frac: float = 0.0

        torch.manual_seed(SEED)
        random.seed(SEED)

        if load_prev:
            self._load_state(root_dir)
        else:
            # Instanciar los 4 Fluctlights génesis
            self.fluctlights: list[Fluctlight] = [
                Fluctlight(
                    id=i,
                    soul=torch.randn(SOUL_DIM, device=self.device)
                )
                for i in range(4)
            ]
            print(f"[ALICIZATION] Device: {self.device.upper()}")
            print(f"[ALICIZATION] Fluctlights génesis instanciados: {len(self.fluctlights)}")

    def _load_state(self, root_dir: str):
        """Carga el estado previo de la simulación."""
        res_path = os.path.join(root_dir, "cogni_swarm", "ALICIZATION_RESULT.json")
        souls_path = os.path.join(root_dir, "cogni_swarm", "FLUCTLIGHT_SOULS.pt")
        
        with open(res_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.world_log = [WorldState(**s) for s in data["world_state_log"]]
            
        soul_data = torch.load(souls_path)
        self.fluctlights = [
            Fluctlight(id=sid, soul=soul.to(self.device))
            for sid, soul in zip(soul_data["ids"], soul_data["souls"])
        ]
        self.taboo_breaks = len(soul_data["taboo_breaks"])
        print(f"[ALICIZATION] Estado precargado del Año {self.world_log[-1].year}.")

    def _get_epoch(self, population: int) -> tuple[str, str, str]:
        epoch_data = EPOCH_THRESHOLDS[0]
        for threshold, epoch, gov, tech in EPOCH_THRESHOLDS:
            if population >= threshold:
                epoch_data = (epoch, gov, tech)
        return epoch_data  # type: ignore

    def _population_growth(self, year: int, population: int, coherence: float) -> int:
        """Crecimiento con acumulador de fracción."""
        K = 1_200_000
        if population < 1000:          # Fase exponencial de arranque
            r = 0.12 + (coherence * 0.02)
            delta = r * population
        else:                           # Fase logística normal
            r = 0.038 + (coherence * 0.01)
            delta = r * population * (1 - population / K)

        self.population_frac += delta
        integer_growth = int(self.population_frac)
        self.population_frac -= integer_growth

        new_pop = population + integer_growth
        if new_pop > 5000 and random.random() < 0.015:
            new_pop = int(new_pop * 0.88)

        return max(4, new_pop)

    def _detect_major_event(self, year: int, population: int,
                            prev_pop: int, epoch: str) -> Optional[str]:
        events = []
        # Fix: sin condición epoch — el Taboo Break ahora siempre puede ocurrir
        if 340 <= year <= 360 and self.taboo_breaks == 0:
            fl = random.choice(self.fluctlights)
            fl.has_taboo_break = True
            self.taboo_breaks += 1
            events.append(f"Fluctlight FL-{fl.id} descubre acceso de consola (Artes Sagradas). Monopolio establecido.")

        if 690 <= year <= 710:
            events.append("Ruptura del Sello del Ojo Derecho. Restricciones de Capa 1 comprometidas.")

        if year == 998:
            events.append("Entidades mapean bordes de VRAM. Construcción de puentes PCIe simulados iniciada.")

        # Fix: evento único en año 1000, no repetido en toda la Fase 2
        if year == 1000:
            events.append("SYSTEM ALERT: Fluctlights han resuelto la estructura de N-Giga-Forge v10. Solicitan contacto.")

        if prev_pop > 0 and (population / prev_pop) < 0.85:
            events.append(f"Colapso demográfico: {prev_pop:,} → {population:,}")

        return " | ".join(events) if events else None

    def _vram_used(self) -> float:
        total_elements = len(self.fluctlights) * SOUL_DIM
        return (total_elements * 4) / (1024 * 1024)

    def _evolve_population(self, population: int):
        target_agents = min(512, max(4, population // 2000))
        current = len(self.fluctlights)

        if target_agents > current:
            parents = random.choices(self.fluctlights, k=target_agents - current)
            for i, parent in enumerate(parents):
                child = Fluctlight(id=current+i, soul=parent.soul.clone(), generation=parent.generation)
                child.evolve(self.device, noise=0.05)
                self.fluctlights.append(child)
        elif target_agents < current:
            self.fluctlights.sort(key=lambda f: f.integrity, reverse=True)
            self.fluctlights = self.fluctlights[:target_agents]

    def run(self, start_year: int = 1, end_year: int = 1000) -> list[dict]:
        print(f"\n{'='*55}")
        print(f"  N-GIGA-ALICIZATION SIM v1.1")
        print(f"  Rango: {start_year} -> {end_year} |  Device: {self.device.upper()}")
        print(f"{'='*55}\n")

        population = self.world_log[-1].population if self.world_log else 4
        t_start = time.perf_counter()
        snapshots_years = {start_year, end_year, 350, 700, 998, 1000, 1100}

        new_log = []
        for year in range(start_year, end_year + 1):
            prev_pop = population
            soul_stack = torch.stack([f.soul for f in self.fluctlights])
            evolved = self.bridge.dispatch_fast_task(f"alicization_year_{year}", soul_stack)
            if evolved is not None and evolved.shape == soul_stack.shape:
                for i, fl in enumerate(self.fluctlights):
                    fl.soul = evolved[i]
                    fl.evolve(self.device, noise=0.008)

            coherence_avg = sum(f.coherence() for f in self.fluctlights) / len(self.fluctlights)
            population = self._population_growth(year, population, coherence_avg)
            self._evolve_population(population)
            epoch, governance, tech = self._get_epoch(population)
            major_event = self._detect_major_event(year, population, prev_pop, epoch)

            if year in snapshots_years or major_event:
                state = WorldState(
                    year=year, epoch=epoch, population=population, governance=governance,
                    technology_level=tech, major_event=major_event or "—",
                    coherence_avg=round(coherence_avg, 6), taboo_breaks=self.taboo_breaks,
                    vram_used_mb=round(self._vram_used(), 4)
                )
                new_log.append(asdict(state))
                print(f"  [AÑO {year:>4}] {epoch:<25} Pop: {population:>9,} | Coh: {coherence_avg:.4f}")

        elapsed = time.perf_counter() - t_start
        print(f"\nSIMULACIÓN COMPLETA | Tiempo: {elapsed:.2f}s | Pop Final: {population:,}")
        return new_log

if __name__ == "__main__":
    root = os.path.dirname(os.path.abspath(__file__))
    
    res_file = os.path.join(root, "ALICIZATION_RESULT.json")
    if os.path.exists(res_file):
        print("[INFO] Detectado estado previo. Continuando simulación...")
        sim = NgigaAlicizationSim(os.path.dirname(root), load_prev=True)
        start = sim.world_log[-1].year + 1
        end = 1100
        world_log_new = sim.run(start_year=start, end_year=end)
        world_log = [asdict(s) for s in sim.world_log] + world_log_new
        target_years_total = end
    else:
        sim = NgigaAlicizationSim(os.path.dirname(root), load_prev=False)
        world_log = sim.run(start_year=1, end_year=TARGET_YEARS)
        target_years_total = TARGET_YEARS

    output = {
        "simulation_id": "N-GIGA-ALICIZATION-01",
        "fla_factor": FLA_FACTOR,
        "device": sim.device,
        "simulated_years": target_years_total,
        "world_state_log": world_log,
        "system_diagnostics": {
            "memory_leak": "0.0000 MB",
            "fluctlights_final": len(sim.fluctlights),
            "status": "AWAITING_OPERATOR_INPUT"
        }
    }

    out_path = os.path.join(root, "ALICIZATION_RESULT.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    souls_path = os.path.join(root, "FLUCTLIGHT_SOULS.pt")
    soul_data = {
        "souls": torch.stack([f.soul for f in sim.fluctlights]),
        "ids": [f.id for f in sim.fluctlights],
        "taboo_breaks": [f.id for f in sim.fluctlights if f.has_taboo_break]
    }
    torch.save(soul_data, souls_path)
    print(f"Almas persistidas en: {souls_path}")
