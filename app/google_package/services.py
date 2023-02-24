from .base import GoogleBaseClient


class GoogleClient(GoogleBaseClient):

    def _get_spreadsheet_create_body(self):
        return {
            'properties': {
                'title': f'Отчет от: {self._get_datetime()}',
                'locale': self.LOCALE,
            },
            'sheets': self.SHEETS_PROPERTIES,
        }

    def _get_spreadsheet_update_body(self):
        table = [
            ['Отчет от', self._get_datetime()],
            ['Топ проектов по скорости закрытия'],
            ['Название проекта', 'Время сбора', 'Описание'],
        ]
        if self.UPDATE_DATA:
            for project in self.UPDATE_DATA:
                table.append([
                    project.name,
                    str(project.close_date - project.create_date),
                    project.description,
                ])
        return {
            'majorDimension': self.DIMENSIONS,
            'values': table,
        }


google_client = GoogleClient()
