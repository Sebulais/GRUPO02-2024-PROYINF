import unittest
from unittest.mock import patch
from polls.models import Boletin, InformacionCientifica
from django.utils.translation import activate, gettext as _
import polls.signals


class TestSignals(unittest.TestCase):
    saved_instances = []  # Lista para rastrear instancias guardadas

    @classmethod
    def setUpClass(cls):
        """Configuración inicial para toda la clase de tests"""
        print("\n=== Inicializando recursos para todos los tests ===")

    @classmethod
    def tearDownClass(cls):
        """Limpieza final para toda la clase de tests"""
        print("\n=== Limpieza final después de todos los tests ===")
        # Limpieza adicional si es necesaria

    def setUp(self):
        """Configuración antes de cada test"""
        print(f"\nPreparando test: {self._testMethodName}")
        # Creamos instancias para cada test
        self.boletin_listo = Boletin(estado='Listo para revisión')
        self.boletin_en_proceso = Boletin(estado='En proceso')
        self.info_relevante = InformacionCientifica(es_relevante=True)
        self.info_no_relevante = InformacionCientifica(es_relevante=False)
        self.traduccion_aleman = Traduccion(estado='Nachrichtenbulletin')
        slef.traduccion_ingles = Traduccion(estado='News Bulletin')

    def tearDown(self):
        """Limpieza después de cada test"""
        # Limpiamos solo las instancias guardadas durante un test
        print("Limpiando test...")
        for instance in self.saved_instances:
            if instance.pk is not None:
                instance.delete()
        self.saved_instances.clear()

    def _guardar_instancia(self, instance):
        """Helper para guardar instancias y registrar para limpieza"""
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
    
            
    def test_traduccion_a_ingles(self, mock_notificar):
        print("\n[TEST] test_traduccion_a_ingles")
        activate('en')
        texto_original = _("Boletín de Noticias")
        print(f"Input: idioma = 'en', texto original = 'Boletín de Noticias'")
        try:
            self.assertEqual(texto_original, "News Bulletin")
            print("Output esperado: 'News Bulletin' → Traducción correcta")
        except AssertionError as e:
            print(f"Output inesperado: '{texto_original}' ≠ 'News Bulletin'")
            raise

    def test_traduccion_a_aleman(self, mock_notificar):
        print("\n[TEST] test_traduccion_a_aleman")
        activate('de')
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
