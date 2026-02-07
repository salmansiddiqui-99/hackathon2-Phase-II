"""
Language Detection and Localization Utilities
"""
from typing import Dict, Optional, Tuple
from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException
import logging

# Set seed for consistent results
DetectorFactory.seed = 0

logger = logging.getLogger(__name__)

# Language code to language name mapping
LANGUAGE_NAMES = {
    'en': 'English',
    'es': 'Spanish',
    'fr': 'French',
    'de': 'German',
    'it': 'Italian',
    'pt': 'Portuguese',
    'ru': 'Russian',
    'zh-cn': 'Chinese (Simplified)',
    'zh-tw': 'Chinese (Traditional)',
    'ja': 'Japanese',
    'ko': 'Korean',
    'ar': 'Arabic',
    'hi': 'Hindi',
    'bn': 'Bengali',
    'pa': 'Punjabi',
    'te': 'Telugu',
    'mr': 'Marathi',
    'ta': 'Tamil',
    'ur': 'Urdu',
}

# Language code to ISO 639-1 mapping for consistency
LANGUAGE_CODE_MAP = {
    'zh': 'zh-cn',  # Map Chinese to Simplified Chinese
    'zh-Hans': 'zh-cn',
    'zh-Hant': 'zh-tw',
    'deu': 'de',  # Map German ISO 639-2 to ISO 639-1
    'deutsch': 'de',
    'fra': 'fr',  # Map French ISO 639-2 to ISO 639-1
    'français': 'fr',
    'ita': 'it',  # Map Italian ISO 639-2 to ISO 639-1
    'italiano': 'it',
    'por': 'pt',  # Map Portuguese ISO 639-2 to ISO 639-1
    'português': 'pt',
    'rus': 'ru',  # Map Russian ISO 639-2 to ISO 639-1
    'русский': 'ru',
    'jpn': 'ja',  # Map Japanese ISO 639-2 to ISO 639-1
    'arb': 'ar',  # Map Arabic ISO 639-2 to ISO 639-1
    'ara': 'ar',
}

class LanguageDetector:
    """Utility class for detecting and handling language in user input."""

    @staticmethod
    def detect_language(text: str) -> Tuple[str, float]:
        """
        Detect the language of the given text.

        Args:
            text: Input text to detect language for

        Returns:
            Tuple of (detected_language_code, confidence_score)
        """
        if not text or len(text.strip()) < 3:
            return 'en', 0.0  # Default to English for very short texts

        try:
            # Detect language using langdetect
            detected_lang = detect(text)

            # Map to standard codes if needed
            mapped_lang = LANGUAGE_CODE_MAP.get(detected_lang, detected_lang.lower())

            # Since langdetect doesn't provide confidence directly,
            # we'll estimate confidence based on text length and reliability
            # This is a simple heuristic
            confidence = min(0.95, len(text) / 50) if len(text) < 50 else 0.95

            return mapped_lang, confidence

        except LangDetectException as e:
            logger.warning(f"Language detection failed for text: {text[:50]}... Error: {e}")
            return 'en', 0.0
        except Exception as e:
            logger.error(f"Unexpected error in language detection: {e}")
            return 'en', 0.0

    @staticmethod
    def get_language_name(lang_code: str) -> str:
        """Get the display name for a language code."""
        return LANGUAGE_NAMES.get(lang_code, lang_code)

    @staticmethod
    def is_supported_language(lang_code: str) -> bool:
        """Check if the language is supported."""
        return lang_code in LANGUAGE_NAMES


