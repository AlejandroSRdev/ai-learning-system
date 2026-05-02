from fastapi import APIRouter, Depends, HTTPException

from src.ai.exceptions import AIOutputValidationError, AITransientError
from src.api.deps import get_pool
from src.services.explain import generate_explanation

router = APIRouter()


@router.post("/{student_id}")
async def explain(student_id: int, pool=Depends(get_pool)):
    try:
        return await generate_explanation(student_id, pool)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except AIOutputValidationError as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    except AITransientError as exc:
        raise HTTPException(status_code=503, detail=str(exc))
