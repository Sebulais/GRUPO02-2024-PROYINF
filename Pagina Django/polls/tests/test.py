
import unittest
from unittest.mock import patch, MagicMock
from polls.models import Boletin, InformacionCientifica

# Importar las funciones de señales para asegurarnos que se conectan
import polls.signals


class TestSignals(unittest.TestCase):

    @patch('app.utils.notificar')
    def test_boletin_listo_notificacion_called(self, mock_notificar):
        boletin = Boletin(estado='Listo para revisión')
        # Simular save que dispara post_save
        boletin.save()
        # Verificar que notificar fue llamada
        mock_notificar.assert_called_once_with('boletin_listo', boletin)

    @patch('app.utils.notificar')
    def test_boletin_listo_notificacion_not_called(self, mock_notificar):
        boletin = Boletin(estado='En proceso')
        boletin.save()
        mock_notificar.assert_not_called()

    @patch('app.utils.notificar')
    def test_info_relevante_notificacion_called(self, mock_notificar):
        info = InformacionCientifica(es_relevante=True)
        info.save()
        mock_notificar.assert_called_once_with('nueva_info_relevante', info)

    @patch('app.utils.notificar')
    def test_info_relevante_notificacion_not_called(self, mock_notificar):
        info = InformacionCientifica(es_relevante=False)
        info.save()
        mock_notificar.assert_not_called()


if __name__ == '__main__':
    unittest.main()
