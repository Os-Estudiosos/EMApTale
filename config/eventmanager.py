from pygame.event import Event

class EventManager:
    """Essa classe serve para armazenar todos os eventos de um frame especifico, pois o pygame.event.get() remove todos os eventos da lista
    """
    events: list[Event] = []
