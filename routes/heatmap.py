from fastapi import APIRouter
from services.data_service import generate_heatmap_states

router = APIRouter(prefix="/api/heatmap", tags=["heatmap"])

@router.get('/india')
async def india():
    states = generate_heatmap_states()
    national = {"total_buzz": sum(s['buzz_intensity'] for s in states), "hotspots": [s['state'] for s in states[:3]], "emerging_regions": [s['state'] for s in states[-3:]]}
    return {"states": states, "national_trends": national}

@router.get('/trending')
async def trending():
    states = generate_heatmap_states()
    hotspots = sorted(states, key=lambda s: -s['buzz_intensity'])[:5]
    return {"hotspots": hotspots}

@router.get('/details/{state}')
async def details(state: str):
    states = generate_heatmap_states()
    matched = [s for s in states if s['state'].lower()==state.lower()]
    if not matched:
        return {"state": state, "message": "No data"}
    return matched[0]
