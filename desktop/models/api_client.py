"""
Simple API client for communicating with the backend server.
Centralizes all network calls so views don't import requests directly.
"""

from typing import Any, Dict, Optional

import requests

from config.constants import API_BASE_URL, API_TIMEOUT


def get_students(page: int = 1, page_size: int = 12, search: str = "") -> Dict[str, Any]:
    params: Dict[str, Any] = {"page": page, "page_size": page_size}
    if search:
        params["search"] = search
    response = requests.get(f"{API_BASE_URL}/students", params=params, timeout=API_TIMEOUT)
    response.raise_for_status()
    data = response.json()
    # Support both paginated dict or raw list responses from backend
    if isinstance(data, list):
        total = len(data)
        start = (page - 1) * page_size
        return {
            "meta": {"total": total, "page": page, "page_size": page_size},
            "items": data[start : start + page_size],
        }
    
    print("Test", data)
    return data


def create_student(payload: Dict[str, Any]) -> Dict[str, Any]:
    response = requests.post(f"{API_BASE_URL}/students", json=payload, timeout=API_TIMEOUT)
    if response.status_code not in (200, 201):
        # Raise for non-success to allow callers to fallback to local behavior
        response.raise_for_status()
    return response.json()


def update_student(student_id: int, payload: Dict[str, Any]) -> Dict[str, Any]:
    response = requests.put(
        f"{API_BASE_URL}/students/{student_id}", json=payload, timeout=API_TIMEOUT
    )
    response.raise_for_status()
    return response.json()


def delete_student(student_id: int) -> bool:
    response = requests.delete(f"{API_BASE_URL}/students/{student_id}", timeout=API_TIMEOUT)
    if response.status_code not in (200, 204):
        response.raise_for_status()
    return True


def update_student_grades(student_code: str, grades: Dict[str, Any]) -> Dict[str, Any]:
    """Cập nhật điểm số của học sinh theo mã học sinh"""
    response = requests.patch(
        f"{API_BASE_URL}/students/by-code/{student_code}/grades", 
        json=grades, 
        timeout=API_TIMEOUT
    )
    response.raise_for_status()
    return response.json()


