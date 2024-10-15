import logging
from typing import Optional
from buco_db_controller.repositories.coefficients_repository import CoefficientsRepository

LOGGER = logging.getLogger(__name__)


class CoefficientsService:
    def __init__(self):
        self.coefficients_repository = CoefficientsRepository()

    def insert_coefficients(self, coefficients):
        self.coefficients_repository.insert_document('coefficients', coefficients)
        LOGGER.info('Inserted coefficients data')

    def get_coefficients(self, season: int) -> Optional[dict]:
        response = self.coefficients_repository.get_coefficients(season)

        if not response.get('data', []):
            return None

        coefficients = response['data']
        return coefficients
