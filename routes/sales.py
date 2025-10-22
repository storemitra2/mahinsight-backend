from fastapi import APIRouter, UploadFile, File, HTTPException
from services.data_service import generate_sales_data
import csv
from io import StringIO
from datetime import datetime, timedelta

router = APIRouter(prefix="/api/sales", tags=["sales"])

@router.get('/overview')
async def overview():
    data = generate_sales_data(1)
    total_sales = sum(d['units_sold'] for d in data)
    top = {}
    for d in data:
        top.setdefault(d['vehicle_model'],0)
        top[d['vehicle_model']] += d['units_sold']
    top_models = sorted([{"model":k,"sales":v} for k,v in top.items()], key=lambda x: -x['sales'])[:5]
    return {"total_sales": total_sales, "top_models": top_models}

@router.get('/regions')
async def regions():
    data = generate_sales_data(1)
    regions = {}
    for d in data:
        regions.setdefault(d['region'],0)
        regions[d['region']]+= d['units_sold']
    return {"regional_performance":[{"region":k,"sales":v} for k,v in regions.items()]}

@router.get('/models')
async def models():
    data = generate_sales_data(1)
    models = {}
    for d in data:
        models.setdefault(d['vehicle_model'],0)
        models[d['vehicle_model']]+=d['units_sold']
    return {"models": [{"model":k,"sales":v} for k,v in models.items()]}

@router.get('/trends')
async def trends(days: int = 30):
    data = generate_sales_data(2)
    # simple aggregation by date
    by_date = {}
    for d in data:
        by_date.setdefault(d['date'],0)
        by_date[d['date']]+=d['units_sold']
    items = sorted(by_date.items())[-days:]
    return {"trends": items}

@router.post('/upload')
async def upload(csvfile: UploadFile = File(...)):
    content = await csvfile.read()
    s = content.decode('utf-8')
    reader = csv.DictReader(StringIO(s))
    processed = []
    for row in reader:
        processed.append(row)
    return {"processed": len(processed)}
