from django.urls import path
from .views import (SingleCardForBackendView, ListCardsForBackendView,
                    SingleCardForUser, ListMemorizedCards,
                    ListUserNotMemorizedCards, CramQueue,
                    ListOutstandingCards)

urlpatterns = [
    path("cards/",
         ListCardsForBackendView.as_view(),
         name="list_cards"),
    path("cards/<uuid:pk>/",
         SingleCardForBackendView.as_view(),
         name="single_card"),
    path("users/<uuid:user_pk>/cards/<uuid:card_pk>/",
         SingleCardForUser.as_view(),
         name="card_for_user"),

    # remove memorizing from this route
    path("users/<uuid:user_pk>/cards/<uuid:card_pk>/grade/<int:grade>/",
         SingleCardForUser.as_view(),
         name="memorize_review_card"),

    # TODO: Reviewing:
    # POST users/<uuid:user_pk>/cards/memorized/<card_id>
    # body: { "grade": 4 }
    path("users/<uuid:user_pk>/cards/memorized",
         ListMemorizedCards.as_view(),
         name="list_of_memorized_cards_for_user"),
    path("users/<uuid:user_pk>/cards/outstanding",
         ListOutstandingCards.as_view(),
         name="outstanding_cards"),

    # queued cards
    # TODO: memorizing:
    # POST "users/<uuid:user_pk>/cards/queued/<card_id>"
    # body: { "grade": 4 }
    # grade should go into request body; request using POST
    # rather than PUT
    path("users/<uuid:user_pk>/cards/queued",
         ListUserNotMemorizedCards.as_view(),
         name="list_of_not_memorized_cards_for_user"),

    # cram queue
    path("users/<uuid:user_pk>/cards/cram-queue/<uuid:card_pk>",
         CramQueue.as_view(),
         name="cram_queue"),
    path("users/<uuid:user_pk>/cards/cram-queue",
         CramQueue.as_view(),
         name="get_cram_queue"),
]
