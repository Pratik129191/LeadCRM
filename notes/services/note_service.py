from django.db import transaction

from ..models import Note
from core.events.event_bus import emit
from core.events.events import EventTypes
from core.constants import EntityType, AuditAction


class NoteService:
    @staticmethod
    @transaction.atomic
    def create_note(organization, user, content, lead=None, deal=None):
        note = Note.objects.create(
            organization=organization,
            user=user,
            content=content,
            lead=lead,
            deal=deal,
        )

        emit(
            event_type=EventTypes.NOTE_CREATED,
            payload={
                "organization": organization,
                "user": user,
                "action": AuditAction.NOTE_CREATED,
                "entity_type": EntityType.NOTE,
                "entity_id": note.id,
                "lead": lead,
                "metadata": {
                    "preview": content[:80]
                }
            }
        )

        return note


