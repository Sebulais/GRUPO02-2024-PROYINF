import unittest
from unittest.mock import patch
from polls.models import Boletin, InformacionCientifica
from django.utils.translation import activate, deactivate, gettext as _
import polls.signals


class TestSignals(unittest.TestCase):
    saved_instances = []
    idioma_test = None  # Para guardar el idioma a activar en los tests de traducción

    @classmethod
    def setUpClass(cls):
        print("\n=== Inicializando recursos para todos los tests ===")

    @classmethod
    def tearDownClass(cls):
        print("\n=== Limpieza final después de todos los tests ===")

    def setUp(self):
        print(f"\nPreparando test: {self._testMethodName}")
        self.boletin_listo = Boletin(estado='Listo para revisión')
        self.boletin_en_proceso = Boletin(estado='En proceso')
        self.info_relevante = InformacionCientifica(es_relevante=True)
        self.info_no_relevante = InformacionCientifica(es_relevante=False)

        # Activar idioma si está definido en el test
        if self.idioma_test:
            activate(self.idioma_test)

    def tearDown(self):
        print("Limpiando test...")
        for instance in self.saved_instances:
            if instance.pk is not None:
                instance.delete()
        self.saved_instances.clear()

        # Restaurar idioma por defecto
        if self.idioma_test:
            deactivate()
            self.idioma_test = None

    def _guardar_instancia(self, instance):
        instance.save()
        self.saved_instances.append(instance)
        return instance

    @patch('polls.signals.notificar')
    def test_boletin_listo_notificacion_called(self, mock_notificar):
        print("\n[TEST] test_boletin_listo_notificacion_called")
        print(f"Input: estado = {self.boletin_listo.estado}")
        boletin = self._guardar_instancia(self.boletin_listo)
        try:
            mock_notificar.assert_called_once_with('boletin_listo', boletin)
            print("Output esperado: notificar('boletin_listo', boletin) → Llamado correctamente")
        except AssertionError as e:
            print("Output inesperado:", str(e))
            raise

    @patch('polls.signals.notificar')
    def test_boletin_listo_notificacion_not_called(self, mock_notificar):
        print("\n[TEST] test_boletin_listo_notificacion_not_called")
        print(f"Input: estado = {self.boletin_en_proceso.estado}")
        self._guardar_instancia(self.boletin_en_proceso)
        if not mock_notificar.called:
            print("Output esperado: notificar() → No llamado")
        else:
            print("Output inesperado: notificar() fue llamado")
            self.fail("notificar fue llamado cuando no debía")

    @patch('polls.signals.notificar')
    def test_info_relevante_notificacion_called(self, mock_notificar):
        print("\n[TEST] test_info_relevante_notificacion_called")
        print(f"Input: es_relevante = {self.info_relevante.es_relevante}")
        info = self._guardar_instancia(self.info_relevante)
        try:
            mock_notificar.assert_called_once_with('nueva_info_relevante', info)
            print("Output esperado: notificar('nueva_info_relevante', info) → Llamado correctamente")
        except AssertionError as e:
            print("Output inesperado:", str(e))
            raise

    @patch('polls.signals.notificar')
    def test_info_relevante_notificacion_not_called(self, mock_notificar):
        print("\n[TEST] test_info_relevante_notificacion_not_called")
        print(f"Input: es_relevante = {self.info_no_relevante.es_relevante}")
        self._guardar_instancia(self.info_no_relevante)
        if not mock_notificar.called:
            print("Output esperado: notificar() → No llamado")
        else:
            print("Output inesperado: notificar() fue llamado")
            self.fail("notificar fue llamado cuando no debía")

    def test_traduccion_a_ingles(self):
        print("\n[TEST] test_traduccion_a_ingles")
        self.idioma_test = 'en'
        texto_original = _("Boletín de Noticias")
        print(f"Input: idioma = 'en', texto original = 'Boletín de Noticias'")
        try:
            self.assertEqual(texto_original, "News Bulletin")
            print("Output esperado: 'News Bulletin' → Traducción correcta")
        except AssertionError as e:
            print(f"Output inesperado: '{texto_original}' ≠ 'News Bulletin'")
            raise

    def test_traduccion_a_aleman(self):
        print("\n[TEST] test_traduccion_a_aleman")
        self.idioma_test = 'de'
        texto_original = _("Boletín de Noticias")
        print(f"Input: idioma = 'de', texto original = 'Boletín de Noticias'")
        try:
            self.assertEqual(texto_original, "Nachrichtenbulletin")
            print("Output esperado: 'Nachrichtenbulletin' → Traducción correcta")
        except AssertionError as e:
            print(f"Output inesperado: '{texto_original}' ≠ 'Nachrichtenbulletin'")
            raise


if __name__ == '__main__':
    unittest.main()


#Para ejecutar los tests, usar el tests.py que esta en la carpeta polls usando python manage.py test