class LocalizationManager:
    """Manages language-specific responses and localization."""

    def __init__(self):
        # Default English responses
        self.responses = {
            'en': {
                'task_added': "Task '{title}' has been added successfully with ID {task_id}.",
                'tasks_list_empty': "You don't have any tasks.",
                'tasks_list_header': "You have {count} task(s):",
                'task_completed': "Task '{title}' has been marked as completed.",
                'task_incomplete': "Task '{title}' has been marked as incomplete.",
                'task_updated': "Task '{title}' has been updated successfully.",
                'task_deleted': "Task '{title}' has been deleted successfully.",
                'error_occurred': "Error: {error}",
                'operation_success': "Operation completed successfully.",
                'confirm_delete': "Are you sure you want to delete the task \"{title}\"? This cannot be undone. Please confirm with yes/no.",
                'confirm_update': "Do you want to update the task \"{title}\" with the following changes?\n{changes}\nPlease confirm with yes/no.",
                'task_not_found': "Could not find a task matching '{title_query}'. Please check the task name and try again.",
                'task_not_found_with_suggestions': "Could not find a task matching '{title_query}'. Available tasks: {available_tasks}. Please check the task name and try again.",
            },
            'es': {
                'task_added': "La tarea '{title}' ha sido agregada exitosamente con ID {task_id}.",
                'tasks_list_empty': "No tienes tareas.",
                'tasks_list_header': "Tienes {count} tarea(s):",
                'task_completed': "La tarea '{title}' ha sido marcada como completada.",
                'task_incomplete': "La tarea '{title}' ha sido marcada como incompleta.",
                'task_updated': "La tarea '{title}' ha sido actualizada exitosamente.",
                'task_deleted': "La tarea '{title}' ha sido eliminada exitosamente.",
                'error_occurred': "Error: {error}",
                'operation_success': "Operación completada exitosamente.",
                'confirm_delete': "¿Estás seguro de que deseas eliminar la tarea \"{title}\"? Esta acción no se puede deshacer. Por favor confirma con sí/no.",
                'confirm_update': "¿Quieres actualizar la tarea \"{title}\" con los siguientes cambios?\n{changes}\nPor favor confirma con sí/no.",
                'task_not_found': "No se pudo encontrar una tarea que coincida con '{title_query}'. Por favor verifica el nombre de la tarea e inténtalo de nuevo.",
                'task_not_found_with_suggestions': "No se pudo encontrar una tarea que coincida con '{title_query}'. Tareas disponibles: {available_tasks}. Por favor verifica el nombre de la tarea e inténtalo de nuevo.",
            },
            'fr': {
                'task_added': "La tâche '{title}' a été ajoutée avec succès avec l'ID {task_id}.",
                'tasks_list_empty': "Vous n'avez aucune tâche.",
                'tasks_list_header': "Vous avez {count} tâche(s):",
                'task_completed': "La tâche '{title}' a été marquée comme terminée.",
                'task_incomplete': "La tâche '{title}' a été marquée comme incomplète.",
                'task_updated': "La tâche '{title}' a été mise à jour avec succès.",
                'task_deleted': "La tâche '{title}' a été supprimée avec succès.",
                'error_occurred': "Erreur : {error}",
                'operation_success': "Opération terminée avec succès.",
                'confirm_delete': "Êtes-vous sûr de vouloir supprimer la tâche \"{title}\" ? Cette action est irréversible. Veuillez confirmer par oui/non.",
                'confirm_update': "Voulez-vous mettre à jour la tâche \"{title}\" avec les modifications suivantes ?\n{changes}\nVeuillez confirmer par oui/non.",
                'task_not_found': "Impossible de trouver une tâche correspondant à '{title_query}'. Veuillez vérifier le nom de la tâche et réessayer.",
                'task_not_found_with_suggestions': "Impossible de trouver une tâche correspondant à '{title_query}'. Tâches disponibles : {available_tasks}. Veuillez vérifier le nom de la tâche et réessayer.",
            },
            'de': {
                'task_added': "Die Aufgabe '{title}' wurde erfolgreich mit der ID {task_id} hinzugefügt.",
                'tasks_list_empty': "Sie haben keine Aufgaben.",
                'tasks_list_header': "Sie haben {count} Aufgabe(n):",
                'task_completed': "Die Aufgabe '{title}' wurde als abgeschlossen markiert.",
                'task_incomplete': "Die Aufgabe '{title}' wurde als unvollständig markiert.",
                'task_updated': "Die Aufgabe '{title}' wurde erfolgreich aktualisiert.",
                'task_deleted': "Die Aufgabe '{title}' wurde erfolgreich gelöscht.",
                'error_occurred': "Fehler: {error}",
                'operation_success': "Vorgang erfolgreich abgeschlossen.",
                'confirm_delete': "Sind Sie sicher, dass Sie die Aufgabe \"{title}\" löschen möchten? Dies kann nicht rückgängig gemacht werden. Bitte bestätigen Sie mit ja/nein.",
                'confirm_update': "Möchten Sie die Aufgabe \"{title}\" mit folgenden Änderungen aktualisieren?\n{changes}\nBitte bestätigen Sie mit ja/nein.",
                'task_not_found': "Konnte keine Aufgabe finden, die mit '{title_query}' übereinstimmt. Bitte überprüfen Sie den Aufgabenname und versuchen Sie es erneut.",
                'task_not_found_with_suggestions': "Konnte keine Aufgabe finden, die mit '{title_query}' übereinstimmt. Verfügbare Aufgaben: {available_tasks}. Bitte überprüfen Sie den Aufgabenname und versuchen Sie es erneut.",
            },
            'it': {
                'task_added': "L'attività '{title}' è stata aggiunta correttamente con ID {task_id}.",
                'tasks_list_empty': "Non hai attività.",
                'tasks_list_header': "Hai {count} attività:",
                'task_completed': "L'attività '{title}' è stata contrassegnata come completata.",
                'task_incomplete': "L'attività '{title}' è stata contrassegnata come incompleta.",
                'task_updated': "L'attività '{title}' è stata aggiornata correttamente.",
                'task_deleted': "L'attività '{title}' è stata cancellata correttamente.",
                'error_occurred': "Errore: {error}",
                'operation_success': "Operazione completata correttamente.",
                'confirm_delete': "Sei sicuro di voler eliminare l'attività \"{title}\"? Questa azione non può essere annullata. Per favore conferma con sì/no.",
                'confirm_update': "Vuoi aggiornare l'attività \"{title}\" con le seguenti modifiche?\n{changes}\nPer favore conferma con sì/no.",
                'task_not_found': "Impossibile trovare un'attività che corrisponda a '{title_query}'. Controlla il nome dell'attività e riprova.",
                'task_not_found_with_suggestions': "Impossibile trovare un'attività che corrisponda a '{title_query}'. Attività disponibili: {available_tasks}. Controlla il nome dell'attività e riprova.",
            },
            'pt': {
                'task_added': "A tarefa '{title}' foi adicionada com sucesso com o ID {task_id}.",
                'tasks_list_empty': "Você não tem tarefas.",
                'tasks_list_header': "Você tem {count} tarefa(s):",
                'task_completed': "A tarefa '{title}' foi marcada como concluída.",
                'task_incomplete': "A tarefa '{title}' foi marcada como incompleta.",
                'task_updated': "A tarefa '{title}' foi atualizada com sucesso.",
                'task_deleted': "A tarefa '{title}' foi excluída com sucesso.",
                'error_occurred': "Erro: {error}",
                'operation_success': "Operação concluída com sucesso.",
                'confirm_delete': "Tem certeza de que deseja excluir a tarefa \"{title}\"? Isso não pode ser desfeito. Por favor, confirme com sim/não.",
                'confirm_update': "Deseja atualizar a tarefa \"{title}\" com as seguintes alterações?\n{changes}\nPor favor, confirme com sim/não.",
                'task_not_found': "Não foi possível encontrar uma tarefa correspondente a '{title_query}'. Por favor, verifique o nome da tarefa e tente novamente.",
                'task_not_found_with_suggestions': "Não foi possível encontrar uma tarefa correspondente a '{title_query}'. Tarefas disponíveis: {available_tasks}. Por favor, verifique o nome da tarefa e tente novamente.",
            },
            'ru': {
                'task_added': "Задача '{title}' была успешно добавлена с ID {task_id}.",
                'tasks_list_empty': "У вас нет задач.",
                'tasks_list_header': "У вас {count} задач(и):",
                'task_completed': "Задача '{title}' была отмечена как выполненная.",
                'task_incomplete': "Задача '{title}' была отмечена как невыполненная.",
                'task_updated': "Задача '{title}' была успешно обновлена.",
                'task_deleted': "Задача '{title}' была успешно удалена.",
                'error_occurred': "Ошибка: {error}",
                'operation_success': "Операция выполнена успешно.",
                'confirm_delete': "Вы уверены, что хотите удалить задачу \"{title}\"? Это действие нельзя отменить. Пожалуйста, подтвердите да/нет.",
                'confirm_update': "Хотите обновить задачу \"{title}\" со следующими изменениями?\n{changes}\nПожалуйста, подтвердите да/нет.",
                'task_not_found': "Не удалось найти задачу, соответствующую '{title_query}'. Пожалуйста, проверьте название задачи и повторите попытку.",
                'task_not_found_with_suggestions': "Не удалось найти задачу, соответствующую '{title_query}'. Доступные задачи: {available_tasks}. Пожалуйста, проверьте название задачи и повторите попытку.",
            },
            'ja': {
                'task_added': "タスク '{title}' が正常に追加されました。ID: {task_id}",
                'tasks_list_empty': "タスクがありません。",
                'tasks_list_header': "{count} 個のタスクがあります:",
                'task_completed': "タスク '{title}' は完了としてマークされました。",
                'task_incomplete': "タスク '{title}' は未完了としてマークされました。",
                'task_updated': "タスク '{title}' が正常に更新されました。",
                'task_deleted': "タスク '{title}' は正常に削除されました。",
                'error_occurred': "エラー: {error}",
                'operation_success': "操作は正常に完了しました。",
                'confirm_delete': "本当にタスク \"{title}\" を削除してもよろしいですか？この操作は元に戻せません。はい/いいえで確認してください。",
                'confirm_update': "以下の変更を含むタスク \"{title}\" を更新しますか？\n{changes}\nはい/いいえで確認してください。",
                'task_not_found': "'{title_query}' に一致するタスクが見つかりませんでした。タスク名を確認して、もう一度試してください。",
                'task_not_found_with_suggestions': "'{title_query}' に一致するタスクが見つかりませんでした。利用可能なタスク: {available_tasks}。タスク名を確認して、もう一度試してください。",
            },
            'ar': {
                'task_added': "تمت إضافة المهمة '{title}' بنجاح مع المعرف {task_id}.",
                'tasks_list_empty': "لا توجد لديك مهام.",
                'tasks_list_header': "لديك {count} مهمة/مهمات:",
                'task_completed': "تم وضع علامة على المهمة '{title}' كمنتهية.",
                'task_incomplete': "تم وضع علامة على المهمة '{title}' كغير مكتملة.",
                'task_updated': "تم تحديث المهمة '{title}' بنجاح.",
                'task_deleted': "تم حذف المهمة '{title}' بنجاح.",
                'error_occurred': "خطأ: {error}",
                'operation_success': "اكتملت العملية بنجاح.",
                'confirm_delete': "هل أنت متأكد أنك تريد حذف المهمة \"{title}\"؟ لا يمكن التراجع عن هذا الإجراء. يرجى التأكيد بـ نعم/لا.",
                'confirm_update': "هل تريد تحديث المهمة \"{title}\" بالتغييرات التالية؟\n{changes}\nيرجى التأكيد بـ نعم/لا.",
                'task_not_found': "تعذر العثور على مهمة تطابق '{title_query}'. يرجى التحقق من اسم المهمة والمحاولة مرة أخرى.",
                'task_not_found_with_suggestions': "تعذر العثور على مهمة تطابق '{title_query}'. المهام المتوفرة: {available_tasks}. يرجى التحقق من اسم المهمة والمحاولة مرة أخرى.",
            }
        }

    def get_response(self, lang_code: str, key: str, **kwargs) -> str:
        """
        Get localized response for the given language.

        Args:
            lang_code: Language code (e.g., 'en', 'es', 'fr')
            key: Response key to lookup
            **kwargs: Additional parameters to format the response

        Returns:
            Localized response string
        """
        # Use the specified language if available, otherwise fall back to English
        lang_responses = self.responses.get(lang_code, self.responses['en'])
        response_template = lang_responses.get(key, self.responses['en'][key])

        try:
            return response_template.format(**kwargs)
        except KeyError:
            # If formatting fails due to missing keys, return the original template
            return response_template


# Global instances
language_detector = LanguageDetector()
localization_manager = LocalizationManager()